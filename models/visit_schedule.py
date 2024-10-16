#!/usr/bin/python3
"""Visit schelduling module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey, DATE
from sqlalchemy.orm import relationship
import os


class Visit_schedule(BaseModel, Base):
    """Mapping class for visit_schedule table"""

    __tablename__ = "visit_schedule"
    schedule_date = Column(DATE, nullable=True)
    schedule_time = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    property_id = Column(String(60), ForeignKey('property.id'), nullable=False)


    user = relationship("User", back_populates="schedules")
    property3 = relationship("Property", back_populates="schedules")
