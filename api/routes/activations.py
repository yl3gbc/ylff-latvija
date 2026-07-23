from datetime import datetime

from flask import Blueprint, request

from auth.decorators import admin_required
from extensions import db
from models.activation import Activation
from models.object import YLFFObject


activations_bp = Blueprint(
    "activations",
    __name__,
    url_prefix="/activations",
)


@activations_bp.route("", methods=["GET"])
def list_activations():
    activations = Activation.query.order_by(
        Activation.created_at.desc()
    ).all()

    return {
        "activations": [
            {
                "id": item.id,
                "callsign": item.callsign,
                "ylff_object_id": item.ylff_object_id,
                "qso_count": item.qso_count,
                "operators": item.operators,
                "activation_start": (
                    item.activation_start.isoformat()
                    if item.activation_start
                    else None
                ),
                "activation_end": (
                    item.activation_end.isoformat()
                    if item.activation_end
                    else None
                ),
                "created_at": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                ),
            }
            for item in activations
        ]
    }


@activations_bp.route("/create", methods=["POST"])
@admin_required
def create_activation(current_user):
    data = request.get_json()

    if not data:
        return {"error": "No JSON data"}, 400

    callsign = data.get("callsign")
    reference = data.get("reference")

    if not callsign or not reference:
        return {"error": "Callsign and reference required"}, 400

    ylff_object = YLFFObject.query.filter_by(
        reference=reference,
    ).first()

    if not ylff_object:
        return {"error": "Object not found"}, 404

    activation_start = None
    activation_end = None

    if data.get("activation_start"):
        activation_start = datetime.strptime(
            data.get("activation_start"),
            "%Y-%m-%d",
        ).date()

    if data.get("activation_end"):
        activation_end = datetime.strptime(
            data.get("activation_end"),
            "%Y-%m-%d",
        ).date()

    try:
        qso_count = int(data.get("qso_count") or 0)
    except (TypeError, ValueError):
        return {"error": "qso_count must be an integer"}, 400

    if qso_count < 0:
        return {"error": "qso_count cannot be negative"}, 400

    activation = Activation(
        callsign=callsign.upper(),
        ylff_object_id=ylff_object.id,
        qso_count=qso_count,
        activation_start=activation_start,
        activation_end=activation_end,
        operators=data.get("operators"),
        status=(
            "complete"
            if qso_count >= 100
            else "incomplete"
        ),
    )

    db.session.add(activation)
    db.session.commit()

    return {
        "message": "Activation created",
        "activation": {
            "id": activation.id,
            "callsign": activation.callsign,
            "reference": ylff_object.reference,
            "qso_count": activation.qso_count,
            "operators": activation.operators,
        },
    }, 201