from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.billing_service import pay_bill_logic
from app.models.bill import Bill
from app.models.usage import Usage

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("", methods=["POST"])
@swag_from({
    'tags': ['Billing'],
    'description': 'Pay a bill for a given month (No authentication required)',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'subscriber_no': {'type': 'string'},
                    'month': {'type': 'string'}
                },
                'required': ['subscriber_no', 'month']
            }
        }
    ],
    'responses': {
        200: {'description': 'Bill paid successfully or topped up'},
        400: {'description': 'No usage to pay for'}
    }
})
def pay_bill():
    data = request.get_json()
    subscriber_no = data.get("subscriber_no")
    month = data.get("month")
    response, status = pay_bill_logic(subscriber_no, month)
    return jsonify(response), status

@billing_bp.route("/bill", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'List all paid bills for the logged-in subscriber',
    'security': [{"Bearer": []}],
    'responses': {
        200: {
            'description': 'List of paid bills',
            'examples': {
                'application/json': [
                    {
                        "month": "2025-04",
                        "total": 3.0,
                        "paid_at": "2025-04-20T14:33:00"
                    }
                ]
            }
        }
    }
})
def get_paid_bills():
    subscriber_no = get_jwt_identity()
    bills = Bill.query.filter_by(subscriber_no=subscriber_no).all()
    result = [
        {
            "month": bill.month,
            "total": bill.total,
            "paid_at": bill.paid_at.isoformat()
        } for bill in bills
    ]
    return jsonify(result), 200

@billing_bp.route("/bill/details", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'Get detailed breakdown of usage and bill for a specific month',
    'security': [{"Bearer": []}],
    'parameters': [
        {'name': 'month', 'in': 'query', 'type': 'string', 'required': True, 'description': 'Month in YYYY-MM format'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'required': False, 'description': 'Page number'},
        {'name': 'page_size', 'in': 'query', 'type': 'integer', 'required': False, 'description': 'Number of items per page'},
    ],
    'responses': {
        200: {
            'description': 'Detailed bill info (paginated)',
        }
    }
})
def get_bill_details():
    subscriber_no = get_jwt_identity()
    month = request.args.get("month")

    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size

    all_usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()
    total_items = len(all_usages)
    total_pages = (total_items + page_size - 1) // page_size
    paginated_usages = all_usages[offset:offset + page_size]

    phone_amount = sum(u.amount for u in all_usages if u.type == "phone")
    internet_amount = sum(u.amount for u in all_usages if u.type == "internet")
    phone_minutes = phone_amount * 10
    internet_mb = internet_amount

    total = 0
    if phone_minutes > 1000:
        total += ((phone_minutes - 1000) // 1000) * 10
    if internet_mb > 0:
        total += 50
        if internet_mb > 20000:
            total += ((internet_mb - 20000) // 10000) * 10

    bill = Bill.query.filter_by(subscriber_no=subscriber_no, month=month).first()
    paid = bool(bill)

    return jsonify({
        "month": month,
        "paid": paid,
        "total": total,
        "details": {
            "items": [
                {"type": u.type, "amount": u.amount} for u in paginated_usages
            ],
            "current_page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }), 200
