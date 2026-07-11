from flask import Blueprint

from auth.decorators import admin_required
from extensions import db
from models import User


admin_deactivate_bp = Blueprint(
    "admin_deactivate",
    __name__,
    url_prefix="/admin/users",
)


@admin_deactivate_bp.route("/<int:user_id>/deactivate", methods=["POST"])
@admin_required
def deactivate_user(current_user, user_id):
    user = db.session.get(User, user_id)

    if not user:
        return {
            "error": "User not found",
        }, 404

    if user.id == current_user.id:
        return {
            "error": "You cannot deactivate yourself",
        }, 400

    user.is_active = False

    db.session.commit()

    return {
        "message": "User deactivated",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
        },
    }
