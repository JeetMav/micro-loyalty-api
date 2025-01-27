# app/utils/redis_client.py  

from redis import Redis  
from app.core.config import settings  

redis_client = Redis.from_url(settings.REDIS_URL)  

def get_cache():  
    return redis_client  