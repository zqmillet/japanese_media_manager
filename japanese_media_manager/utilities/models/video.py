from sqlalchemy import Column, String, Text, Date, JSON

from .base import Base

class Video(Base):
    __tablename__ = 'videos'

    number = Column(String(50), primary_key=True)
    title = Column(Text)
    keywords = Column(JSON)
    release_date = Column(Date)
    length = Column(JSON)
    series = Column(Text)
    outline = Column(Text)
    director = Column(Text)
