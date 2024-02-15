import redis
import time
import os

class RedisService():
    _self = None
    def __new__(cls):
        # Singleton pattern to ensure only one instance is created
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.client = redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOSTNAME"), port=os.getenv("REDIS_PORT"), db=0)
    
    def get_long_url(self, short_url):
        self.client.get(short_url)

    def delete_short_url(self, short_url):
        self.client.delete(short_url)
    
    def cache_short_url(self, short_url, long_url, time_to_expire_secs ):
        self.client.set(short_url, long_url)
        self.set_expiry_time(short_url, time_to_expire_secs)
    
    def set_expiry_time(self, short_url, time_to_expire_secs):
        self.client.expire(short_url, time_to_expire_secs)