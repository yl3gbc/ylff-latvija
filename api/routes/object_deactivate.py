from flask import Blueprint

from auth.decorators import admin_required
from extensions import db
from models.object import YLFFObject


object_deactivate_bp = Blueprint(
    "object_deactivate",
    __name__,
    url_prefix="/objects",
)


@object_deactivate_bp.route("/<int:object_id>/deactivate", methods=["POST"])
@admin_required
def deactivate_object(current_user, object_id):
    item = db.session.get(YLFFObject, object_id)

    if not item:
        return {
            "error": "Object not found",
        }, 404

    item.is_active = False

    db.session.commit()

    return {
        "message": "Object deactivated",
        "object": {
            "id": item.id,
            "reference": item.reference,
            "is_active": item.is_active,
        },
    }
