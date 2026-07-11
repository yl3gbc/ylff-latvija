from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from auth.decorators import admin_required
from extensions import db
from models import User


admin_users_bp = Blueprint(
    "admin_users",
    __name__,
    url_prefix="/admin/users",
)


@admin_users_bp.route("/create", methods=["POST"])
@admin_required
def create_user(current_user):
    data = request.get_json()

    if not data:
        return {
            "error": "No JSON data",
        }, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "error": "Email and password required",
        }, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {
            "error": "User already exists",
        }, 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=data.get("is_admin", False),
        is_active=True,
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User created",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
        },
    }, 201
