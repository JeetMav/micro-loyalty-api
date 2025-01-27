import pytest  
from fastapi.testclient import TestClient  
from app.main import app  
from app.db.session import SessionLocal, engine  
from app.models import Base  

@pytest.fixture(scope="session")  
def db():  
    Base.metadata.create_all(bind=engine)  
    db = SessionLocal()  
    yield db  
    db.close()  
    Base.metadata.drop_all(bind=engine)  

@pytest.fixture(scope="module")  
def client():  
    with TestClient(app) as c:  
        yield c  