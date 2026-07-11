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

    activated_ids = {
        activation.ylff_object_id
        for activation in complete_activations
    }

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

        is_activated = item.id in activated_ids

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "id": item.id,
                    "reference": item.reference,
                    "name": item.name,
                    "description": item.description,
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
