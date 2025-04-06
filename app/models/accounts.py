from datetime import datetime
import random
from app.db import db

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(15), unique=True, nullable=False, default=lambda: Account.generate_account_number())
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    user_id = db.Column(db.String(4), db.ForeignKey('users.user_id'), nullable=False)  # Link ke user_id
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relasi ke User
    user = db.relationship("User", backref="accounts", lazy=True)

    @staticmethod
    def generate_account_number():
        """Generate account number in the format 'DDMMYY-XXXXXX'"""
        while True:
            date_str = datetime.now().strftime("%d%m%y")
            random_num = random.randint(100000, 999999)  # Generates a 6-digit random number
            account_number = f"{date_str}-{random_num}"

            # Cek apakah account number sudah ada
            if not Account.query.filter_by(account_number=account_number).first():
                return account_number

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "balance": str(self.balance), 
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
