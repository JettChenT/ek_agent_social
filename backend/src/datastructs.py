from pydantic import BaseModel, Field
from datetime import datetime

class Content(BaseModel):
    id: str
    src_id: str
    content: str
    timestamp: datetime

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
    last_checked: datetime
    name: str
    sources: list[Source] = Field(default_factory=list)
    aggregators: list[Aggregator] = Field(default_factory=list)
    filters: list[Filter] = Field(default_factory=list)
    enhancers: list[Enhancer] = Field(default_factory=list)
