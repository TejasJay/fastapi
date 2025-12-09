from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from external_services.weather import fetch_weather_data
from core.config import get_settings, Settings
from core.httpx_client import get_httpx_client
import httpx
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

router = APIRouter()

@router.get("/{city_name}")
@cache(expire=300, namespace="get_weather_data")
async def get_weather_data(
    city_name: str, 
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(get_httpx_client)
    ) -> dict:
    return await fetch_weather_data(city_name, settings, client)
