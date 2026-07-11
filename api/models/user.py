from datetime import datetime

from sqlalchemy import Sequence

from extensions import db


user_id_seq = Sequence("users_id_seq")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        user_id_seq,
        server_default=user_id_seq.next_value(),
        primary_key=True,
    )

    email = db.Column(db.String(255), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(255))

    last_name = db.Column(db.String(255))

    is_admin = db.Column(db.Boolean, default=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
