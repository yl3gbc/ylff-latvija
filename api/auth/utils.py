import jwt
from flask import current_app, request

from extensions import db
from models import User


def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, {"error": "Missing authorization header"}, 401

    if not auth_header.startswith("Bearer "):
        return None, {"error": "Invalid authorization header"}, 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
        )

        user = db.session.get(User, payload["user_id"])

        if not user:
            return None, {"error": "User not found"}, 404

        if not user.is_active:
            return None, {"error": "User is inactive"}, 403

        return user, None, None

    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}, 401

    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}, 401
