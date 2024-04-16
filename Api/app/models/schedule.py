from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Schedule(db.Model):
    __tablename__='schedules'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_name = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    is_cyclic = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Schedule {self.schedule_name}>'