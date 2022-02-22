from sqlalchemy import Column, String, ForeignKey, Table

from .base import Base

VideoStarRelationship = Table(
    'video_star_relationships',
    Base.metadata,
    Column('video_number', String(50), ForeignKey('videos.number'), nullable=True, primary_key=True),
    Column('star_name', String(50), ForeignKey('stars.name'), nullable=True, primary_key=True),
)
