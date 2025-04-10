from flask import Flask
from app.config import Config
from app.db import init_db
from app.routes import auth, users, accounts, transactions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth.auth_bp, url_prefix="/auth")
    app.register_blueprint(users.user_bp, url_prefix="/users") 
    app.register_blueprint(accounts.account_bp, url_prefix="/accounts")
    app.register_blueprint(transactions.transaction_bp, url_prefix="/transactions")

    return app
