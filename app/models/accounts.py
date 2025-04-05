from datetime import datetime
from app.db import db

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions_from = db.relationship("Transaction", foreign_keys='Transaction.from_account_id', backref="from_account", lazy=True)
    transactions_to = db.relationship("Transaction", foreign_keys='Transaction.to_account_id', backref="to_account", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_type": self.account_type,
            "account_number": self.account_number,
            "balance": float(self.balance),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
