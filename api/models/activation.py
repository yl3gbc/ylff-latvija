from datetime import datetime

from sqlalchemy import Sequence

from extensions import db


activation_id_seq = Sequence("activations_id_seq")


class Activation(db.Model):
    __tablename__ = "activations"

    id = db.Column(
        db.Integer,
        activation_id_seq,
        server_default=activation_id_seq.next_value(),
        primary_key=True,
    )

    callsign = db.Column(
        db.String(50),
        nullable=False,
    )

    ylff_object_id = db.Column(
        db.Integer,
        db.ForeignKey("ylff_objects.id"),
        nullable=False,
    )

    qso_count = db.Column(
        db.Integer,
        default=0,
    )

    activation_start = db.Column(db.Date)

    activation_end = db.Column(db.Date)

    operators = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        default="complete",
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )
