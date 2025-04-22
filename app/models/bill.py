from app.extensions import db

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_no = db.Column(db.String(20), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    total = db.Column(db.Float, nullable=False) 
    paid_at = db.Column(db.DateTime, nullable=False)
