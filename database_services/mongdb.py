from pymongo import MongoClient
import time
import os

class MongoDBService():
    _self = None
    def __new__(cls):
        # Singleton pattern to ensure only one instance is created
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.db_url = 'mongodb://%s:%s/'%(os.getenv("MONGO_DB_HOSTNAME"),os.getenv("MONGO_DB_PORT"))
            self.client = MongoClient(self.db_url)
            self.db = self.client['url_shortener']
            self.url_collection = self.db['urls']
            self.access_logs_collection = self.db['urls_access_logs_collection']
    
    def save_url(self, short_url, long_url, expiration_time):
        self.url_collection.insert_one({
            "short_url": short_url,
            "long_url": long_url,
            "expiration_time": int(expiration_time)
        })
    
    def create_access_log(self, short_url):
        current_time = int(time.time() * 1000)
        access_log = {
                    "short_url": short_url,
                    "access_timestamp": current_time
                }
        self.access_logs_collection.insert_one(access_log)
    
    def fetch_long_url(self, short_url):
       return self.url_collection.find_one({"short_url": short_url})
    
    def fetch_access_metric(self, query):
        return self.access_logs_collection.count_documents(query)
    
    def delete_short_url(self, short_url):
        return self.url_collection.delete_one({"short_url": short_url})
    