# app/core/security.py

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.core.config import settings

def create_jwt(customer_id: str) -> str:
    payload = {
        "sub": customer_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"[DEBUG] Generated Token: {token}")  # Debug token
    return token

# def verify_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(
#             token, 
#             settings.SECRET_KEY, 
#             algorithms=[settings.ALGORITHM]
#         )
#         print(f"[DEBUG] Token Payload: {payload}")  # Debug payload
#         return payload
#     except JWTError as e:
#         print(f"[ERROR] JWT Validation Failed: {str(e)}")  # Debug error
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# In security.py (for testing only)

def verify_token(token: str) -> dict:
    try:
        # Hardcode a valid token for testing
        if token == "DEBUG_MODE":
            return {"sub": "test-customer-id"}
        
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Not authenticated")