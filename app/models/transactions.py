from datetime import datetime
from app.db import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, or transfer
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Menghubungkan dengan Account (menggunakan account_number)
    account_number = db.Column(db.String(15), db.ForeignKey('accounts.account_number'), nullable=False)
    user_id = db.Column(db.String(4), db.ForeignKey('users.user_id'), nullable=False)  # Menghubungkan dengan user_id

    date_transaction = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke Account dan User
    account = db.relationship("Account", backref="transactions", lazy=True)
    user = db.relationship("User", backref="transactions", lazy=True)

    def to_dict(self):
        """Convert object to dictionary format."""
        return {
            "id": self.id,
            "transaction_type": self.transaction_type,
            "amount": str(self.amount),  # Mengubah amount menjadi string
            "balance": str(self.balance),  # Mengubah balance menjadi string
            "account_number": self.account_number,
            "user_id": self.user_id,
            "date_transaction": self.date_transaction.isoformat() if self.date_transaction else None
        }

    def __init__(self, transaction_type, amount, balance, account_number, user_id, date_transaction=None):
        """Initialize a new Transaction."""
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance
        self.account_number = account_number
        self.user_id = user_id
        self.date_transaction = date_transaction or datetime.utcnow()

    def __repr__(self):
        return f"<Transaction {self.id} - {self.transaction_type} - {self.amount}>"
