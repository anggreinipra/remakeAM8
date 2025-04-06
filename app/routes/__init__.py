from flask import Blueprint, jsonify

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to RevoBank API 👋",
        "status": "running"
    }), 200
