from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy import JSON
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .video_star_relationship import VideoStarRelationship

class Video(Base):
    __tablename__ = 'videos'

    number = Column(String(50), primary_key=True)
    title = Column(Text)
    keywords = Column(JSON)
    release_date = Column(Date)
    length = Column(Integer)
    series = Column(Text)
    outline = Column(Text)
    director = Column(Text)
    stars = relationship('Star', secondary=VideoStarRelationship)

    def __repr__(self) -> str:
        return f'<video {self.number}>'
