#!/usr/bin/python3
"""payment module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Float, String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
import os


class Payment(BaseModel, Base):
    """Mapping class for payment table"""
    __tablename__ = "payment"
    amount = Column(Float, nullable=True)
    payment_method = Column(String(45), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    transaction_id = Column(String(60), ForeignKey('transaction.id'), nullable=False)

    transaction = relationship("Transaction", back_populates="payment")
