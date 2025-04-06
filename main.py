from flask import Flask
from app.routes import routes 
from app.routes.auth import auth_bp
from app.routes.users import user_bp
from app.routes.transactions import transaction_bp
from app.routes.accounts import account_bp
import logging
import os
from dotenv import load_dotenv
load_dotenv() 


def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config.from_envvar('FLASK_CONFIG', silent=True)

    # Register blueprints
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(account_bp, url_prefix='/accounts')

    # Setup basic logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Flask app created and blueprints registered.')

    # Error handling: custom 404 page
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404

    # Error handling: general internal server error
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return {'message': 'Internal server error'}, 500

    return app

if __name__ == "__main__":
    # Ensure the app runs only in the development environment
    app = create_app()
    app.run(debug=True)
