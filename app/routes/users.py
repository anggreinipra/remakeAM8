from flask import Blueprint, request, jsonify
from app.models.users import User
from app.utils.auth import hash_password, verify_token
from app.db import db

user_bp = Blueprint("users", __name__)

def get_current_user(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    user_id = verify_token(token)
    return User.query.get(user_id)

# GET /users/me
@user_bp.route("/me", methods=["GET"])
def get_profile():
    user = get_current_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    })

# PUT /users/me
@user_bp.route("/me", methods=["PUT"])
def update_profile():
    user = get_current_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    if data.get("password"):
        user.password_hash = hash_password(data["password"])

    db.session.commit()
    return jsonify({"message": "Profil berhasil diperbarui"})
