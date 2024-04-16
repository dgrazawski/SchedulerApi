from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lecturer_name = db.Column(db.String(50), nullable=False)
    lecturer_lastname = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Lecturer {self.lecturer_lastname}>'