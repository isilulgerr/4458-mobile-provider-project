from flask import Blueprint, request
from flasgger import swag_from
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'description': 'Register a new user',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'subscriber_no': {'type': 'string'},
                'password': {'type': 'string'}
            },
            'required': ['subscriber_no', 'password']
        }
    }],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Missing or already exists'}
    }
})
def register():
    data = request.get_json()
    return register_user(data)

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'description': 'Log in and get JWT token',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'subscriber_no': {'type': 'string'},
                'password': {'type': 'string'}
            },
            'required': ['subscriber_no', 'password']
        }
    }],
    'responses': {
        200: {'description': 'Access token returned'},
        400: {'description': 'Missing fields'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.get_json()
    return login_user(data)
