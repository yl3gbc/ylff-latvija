from datetime import datetime

from sqlalchemy import Sequence

from extensions import db


media_file_id_seq = Sequence("media_files_id_seq")


class MediaFile(db.Model):
    __tablename__ = "media_files"

    id = db.Column(
        db.Integer,
        media_file_id_seq,
        server_default=media_file_id_seq.next_value(),
        primary_key=True,
    )

    filename = db.Column(db.String(255), nullable=False)

    original_filename = db.Column(db.String(255), nullable=False)

    file_size = db.Column(db.Integer)

    mime_type = db.Column(db.String(255))

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )
