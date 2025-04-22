from app.extensions import db

class Subscriber(db.Model):
    subscriber_no = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
