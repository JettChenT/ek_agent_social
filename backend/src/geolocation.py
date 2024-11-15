import os
from ek_geo import Point, Coords
from .datastructs import Content
from openai import AsyncOpenAI
from httpx import AsyncClient

oai_client = AsyncOpenAI()
API_URL = "https://models.earthkit.app/geoclip"
a_client = AsyncClient()

async def geoclip_img(img_url: str) -> Point:
    gclip_api_key = os.getenv("GEOCLIP_API_KEY")
    if not gclip_api_key:
        raise ValueError("GEOCLIP_API_KEY is not set")
    response = await a_client.post(
        API_URL,
        json={"image_url": img_url},
        headers={"X-api-key": gclip_api_key},
    )
    res_json = response.json()
    return Point(res_json["latitude"], res_json["longitude"])

async def geolocate(content: Content) -> Point:
    async with a_client as client:
        response = await client.post(API_URL, json={"api_key": gclip_api_key, "text": content.content})
        return Point(response.json()["latitude"], response.json()["longitude"])
