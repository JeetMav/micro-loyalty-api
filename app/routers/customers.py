# app/routers/customers.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Customer
from app.schemas import CustomerCreate
from app.core.security import create_jwt, verify_token
import uuid

router = APIRouter()

# Use a simple Bearer token flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/register")  # <-- This should match your token endpoint

@router.post("/register", status_code=201)
async def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    # Check for duplicate phone/email
    existing = db.query(Customer).filter(
        (Customer.phone == customer.phone) |
        (Customer.email == customer.email)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Customer already exists")

    # Save new customer
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()

    # Generate and return a JWT token
    token = create_jwt(str(new_customer.id))
    return {
        "id": str(new_customer.id),
        "token": token  # Return the token
    }

@router.get("/customers/{customer_id}")
async def get_customer(
    customer_id: uuid.UUID,
    token: str = Depends(oauth2_scheme),  # Require token
    db: Session = Depends(get_db)
):
    # Validate token
    verify_token(token)  # Raises 401 if invalid

    # Fetch customer details
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer