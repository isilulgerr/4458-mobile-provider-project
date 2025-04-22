from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.billing_service import calculate_total_bill

bill_bp = Blueprint("calculate_bill", __name__)

@bill_bp.route("/calculate-bill", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'Calculate monthly bill based on current usage',
    'security': [{"Bearer": []}],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'month': {'type': 'string'}
            },
            'required': ['month']
        }
    }],
    'responses': {
        200: {'description': 'Monthly bill total returned'},
        400: {'description': 'Missing or invalid data'},
        401: {'description': 'Unauthorized'}
    }
})
def calculate_bill():
    data = request.get_json()
    month = data.get("month")
    if not month:
        return jsonify({"error": "Month is required"}), 400

    subscriber_no = get_jwt_identity()
    response, status = calculate_total_bill(subscriber_no, month)
    return jsonify(response), status
