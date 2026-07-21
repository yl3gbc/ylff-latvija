from datetime import datetime

from sqlalchemy import Sequence, UniqueConstraint

from extensions import db


diploma_record_id_seq = Sequence("diploma_records_id_seq")


class DiplomaRecord(db.Model):
    __tablename__ = "diploma_records"

    __table_args__ = (
        UniqueConstraint(
            "callsign",
            "recipient_type",
            "diploma_code",
            name="uq_diploma_records_callsign_type_code",
        ),
    )

    id = db.Column(
        db.Integer,
        diploma_record_id_seq,
        server_default=diploma_record_id_seq.next_value(),
        primary_key=True,
    )

    callsign = db.Column(
        db.String(50),
        nullable=False,
    )

    recipient_type = db.Column(
        db.String(20),
        nullable=False,
    )

    is_swl = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    diploma_code = db.Column(
        db.String(50),
        nullable=False,
    )

    qualifying_count = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    status = db.Column(
        db.String(30),
        default="eligible",
        nullable=False,
    )

    country_code = db.Column(db.String(10))

    region_code = db.Column(db.String(30))

    requested_at = db.Column(db.DateTime)

    approved_at = db.Column(db.DateTime)

    issued_at = db.Column(db.DateTime)

    approved_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )

    certificate_number = db.Column(
        db.String(50),
        unique=True,
    )

    pdf_path = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
