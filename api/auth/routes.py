from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, request, current_app
from werkzeug.security import check_password_hash

from models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"error": "No JSON data"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid credentials"}, 401

    if not check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    if not user.is_active:
        return {"error": "User is inactive"}, 403

    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "is_admin": user.is_admin,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }

    access_token = jwt.encode(
        token_payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
        },
    }
