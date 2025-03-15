from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from db.engine import Base


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
