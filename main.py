"""
Main entry point for the Mobile Billing API.
"""

import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, jwt, swagger
from app.routes.auth import auth_bp
from app.routes.usage import usage_bp
from app.routes.calculatebill import bill_bp
from app.routes.billing import billing_bp
from flask import jsonify

# Load environment variables from .env
load_dotenv()

# Flask App Initialization
app = Flask(__name__)

# Configuration from .env (fallback to sqlite if env missing)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://billinguser:mc6BRfIRg4VPXkb11eR6ezCNYZV5BIAS@dpg-d02fk4euk2gs73eec590-a.frankfurt-postgres.render.com:5432/billingdb_5gyy")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret")
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config['SWAGGER'] = {
    "title": "Mobile Billing API",
    "uiversion": 3,
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [{"Bearer": []}]
}

from app.models.usage import Usage

@app.route("/debug/usages")
def debug_usages():
    return jsonify([{
        "subscriber_no": u.subscriber_no,
        "month": u.month,
        "type": u.type,
        "amount": u.amount
    } for u in Usage.query.all()])

# Initialize extensions
db.init_app(app)
jwt.init_app(app)
swagger.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
app.register_blueprint(usage_bp, url_prefix="/api/v1/usage")
app.register_blueprint(bill_bp, url_prefix="/api/v1")  # calculate-bill için doğru
app.register_blueprint(billing_bp, url_prefix="/api/v1/pay-bill")

print("✅ Connecting to:", app.config['SQLALCHEMY_DATABASE_URI'])

# For local dev server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Bu satır sadece ilk çalıştırmada tabloyu oluşturur
    app.run(debug=True)
