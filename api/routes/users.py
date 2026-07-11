from flask import Blueprint

from models import User


users_bp = Blueprint("users", __name__)


@users_bp.route("/users")
def users():
    all_users = User.query.all()

    return {
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            }
            for user in all_users
        ]
    }
