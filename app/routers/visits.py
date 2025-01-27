from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session  
from app.db.session import get_db  
from app.models import Visit  
from app.schemas import VisitCreate  
from datetime import datetime, timedelta  
from app.utils.redis_client import get_cache  

router = APIRouter()  

@router.post("/visits")  
async def log_visit(  
    visit: VisitCreate,  
    db: Session = Depends(get_db),  
    redis = Depends(get_cache)  
):  
    # Anti-spam check
    last_visit_key = f"last_visit:{visit.customer_id}"  
    last_visit = redis.get(last_visit_key)  
    if last_visit:  
        last_time = datetime.fromisoformat(last_visit.decode())  
        if (datetime.utcnow() - last_time).days < 1:  
            raise HTTPException(status_code=429, detail="Rate limited")  

    # Database persistence
    new_visit = Visit(**visit.dict())
    db.add(new_visit)  
    db.commit()  
    db.refresh(new_visit)  

    redis.set(last_visit_key, datetime.utcnow().isoformat(), ex=86400)  
    return {"message": "Visit logged successfully.", "visit_id": str(new_visit.id)}