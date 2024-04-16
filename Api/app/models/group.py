from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Group(db.Model):
    __tablename__='groups'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = db.Column(db.String(50), unique=True, nullable=False)
    group_size = db.Column(db.Integer, nullable=False)
    group_type = db.Column(db.Integer, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    schedule_id = db.Column(UUID(as_uuid=True), db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Group {self.group_name}>'