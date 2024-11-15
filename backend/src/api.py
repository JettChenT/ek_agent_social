from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from datetime import datetime
from typing import List
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

prisma = Prisma()
app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentResponse(BaseModel):
    id: str
    content: str
    tweet_url: str | None
    timestamp: datetime
    lat: float | None
    lng: float | None
    ek_agent_url: str | None

@app.get("/content", response_model=List[ContentResponse])
async def get_content():
    try:
        contents = await prisma.content.find_many(
            order={
                'timestamp': 'desc'
            }
        )
        return contents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
