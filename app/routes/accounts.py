from flask import Blueprint, request, jsonify
from app.db import db
from app.models.accounts import Account
from app.utils.auth import verify_token
from app.models.users import User

account_bp = Blueprint("accounts", __name__)

def get_user_id_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return verify_token(token)

@account_bp.route("", methods=["POST"])
def create_account():
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    account_type = data.get("account_type")
    account_number = data.get("account_number")

    if not all([account_type, account_number]):
        return jsonify({"error": "Semua field wajib diisi"}), 400

    account = Account(user_id=user_id, account_type=account_type, account_number=account_number)
    db.session.add(account)
    db.session.commit()
    return jsonify({"message": "Akun berhasil dibuat", "account_id": account.id}), 201

@account_bp.route("", methods=["GET"])
def list_accounts():
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": a.id,
        "account_type": a.account_type,
        "account_number": a.account_number,
        "balance": float(a.balance)
    } for a in accounts])

@account_bp.route("/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    account = Account.query.get_or_404(account_id)
    if account.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.json
    account.account_type = data.get("account_type", account.account_type)
    db.session.commit()
    return jsonify({"message": "Akun diperbarui"})

@account_bp.route("/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    account = Account.query.get_or_404(account_id)
    if account.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Akun berhasil dihapus"})
