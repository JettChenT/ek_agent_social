from pydantic import BaseModel
from datetime import datetime

class Content(BaseModel):
    id: str
    content: str

class Source(BaseModel):
    id: str
    name: str
    url: str

class Aggregator(BaseModel):
    id: str
    name: str
    sources_id: list[str]

class Filter(BaseModel):
    id: str
    sources_id: list[str]

class Enhancer(BaseModel):
    id: str
    name: str
    sources_id: list[str]

class Logs(BaseModel):
    src_id: str
    dst_id: str
    timestamp: datetime
    message: str

class Pipeline(BaseModel):
    id: str
    name: str
    sources: list[Source]
    aggregators: list[Aggregator]
    filters: list[Filter]
    enhancers: list[Enhancer]
