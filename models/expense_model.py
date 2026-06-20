from extensions import db
from datetime import datetime

class Expense(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)

    category = db.Column(db.String(50))

    description = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )