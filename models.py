from app import db
from datetime import datetime


class EmployeeSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(200), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)