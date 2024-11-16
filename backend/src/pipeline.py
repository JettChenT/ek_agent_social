from typing import List
from httpx import AsyncClient
from rss_parser import RSSParser
import uuid
import asyncio
from datetime import datetime, timedelta

from .datastructs import Content, Source, Aggregator, Filter, Enhancer, Pipeline, Logs
from .utils import flatten, spread

a_client = AsyncClient()

async def fetch_content(source: Source) -> List[Content]:
    """
    Fetch content from a source. We support RSS feeds for now.
    """
    response = await a_client.get(source.url)
    response_content = response.text
    if response_content.startswith("<?xml") and "<rss" in response_content:
        # RSS
        contents = RSSParser.parse(response_content)
        return [
            Content(
                id=str(uuid.uuid4()),
                src_id=source.id,
                title=content.content.title.content,
                content=str(content.content.description.content),
                tweet_url=content.guid.content,
                timestamp=datetime.strptime(content.content.pub_date.content, "%a, %d %b %Y %H:%M:%S %Z")
            )
            for content in contents.channel.items
        ]
    else:
        return []

def filter_after_ts(contents: List[Content], ts: datetime) -> List[Content]:
    return [content for content in contents if content.timestamp > ts]

async def proc_sources(pipeline: Pipeline) -> List[List[Content]]:
    """
    Returns a list of new contents from a list of sources.
    """
    contents = await asyncio.gather(*[
        fetch_content(source)
        for source in pipeline.sources
    ])
    contents = [
        filter_after_ts(content, pipeline.last_checked)
        for content in contents
    ]
    return contents

async def run_pipeline(pipeline: Pipeline):
    source_updates = await proc_sources(pipeline)
    return source_updates

async def _main():
    from rich import print
    tst_sources = [
        # "https://determined-insight-production.up.railway.app/twitter/user/jettchen5",
        "https://determined-insight-production.up.railway.app/twitter/user/luoluo_ai",
        # "https://determined-insight-production.up.railway.app/bsky/profile/bsky.app",
        # "https://determined-insight-production.up.railway.app/twitter/list/839124356638904320"
    ]
    sources = [Source(id=str(uuid.uuid4()), name=f"test-{i}", url=url) for i, url in enumerate(tst_sources)]
    pipeline = Pipeline(
        id=str(uuid.uuid4()), 
        name="test", 
        sources=sources, 
        last_checked=datetime.now()-timedelta(hours=10)
    )
    print(await run_pipeline(pipeline))

if __name__ == "__main__":
    import asyncio
    asyncio.run(_main())
