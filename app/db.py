from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models import User, Account, Transaction
