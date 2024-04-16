from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Meeting(db.Model):
    __tablename__='meetings'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = db.Column(db.String(50), unique=True, nullable=False)
    end_date = db.Column(db.String(50), unique=True, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Schedule {self.start_date} {self.end_date}>'