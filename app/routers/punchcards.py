# app/routers/punchcards.py  

from fastapi import APIRouter, Depends, HTTPException  
from app.schemas import PunchCardCreate  
from app.db.session import get_db  
from sqlalchemy.orm import Session  
from app.models import PunchCard  
import uuid  

router = APIRouter()  

@router.post("/punchcards")  
def create_punchcard(  
    punchcard: PunchCardCreate,  
    db: Session = Depends(get_db)  
):  
    if punchcard.required_punches < 1:  
        raise HTTPException(  
            status_code=400,  
            detail="At least 1 punch required. Don’t be greedy."  
        )  
    
    # Save to DB
    db_punchcard = PunchCard(**punchcard.dict())
    db.add(db_punchcard)  
    db.commit()  
    db.refresh(db_punchcard)  
    return {"id": str(db_punchcard.id), "message": "Punch card created. Now go sell coffee."}

@router.post("/punchcards/{punchcard_id}/increment")  
def increment_punches(  
    punchcard_id: uuid.UUID,  
    db: Session = Depends(get_db)  
):  
    punchcard = db.query(PunchCard).filter(PunchCard.id == punchcard_id).first()  
    if not punchcard:  
        raise HTTPException(status_code=404, detail="Punch card not found")  
    
    # Increment punches
    punchcard.punches_achieved += 1  
    db.commit()  
    db.refresh(punchcard)  
    return {"message": "Punch incremented", "punches_achieved": punchcard.punches_achieved}