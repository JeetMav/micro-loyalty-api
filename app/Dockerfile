FROM python:3.11-slim  
RUN pip install fastapi uvicorn sqlalchemy redis  
EXPOSE 8000  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]  
