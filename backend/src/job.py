from .pipeline import Pipeline, run_pipeline, Source, Content
import uuid
from datetime import datetime, timedelta
from .utils import spread
from prisma import Prisma
from prisma.models import Content as DbContent

prisma = Prisma()

SOURCES = [
    "https://determined-insight-production.up.railway.app/twitter/user/jettchen5",
    "https://determined-insight-production.up.railway.app/twitter/user/luoluo_ai",
]

async def main():
    pipeline = Pipeline(
        id=str(uuid.uuid4()), 
        name="test", 
        sources=[Source(id=str(uuid.uuid4()), name=f"test-{i}", url=url) for i, url in enumerate(SOURCES)], 
        last_checked=datetime.now() - timedelta(hours=10)
    )
    contents = await run_pipeline(pipeline)
    contents = [content for content_list in contents for content in content_list]
    print(contents)
    await prisma.connect()
    await prisma.content.create_many(
        data=[
            {
                "id": content.id,
                "content": content.content,
                "tweet_url": content.tweet_url,
                "timestamp": content.timestamp
            }
            for content in contents
        ],
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
