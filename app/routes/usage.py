from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.usage_service import add_usage_record, get_usages_for_subscriber

usage_bp = Blueprint("usage", __name__)

@usage_bp.route("", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Usage'],
    'description': 'Add a usage record (each phone = 10 mins, each internet = 1 MB)',
    'security': [{"Bearer": []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'month': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['phone', 'internet']},
                    'amount': {'type': 'integer', 'default': 1}
                },
                'required': ['month', 'type']
            }
        }
    ],
    'responses': {
        200: {'description': 'Usage added successfully'},
        400: {'description': 'Invalid type'},
        401: {'description': 'Unauthorized'}
    }
})
def add_usage():
    data = request.get_json()
    usage_type = data.get("type")
    amount = data.get("amount", 1)

    if usage_type not in ["phone", "internet"]:
        return jsonify({"error": "Invalid usage type"}), 400

    subscriber_no = get_jwt_identity()
    month = data.get("month")

    add_usage_record(subscriber_no, month, usage_type, amount)

    return jsonify({"message": "Usage added"}), 200

@usage_bp.route("", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Usage'],
    'description': 'List all usage records for the current subscriber',
    'security': [{"Bearer": []}],
    'responses': {
        200: {
            'description': 'List of usage entries',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'month': {'type': 'string'},
                        'type': {'type': 'string'},
                        'amount': {'type': 'integer'}
                    }
                }
            }
        },
        401: {'description': 'Unauthorized'}
    }
})
def list_usage():
    subscriber_no = get_jwt_identity()
    usages = get_usages_for_subscriber(subscriber_no)

    result = [
        {
            "month": u.month,
            "type": u.type,
            "amount": u.amount
        } for u in usages
    ]

    return jsonify(result), 200
