from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


async def hello():
    print("hello")


scheduler = AsyncIOScheduler()
scheduler.add_job(hello, trigger=IntervalTrigger(minutes=27))
scheduler.start()
