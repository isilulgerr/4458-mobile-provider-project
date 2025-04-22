from app.extensions import db

class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_no = db.Column(db.String(20), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # phone / internet
    amount = db.Column(db.Integer, default=1)
