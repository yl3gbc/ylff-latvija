from extensions import db


class QSORecord(db.Model):
    __tablename__ = "qso_records"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    activation_id = db.Column(
        db.Integer,
        db.ForeignKey("activations.id"),
        nullable=False,
    )

    ylff_object_id = db.Column(
        db.Integer,
        db.ForeignKey("ylff_objects.id"),
        nullable=False,
    )

    worked_call = db.Column(
        db.String(50),
        nullable=False,
    )

    qso_date = db.Column(db.Date)

    band = db.Column(db.String(20))

    mode = db.Column(db.String(20))
