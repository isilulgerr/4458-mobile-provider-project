from app.extensions import db
from app.models.subscriber import Subscriber
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify
from datetime import timedelta

def register_user(data):
    subscriber_no = data.get("subscriber_no")
    name = data.get("name")
    password = data.get("password")

    if not subscriber_no or not name or not password:
        return jsonify({"error": "Missing subscriber_no, name, or password"}), 400

    existing = Subscriber.query.filter_by(subscriber_no=subscriber_no).first()
    if existing:
        return jsonify({"error": "Subscriber already exists"}), 400

    hashed = generate_password_hash(password)
    new_subscriber = Subscriber(
        subscriber_no=subscriber_no,
        name=name,
        password_hash=hashed
    )
    db.session.add(new_subscriber)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


def login_user(data):
    subscriber_no = data.get("subscriber_no")
    password = data.get("password")

    if not subscriber_no or not password:
        return jsonify({"error": "Missing subscriber_no or password"}), 400

    user = Subscriber.query.filter_by(subscriber_no=subscriber_no).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=subscriber_no, expires_delta=timedelta(days=1))
    return jsonify({"access_token": access_token}), 200
