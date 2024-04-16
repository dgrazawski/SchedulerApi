from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Subject(db.Model):
    __tablename__='subjects'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_name = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    lab_hours = db.Column(db.Integer, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Schedule {self.subject_name}>'