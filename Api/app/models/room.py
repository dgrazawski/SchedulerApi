from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Room(db.Model):
    __tablename__='rooms'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_size = db.Column(db.Integer, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Schedule {self.room_number}>'