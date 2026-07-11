from sqlalchemy import Sequence

from extensions import db


ylff_object_id_seq = Sequence("ylff_objects_id_seq")


class YLFFObject(db.Model):
    __tablename__ = "ylff_objects"

    id = db.Column(
        db.Integer,
        ylff_object_id_seq,
        server_default=ylff_object_id_seq.next_value(),
        primary_key=True,
    )

    reference = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
    )

    name = db.Column(
        db.String(255),
        nullable=False,
    )

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    locator = db.Column(
        db.String(20),
        nullable=True,
    )

    description = db.Column(db.Text)

    image_url = db.Column(
        db.Text,
        nullable=True,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
    )

    status = db.Column(
        db.String(20),
        default="active",
        nullable=False,
    )

    included_in_reference = db.Column(
        db.String(20),
        nullable=True,
    )

    included_until = db.Column(
        db.Date,
        nullable=True,
    )