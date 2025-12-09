from fastapi import Depends
from core.httpx_client import get_httpx_client
from core.config import get_settings, Settings
import httpx

async def fetch_weather_data(
    city_name: str, 
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(get_httpx_client)
    ) -> dict:
    BaseURL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.419,
        "current_weather": True,
    }
    headers = {
        "X-API-Key": settings.API_AUTH_KEY,
        "User-Agent": "FastAPI-Weather-App1.0",
    }

    response = await client.get(BaseURL, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

