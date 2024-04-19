from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class NonCyclicTile(db.Model):
    __tablename__='noncyclictiles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day = db.Column(db.String(20), nullable=False)
    meeting_id = db.Column(UUID(as_uuid=True), db.ForeignKey('meetings.id', ondelete='CASCADE'), nullable=False)
    allocation_id = db.Column(UUID(as_uuid=True), db.ForeignKey('allocations.id', ondelete='CASCADE'), nullable=False)
    schedule_id = db.Column(UUID(as_uuid=True), db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Tile {self.day}>'