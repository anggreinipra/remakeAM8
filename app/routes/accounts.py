import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.db import db
from app.models.accounts import Account
from app.models.users import User
from app.utils.auth import verify_token

account_bp = Blueprint("accounts", __name__)

def get_user_id_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return verify_token(token)

# Helper untuk generate account number unik sesuai dengan format yang diinginkan
def generate_unique_account_number():
    today_str = datetime.now().strftime("%d%m%y")
    while True:
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        account_number = f"{today_str}-{random_digits}"
        # Cek apakah account_number sudah ada
        if not Account.query.filter_by(account_number=account_number).first():
            return account_number

@account_bp.route("", methods=["POST"])
def create_account():
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json or {}

    account_type = data.get("account_type", "savings")

    # Generate unique account number
    account_number = generate_unique_account_number()

    # Retrieve the user and create the account
    user = User.query.get_or_404(user_id)
    account = Account(
        user_id=user.id,
        account_type=account_type,
        account_number=account_number
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({
        "message": "Account successfully created",
        "account_id": account.id,
        "account_number": account.account_number
    }), 201

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

    return jsonify({"message": "Account updated successfully"})

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

    return jsonify({"message": "Account deleted successfully"})
