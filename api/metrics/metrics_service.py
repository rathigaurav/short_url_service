
from fastapi import HTTPException, status

import redis
import random
import time
from datetime import datetime, timedelta
from database_services.mongdb import MongoDBService
from database_services.redis import RedisService
from utils.logger import LoggerService

class MetricsService():
    _self = None
    def __new__(cls, mongodb_service, logger_service ):
        # Singleton pattern to ensure only one instance is created
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self
    
    def __init__(self, mongodb_service, logger_service):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.log = logger_service 
            self.mongodb_service = mongodb_service
    
    def generate_access_metrics(self, short_url):
        try:
            # Check if the short URL exists in the database
            if not self.mongodb_service.fetch_long_url(short_url):
                message = 'short_url: %s not found.'%(short_url)
                self.log.error(message)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error':message})
            """
            Get access metrics for the short URL i,e how many times a
            short_url has been accessed in last 24hr, 1week, all_time.
            """
            metrics =  {
                "24_hr": self.get_access_count_metric_24hr(short_url),
                "1_week": self.get_access_count_metric_1week(short_url),
                "all_time": self.get_access_count_metric_all_time(short_url),
            }
            self.log.info('access count metrics:%s for short_url:%s'%(metrics,short_url))
            return metrics

        except Exception as e:
            error_message = 'Failed to generate access_count metrics. Error:%s'%(e)
            self.log.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error':error_message})

    def get_access_count_metric_from_db(self, short_url, since):
        # MongoDB query to retrieve access metrics for a specified time range
        query = {
            "short_url": short_url,
            "access_timestamp": {"$gte": int(since.timestamp() * 1000)}  # Convert to milliseconds
        }
        return self.mongodb_service.fetch_access_metric(query)

    def get_access_count_metric_24hr(self, short_url):
        # Get access metrics for the last 24 hours
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=24)
        return self.get_access_count_metric_from_db(short_url, start_time)
    
    def get_access_count_metric_1week(self, short_url):
        # Get access metrics for the last 1 week
        current_time = datetime.now()
        start_time = current_time - timedelta(weeks=1)
        return self.get_access_count_metric_from_db(short_url, start_time)
    
    def get_access_count_metric_all_time(self, short_url):
        # Get access metrics for all time
        start_time= datetime.fromtimestamp(0)
        return self.get_access_count_metric_from_db(short_url, start_time)

def get_metrics_service():
    return MetricsService(MongoDBService(), LoggerService())