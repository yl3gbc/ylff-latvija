from datetime import date

from flask import Blueprint

from models.activation import Activation
from models.expedition_plan import ExpeditionPlan
from models.object import YLFFObject


object_geojson_bp = Blueprint(
    "object_geojson",
    __name__,
    url_prefix="/objects",
)


@object_geojson_bp.route("/geojson", methods=["GET"])
def objects_geojson():
    objects = YLFFObject.query.all()

    complete_activations = Activation.query.filter_by(
        status="complete",
    ).all()

    activations_by_object = {}

    for activation in complete_activations:
        activations_by_object.setdefault(
            activation.ylff_object_id,
            [],
        ).append(activation)

    approved_plans = ExpeditionPlan.query.filter_by(
        status="approved",
    ).all()

    plans_by_reference = {}

    for plan in approved_plans:
        plans_by_reference.setdefault(
            plan.ylff_reference,
            [],
        ).append(
            {
                "id": plan.id,
                "callsign": plan.callsign,
                "operators": plan.operators,
                "planned_date": plan.planned_date.isoformat() if plan.planned_date else None,
                "planned_time_utc": plan.planned_time_utc,
                "mode": plan.mode,
                "notes": plan.notes,
            }
        )

    features = []

    for item in objects:
        if item.latitude is None or item.longitude is None:
            continue

        plans = plans_by_reference.get(
            item.reference,
            [],
        )

        item_activations = activations_by_object.get(
            item.id,
            [],
        )

        latest_activation = (
            max(
                item_activations,
                key=lambda activation: (
                    activation.activation_start or date.min,
                    activation.id or 0,
                ),
            )
            if item_activations
            else None
        )

        total_qso = sum(
            activation.qso_count or 0
            for activation in item_activations
        )

        is_activated = bool(item_activations)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "id": item.id,
                    "reference": item.reference,
                    "name": item.name,
                    "description": item.description,
                    "image_url": item.image_url,
                    "total_qso": total_qso,
                    "last_activator_callsign": (
                        latest_activation.callsign
                        if latest_activation
                        else None
                    ),
                    "activation_count": len(item_activations),
                    "last_activation_date": (
                        latest_activation.activation_start.isoformat()
                        if latest_activation
                        and latest_activation.activation_start
                        else None
                    ),
                    "object_status": item.status,
                    "is_activated": is_activated,
                    "activation_status_text": "Aktivizēts" if is_activated else "Vēl nav aktivizēts",
                    "has_planned_expedition": bool(plans),
                    "planned_expeditions": plans,
                    "included_in_reference": item.included_in_reference,
                    "included_until": item.included_until.isoformat() if item.included_until else None,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        item.longitude,
                        item.latitude,
                    ],
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "features": features,
    }
