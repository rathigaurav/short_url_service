from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, HttpUrl

from .short_url_service import get_short_url_service
from validator.validation_handler import CreateShortURLInput

short_url_router = APIRouter()

@short_url_router.post('/create')
async def shorten_url(input:CreateShortURLInput, short_url_service=Depends(get_short_url_service)):
    long_url = input.long_url
    expiration_time = input.expiration_time
    short_url = short_url_service.generate_short_url(long_url, expiration_time)
    return JSONResponse(content = {'short_url': short_url}, status_code=201)
    

@short_url_router.get("/lookup/{short_url:path}")
async def redirect_to_long_url(short_url:str, short_url_service=Depends(get_short_url_service)):
    long_url = short_url_service.get_long_url(short_url)
    return RedirectResponse(url=long_url)

@short_url_router.delete('/delete/{short_url:path}')
async def delete_short_url(short_url:str, short_url_service=Depends(get_short_url_service)):
    short_url_service.delete_short_url(short_url)
    return JSONResponse(content = {'message':'Short URL successfully deleted.'}, status_code=200)



