from flask import Blueprint, request, jsonify
from app.db import db
from app.models.users import User
from app.utils.auth import generate_token, hash_password, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Semua field wajib diisi"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username atau email sudah digunakan"}), 400

    hashed_pw = hash_password(password)
    new_user = User(username=username, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User berhasil dibuat"}), 201

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
