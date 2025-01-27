# app/routers/analytics.py  

from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db  
from app.models import PunchCard, Visit, Customer 
from app.schemas import AnalyticsResponse  
from app.utils.redis_client import get_cache  
from typing import List, Dict  
import json  

router = APIRouter()  

@router.get("/analytics/redemption-rate")  
async def get_redemption_rate(  
    db: Session = Depends(get_db)  
):  
    total_punchcards = db.query(PunchCard).count()  
    redeemed = db.query(PunchCard).filter(  
        PunchCard.punches_achieved >= PunchCard.required_punches  # Correct logic
    ).count()  

    rate = (redeemed / total_punchcards) * 100 if total_punchcards > 0 else 0  
    return {"redemption_rate": round(rate, 2)}

@router.get("/analytics/avg-punches", response_model=AnalyticsResponse)
async def get_avg_punches_per_customer(
    db: Session = Depends(get_db)
):
    # Calculate total punches (visits) and total customers
    total_punches = db.query(func.count(Visit.id)).scalar()  # Total visits
    total_customers = db.query(func.count(Customer.id)).scalar()  # Total customers

    # Calculate average punches per customer
    avg_punches = total_punches / total_customers if total_customers > 0 else 0

    # Return only the required field
    return {"avg_punches_per_customer": round(avg_punches, 2)}