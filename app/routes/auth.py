from flask import Blueprint, request, jsonify
from app.db import db
from app.models.users import User
from app.models.accounts import Account
from app.utils.auth import generate_token, hash_password, check_password
from datetime import datetime
import random

auth_bp = Blueprint("auth", __name__)

# Helper untuk generate account number unik
def generate_unique_account_number():
    today = datetime.utcnow().strftime("%d%m%y")
    while True:
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        account_number = f"{today}-{random_digits}"
        if not Account.query.filter_by(account_number=account_number).first():
            return account_number

# POST /register - Register user baru + akun otomatis
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Semua field wajib diisi"}), 400

    # Cek apakah email atau username sudah terdaftar
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username atau email sudah digunakan"}), 400

    # Hash password
    hashed_pw = hash_password(password)
    new_user = User(username=username, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    # Buat akun bank otomatis setelah registrasi
    account_number = generate_unique_account_number()
    new_account = Account(
        account_type='savings',
        account_number=account_number,
        user_id=new_user.id,  # Menghubungkan akun dengan user
        balance=0.0
    )
    db.session.add(new_account)
    db.session.commit()

    return jsonify({
        "message": "User berhasil dibuat",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        },
        "account": {
            "account_number": new_account.account_number,
            "balance": new_account.balance
        }
    }), 201

# POST /login - Login dan mendapatkan token JWT
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({"error": "Email atau password salah"}), 401

    token = generate_token(user.id)
    return jsonify({"token": token}), 200
