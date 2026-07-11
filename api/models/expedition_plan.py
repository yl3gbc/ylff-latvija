from datetime import datetime

from extensions import db


class ExpeditionPlan(db.Model):
    __tablename__ = "expedition_plans"

    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(50), nullable=False)
    operators = db.Column(db.String(255))
    ylff_reference = db.Column(db.String(50), nullable=False)
    planned_date = db.Column(db.Date)
    planned_time_utc = db.Column(db.String(20))
    mode = db.Column(db.String(50))
    whatsapp = db.Column(db.String(80))
    email = db.Column(db.String(255))
    notes = db.Column(db.Text)
    status = db.Column(db.String(30), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
