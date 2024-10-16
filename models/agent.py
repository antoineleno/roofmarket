#!/usr/bin/python3
"""Agent module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Agent(BaseModel, Base):
    """Mapping class for agent table"""

    __tablename__ = "agent"

    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    license_number = Column(String(60), nullable=False)
    experience_years = Column(String(15), nullable=False)

    user = relationship("User", back_populates="agent")
