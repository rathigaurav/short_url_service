from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from .metrics_service import get_metrics_service
from dotenv import load_dotenv

metrics_router = APIRouter()

@metrics_router.get("/access_count/{short_url:path}")
async def get_metrics(short_url:str, metrics_service=Depends(get_metrics_service)):
    metrics = metrics_service.generate_access_metrics(short_url)
    return JSONResponse(content = {"metrics":metrics}, status_code=200)
    