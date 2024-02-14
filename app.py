from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from api.metrics.metrics_api import metrics_router
from api.shortner.short_url_api import short_url_router
# from middleware_custom.exception_handler import custom_exception_handler, CustomRequestValidationError

load_dotenv() # this will load the configs from .env file
app = FastAPI()
# app.add_exception_handler(CustomRequestValidationError, custom_exception_handler)
# Include short_url_router and metrics_router
app.include_router(short_url_router, prefix="/short_url", tags=["short_url"])
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])


