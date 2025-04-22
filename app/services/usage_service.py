from app.models.usage import Usage
from app.extensions import db

def add_usage_record(subscriber_no, month, usage_type, amount):
    usage = Usage(
        subscriber_no=subscriber_no,
        month=month,
        type=usage_type,
        amount=amount
    )
    db.session.add(usage)
    db.session.commit()
    return usage

def get_usages_for_subscriber(subscriber_no):
    return Usage.query.filter_by(subscriber_no=subscriber_no).all()
