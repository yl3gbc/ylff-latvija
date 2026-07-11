from flask import Blueprint, request

from auth.decorators import admin_required
from extensions import db
from models.object import YLFFObject


objects_bp = Blueprint("objects", __name__, url_prefix="/objects")


@objects_bp.route("", methods=["GET"])
def list_objects():
    objects = YLFFObject.query.order_by(YLFFObject.reference.asc()).all()

    return {
        "objects": [
            {
                "id": item.id,
                "reference": item.reference,
                "name": item.name,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "description": item.description,
                "is_active": item.is_active,
            }
            for item in objects
        ]
    }


@objects_bp.route("/create", methods=["POST"])
@admin_required
def create_object(current_user):
    data = request.get_json()

    if not data:
        return {"error": "No JSON data"}, 400

    reference = data.get("reference")
    name = data.get("name")

    if not reference or not name:
        return {"error": "Reference and name required"}, 400

    existing_object = YLFFObject.query.filter_by(reference=reference).first()

    if existing_object:
        return {"error": "Object already exists"}, 409

    item = YLFFObject(
        reference=reference,
        name=name,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        description=data.get("description"),
        is_active=data.get("is_active", True),
    )

    db.session.add(item)
    db.session.commit()

    return {
        "message": "Object created",
        "object": {
            "id": item.id,
            "reference": item.reference,
            "name": item.name,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "is_active": item.is_active,
        },
    }, 201


@objects_bp.route("/<int:object_id>", methods=["GET"])
def object_detail(object_id):
    item = db.session.get(YLFFObject, object_id)

    if not item:
        return {"error": "Object not found"}, 404

    return {
        "id": item.id,
        "reference": item.reference,
        "name": item.name,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "description": item.description,
        "is_active": item.is_active,
    }
