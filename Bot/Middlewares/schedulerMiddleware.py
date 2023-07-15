import asyncio
from datetime import datetime

import aioschedule
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.sql import func

from DataBase.Models import Chains
from DataBase.Models import Post
from DataBase.session import async_session


class SchedulerMiddleware:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def get_pending_posts(self):
        async with async_session() as session:
            async with session.begin():
                current_datetime = func.now()
                chains = await session.execute(
                    select(Chains).where(Chains.active_due_date >= current_datetime)
                )
                for chain in chains.all():
                    print(chain)
                    # posts = await session.execute(
                    #     select(Post).where(
                    #         and_(Post.chain_id == chain.chain_id, Post.is_sent == False)
                    #     )
                    # )
                    # for post in posts.all():
                    #     # Действия с найденными постами
                    #     print(f"Pending Post ID: {post.post_id}, Chain ID: {chain.chain_id}")


scheduler = SchedulerMiddleware()
asyncio.run(scheduler.get_pending_posts())
