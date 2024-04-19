from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Allocation(db.Model):
    __tablename__='allocations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lecturer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lecturers.id', ondelete='CASCADE'), nullable=False)
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(UUID(as_uuid=True), db.ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    schedule_id = db.Column(UUID(as_uuid=True), db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    
    def __repr__(self):
        return f'<Allocation {self.id}>'