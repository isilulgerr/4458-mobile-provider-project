from app.models.bill import Bill
from app.models.usage import Usage
from app.extensions import db
from datetime import datetime
from flask import jsonify

def pay_bill_logic(subscriber_no, month):
    bill = Bill.query.filter_by(subscriber_no=subscriber_no, month=month).first()
    usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()
    if not usages:
        return jsonify({"error": "No usage found for this month"}), 400

    phone_minutes = sum(u.amount for u in usages if u.type == "phone") * 10
    internet_mb = sum(u.amount for u in usages if u.type == "internet")

    total = 0
    if phone_minutes > 1000:
        total += ((phone_minutes - 1000) // 1000) * 10
    if internet_mb > 0:
        total += 50
        if internet_mb > 20000:
            total += ((internet_mb - 20000) // 10000) * 10

    now = datetime.utcnow()

    if bill:
        remaining = total - bill.total
        if remaining > 0:
            bill.total += remaining
            db.session.commit()
            return jsonify({"message": "Remaining bill amount paid", "new_total": bill.total}), 200
        else:
            return jsonify({"message": "Already fully paid", "total": bill.total}), 200

    new_bill = Bill(subscriber_no=subscriber_no, month=month, total=total, paid_at=now)
    db.session.add(new_bill)
    db.session.commit()

    return jsonify({"message": "Bill paid successfully", "total": total}), 200

def calculate_total_bill(subscriber_no, month):
    usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()
    phone_minutes = sum(u.amount for u in usages if u.type == "phone") * 10
    internet_mb = sum(u.amount for u in usages if u.type == "internet")

    total = 0

    if phone_minutes > 1000:
        total += ((phone_minutes - 1000) // 1000) * 10

    if internet_mb > 0:
        total += 50
        if internet_mb > 20000:
            extra_mb = internet_mb - 20000
            total += (extra_mb // 10000) * 10

    return {
        "total": total,
        "phone_minutes": phone_minutes,
        "internet_mb": internet_mb
    }

