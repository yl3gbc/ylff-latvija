from flask import Blueprint

from models.object import YLFFObject


object_detail_bp = Blueprint(
    "object_detail",
    __name__,
    url_prefix="/objects",
)


@object_detail_bp.route("/<reference>", methods=["GET"])
def object_detail(reference):

    item = YLFFObject.query.filter_by(
        reference=reference
    ).first()

    if not item:
        return {
            "error": "Object not found",
        }, 404

    return {
        "object": {
            "id": item.id,
            "reference": item.reference,
            "name": item.name,
            "description": item.description,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "status": item.status,
            "included_in_reference": item.included_in_reference,
            "included_until": (
                item.included_until.isoformat()
                if item.included_until
                else None
            ),
        }
    }
