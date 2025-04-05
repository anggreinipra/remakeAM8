from datetime import datetime
from app.db import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(255), nullable=False)  # deposit, withdrawal, transfer
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": float(self.amount),
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
