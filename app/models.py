# app/models.py  

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean  
from sqlalchemy.dialects.postgresql import UUID  
from sqlalchemy.ext.declarative import declarative_base  
import uuid  
from datetime import datetime  

Base = declarative_base()  

class Business(Base):
    __tablename__ = "businesses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    qr_code = Column(String(512), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(Boolean, default=False)

class PunchCard(Base):  
    __tablename__ = "punchcards"  
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    business_id = Column(UUID, ForeignKey("businesses.id"))  
    required_punches = Column(Integer, nullable=False)  
    punches_achieved = Column(Integer, default=0)  # Tracks progress
    reward = Column(String(255), nullable=False)  
    expires_in_days = Column(Integer)  
    created_at = Column(DateTime, default=datetime.utcnow)  

class Visit(Base):
    __tablename__ = "visits"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID, ForeignKey("customers.id"), nullable=False)
    pos_transaction_id = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String(100))