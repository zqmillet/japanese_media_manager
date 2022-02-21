from sqlalchemy import Column, String, Text, Date

from .base import Base

class Star(Base):
    __tablename__ = 'stars'

    name = Column(String(50), primary_key=True)
