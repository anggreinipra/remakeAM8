from datetime import datetime
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
import random

from app.models.accounts import Account

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(4), unique=True, nullable=False, default=lambda: User.generate_user_id())
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relasi ke Account
    accounts = db.relationship("Account", backref="owner", cascade="all, delete-orphan", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def generate_user_id():
        """Generate a user_id in the format '0001', '0002', etc."""
        last_user = User.query.order_by(User.user_id.desc()).first()
        next_user_id = 1 if last_user is None else int(last_user.user_id) + 1
        return f"{next_user_id:04d}"
    
    @staticmethod
    def generate_account_number():
        """Generate an account number in the format 'DDMMYY-XXXXXX'"""
        while True:
            date_str = datetime.now().strftime("%d%m%y")
            random_num = random.randint(100000, 999999)
            account_number = f"{date_str}-{random_num}"

            # Cek apakah account number sudah ada
            if not Account.query.filter_by(account_number=account_number).first():
                return account_number
