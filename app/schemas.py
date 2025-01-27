# app/schemas.py  

from pydantic import BaseModel, Field, EmailStr  
from typing import Optional, List 
import uuid  

class CustomerCreate(BaseModel):  
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")  # E.164 format  
    email: Optional[EmailStr] = None  
    qr_code: Optional[str] = None  

class PunchCardCreate(BaseModel):  
    business_id: uuid.UUID  
    required_punches: int = Field(..., ge=1)  # Minimum 1 punch  
    reward: str  
    expires_in_days: Optional[int] = Field(None, ge=1)  

class VisitCreate(BaseModel):  
    customer_id: uuid.UUID  
    pos_transaction_id: Optional[str] = None  
    location: Optional[str] = None  

class AnalyticsResponse(BaseModel):
    top_customers: Optional[List[dict]] = None  # Make this optional
    redemption_rate: Optional[float] = None  # Make this optional
    avg_punches_per_customer: float  # Required field

class BusinessCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)