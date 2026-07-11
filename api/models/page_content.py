from datetime import datetime

from extensions import db


class PageContent(db.Model):
    __tablename__ = "page_contents"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    slug = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )

    title_lv = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    title_ru = db.Column(db.String(255))

    content_lv = db.Column(db.Text)
    content_en = db.Column(db.Text)
    content_ru = db.Column(db.Text)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
