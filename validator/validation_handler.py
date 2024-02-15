from fastapi import HTTPException, Query, status
from pydantic import BaseModel, constr, HttpUrl, validator
from typing import Union
import time
class CreateShortURLInput(BaseModel):
    long_url : str
    expiration_time: Union[int, None]

    @validator("long_url")
    def validate_long_url(cls, value):
        #Supports only http,https,ftp URL
        if not (value.startswith("http://") or value.startswith("ftp://") or  value.startswith("https://")) :
            message = "Provide a valid URL starting with 'http' or 'https' or 'ftp'. Ex:https://www.cloudflare.com/"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error':message})
        return value

    @validator("expiration_time")
    def validate_expiration_time(cls, value):
        # Custom validation logic for expiration_time
        # Ensure it's future time_stamp in ms
        current_timestamp_ms = int(time.time() * 1000)
        if len(str(value))!=13 or value < current_timestamp_ms:
            message = "Expiration time must be a future timestamp(integer) in milliseconds. Ex:1707807728000"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error':message})
        return value