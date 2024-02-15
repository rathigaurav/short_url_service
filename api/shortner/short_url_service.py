
from fastapi import HTTPException, status

import redis
import random
import string
import time
from datetime import datetime, timedelta
from database_services.mongdb import MongoDBService
from database_services.redis import RedisService
from utils.logger import LoggerService

class ShortUrlService():
    _self = None
    def __new__(cls, mongodb_service, redis_service, logger_service):
        # Singleton pattern to ensure only one instance is created
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self
    
    def __init__(self, mongodb_service, redis_service, logger_service):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.log = logger_service 
            self.SHORT_URL_SIZE = 6 
            self.SHORT_URL_BASE_PATH = 'https://shorty/'
            self.DEFAULT_EXPIRATION_TIME_MS = 8018872932000 # ~200years
            self.mongodb_service = mongodb_service
            self.redis_service = redis_service

    def generate_short_url(self, long_url, expiration_time):
        """
        Generate a short URL for the given long URL.
        """
        try:
            self.log.info('Generate short url for long_url:%s with expiration_time:%s'%(long_url, expiration_time))
            long_url = str(long_url)
            expiration_time = expiration_time
            short_url = self.short_url_generator()
            self.save_url(short_url, long_url, expiration_time)
            self.log.info('short_url:%s generated for long_url:%s'%(short_url, long_url))
            return short_url
        except Exception as e:
            error_message = 'Failed to generate short_url. Error:%s'%(e)
            self.log.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error':error_message})

    
    def get_long_url(self, short_url):
        """
        Get the long URL associated with the short URL.
        Try to fetch from redis. If not found in redis
        fetch it form mongodb and cache it in redis.
        """
        try:
            self.log.info('Redirect short_url:%s'%(short_url))
            long_url = self.redis_service.get_long_url(short_url)
            if not long_url:
                long_url = self.get_long_url_from_db(short_url)
            # persist access logs for metric generation
            self.mongodb_service.create_access_log(short_url)
            return long_url
        except Exception as e:
            error_message = 'Failed to get long_url. Error:%s'%(e)
            self.log.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error':error_message})

    def delete_short_url(self, short_url):
        """
        Delete the short URL from both Redis and MongoDB.
        """
        try:
            self.log.info('Deleting short_url:%s'%(short_url))
            self.delete_short_url_from_db(short_url)
            self.redis_service.delete_short_url(short_url)
            self.log.info('short_url:%s successfully deleted.'%(short_url))
        except Exception as e:
            error_message = 'Failed to delete short_url. Error:%s'%(e)
            self.log.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error':error_message})

    
    def short_url_generator(self):
        """
        Generate a random string of length SHORT_URL_SIZE composed of alphabets [a-z, A-Z] and digits [0-9].
        The generated string is used as part of the short URL.
        """
        value = ''.join(random.choices(string.ascii_letters+string.ascii_uppercase + string.digits, k=self.SHORT_URL_SIZE))
        return "{}{}".format(self.SHORT_URL_BASE_PATH, value)
    
    def save_url(self, short_url, long_url, expiration_time):
        """
        Save the short URL, long URL, and expiration time in both Redis and MongoDB.
        """
        try:
            expiration_time = int(expiration_time) if expiration_time else self.DEFAULT_EXPIRATION_TIME_MS
            self.mongodb_service.save_url(short_url, long_url, expiration_time)
            self.set_url_in_redis(short_url, long_url, expiration_time)
        except Exception as e:
            self.log.error('Failed to save url in DB')
            raise e


    def set_url_in_redis(self, short_url, long_url, expiration_time):
        """
        Save the short URL and long URL in Redis.
        """
        current_timestamp_ms = int(time.time() * 1000)
        time_to_expire_secs = (expiration_time - current_timestamp_ms) // 1000
        # Set expiration time
        if time_to_expire_secs > 0:
            self.redis_service.cache_short_url(short_url, long_url, time_to_expire_secs)

    def get_long_url_from_db(self, short_url):
        """
        Retrieve the long URL associated with the given short URL from the MongoDB database.
        """
        document = self.mongodb_service.fetch_long_url(short_url)
        if document:
            long_url = document["long_url"]
            expiration_time = document.get("expiration_time")
            if expiration_time < int(time.time() * 1000):
                message = 'short_url: %s has expired.'%(short_url)
                self.log.error(message)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error':message})
            # If found in MongoDB, cache it in Redis.
            self.set_url_in_redis(short_url, long_url, expiration_time)
            return long_url
        else:
            message = 'Cannot redirect. short_url: %s not found.'%(short_url)
            self.log.error(message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error':message})
    
    def delete_short_url_from_db(self, short_url):
        result = self.mongodb_service.delete_short_url(short_url)
        if result.deleted_count == 0 :
            message = 'short_url: %s does not exist.'%(short_url)
            self.log.error(message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error':message})
        return result

def get_short_url_service():
    return ShortUrlService(MongoDBService(), RedisService(), LoggerService())