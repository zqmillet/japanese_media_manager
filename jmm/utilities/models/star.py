from sqlalchemy import Column, String, BLOB
from sqlalchemy.orm import relationship

from .base import Base
from .video_star_relationship import VideoStarRelationship

class Star(Base):
    __tablename__ = 'stars'

    name = Column(String(50), primary_key=True)
    avatar = Column(BLOB)
    videos = relationship('Video', secondary=VideoStarRelationship, overlaps='stars')

    def __repr__(self) -> str:
        return f'<star {self.name}>'
