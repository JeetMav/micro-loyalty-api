# app/routers/businesses.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Business
import uuid

router = APIRouter()

@router.post("/businesses")
def create_business(
    name: str,  # Add proper Pydantic schema if needed
    db: Session = Depends(get_db)
):
    new_business = Business(name=name)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return {"id": str(new_business.id), "name": new_business.name}