from app.core.redis import redis_client
import logging
logger = logging.getLogger(__name__)

def invalid_product_cache():
    keys = redis_client.keys("product:*")
    if keys:
        redis_client.delete(*keys)

    logging.info("Product Cache is invalid")    
        
    