from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions import Transaction
from app.models.accounts import Account
from app.db import db
from datetime import datetime

transaction_bp = Blueprint("transactions", __name__)

# ✅ CREATE TRANSACTION
@transaction_bp.route("", methods=["POST"])
@jwt_required()
def create_transaction():
    data = request.get_json()
    trans_type = data.get("type")
    from_account_number = data.get("from_account_number")
    to_account_number = data.get("to_account_number")
    amount = data.get("amount")
    description = data.get("description", "")

    if not trans_type or not amount:
        return jsonify({"error": "type and amount are required"}), 400

    if trans_type not in ["deposit", "withdrawal", "transfer"]:
        return jsonify({"error": "Invalid transaction type"}), 400

    user_id = get_jwt_identity()

    if trans_type == "deposit":
        to_account = Account.query.filter_by(account_number=to_account_number, user_id=user_id).first()
        if not to_account:
            return jsonify({"error": "Target account not found"}), 404
        to_account.balance += amount

    elif trans_type == "withdrawal":
        from_account = Account.query.filter_by(account_number=from_account_number, user_id=user_id).first()
        if not from_account or from_account.balance < amount:
            return jsonify({"error": "Insufficient balance or account not found"}), 400
        from_account.balance -= amount

    elif trans_type == "transfer":
        from_account = Account.query.filter_by(account_number=from_account_number, user_id=user_id).first()
        to_account = Account.query.filter_by(account_number=to_account_number).first()
        if not from_account or not to_account:
            return jsonify({"error": "Account not found"}), 404
        if from_account.balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400
        from_account.balance -= amount
        to_account.balance += amount

    # Membuat transaksi baru dan menyimpan ke database
    transaction = Transaction(
        from_account_number=from_account_number,
        to_account_number=to_account_number,
        amount=amount,
        type=trans_type,
        description=description
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction successful"}), 201

# ✅ GET ALL TRANSACTIONS (FILTER)
@transaction_bp.route("", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    account_numbers = [acc.account_number for acc in Account.query.filter_by(user_id=user_id).all()]
    transactions = Transaction.query.filter(
        (Transaction.from_account_number.in_(account_numbers)) |
        (Transaction.to_account_number.in_(account_numbers))
    ).all()

    return jsonify([
        {
            "id": t.id,
            "from_account_number": t.from_account_number,
            "to_account_number": t.to_account_number,
            "amount": float(t.amount),
            "type": t.type,
            "description": t.description,
            "created_at": t.created_at
        } for t in transactions
    ])

# ✅ GET SPECIFIC TRANSACTION
@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Pastikan user memiliki akses ke transaksi tersebut
    user_account_numbers = [acc.account_number for acc in Account.query.filter_by(user_id=user_id).all()]
    if transaction.from_account_number not in user_account_numbers and transaction.to_account_number not in user_account_numbers:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "id": transaction.id,
        "from_account_number": transaction.from_account_number,
        "to_account_number": transaction.to_account_number,
        "amount": float(transaction.amount),
        "type": transaction.type,
        "description": transaction.description,
        "created_at": transaction.created_at
    })
