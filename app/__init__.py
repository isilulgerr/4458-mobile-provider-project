from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config 

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    from app.routes.usage import usage_bp
    from app.routes.billing import billing_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(usage_bp, url_prefix="/api/v1/usage")
    app.register_blueprint(billing_bp, url_prefix="/api/v1/pay-bill")

    return app
