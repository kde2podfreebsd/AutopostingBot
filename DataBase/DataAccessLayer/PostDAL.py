import asyncio
import datetime
import json
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from sqlalchemy import and_
from sqlalchemy import DateTime
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.sql import text

from DataBase.Models import Post
from DataBase.session import async_session


class PostDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createPost(
        self,
        chain_id: int,
        user_chat_id: int,
        post_text: str,
        post_date: datetime,
        media_files: List[str] = None,
    ):
        try:
            post = Post(
                chain_id=chain_id,
                user_chat_id=user_chat_id,
                post_text=post_text,
                post_date=post_date,
                media_files=media_files,
                is_sent=False,
            )
            self.db_session.add(post)
            await self.db_session.commit()
            return "Post created"
        except IntegrityError:
            await self.db_session.rollback()
            return "Failed to create post"

    async def updateIsSent(self, post_id: int):
        await self.db_session.execute(
            update(Post).where(Post.post_id == post_id).values(is_sent=True)
        )
        await self.db_session.commit()
        return "is_sent updated"


# async def test():
#     async with async_session() as session:
#         post_dal = PostDAL(session)
#
#         # Создание нового поста
#         await post_dal.createPost(
#             chain_id=1,
#             user_chat_id=12345678,
#             post_text="This is a sample post.",
#             post_date=datetime.now(),
#             media_files=["path/to/file1.jpg", "path/to/file2.png"]
#         )
#
#         # Обновление параметра is_sent для поста с заданным post_id
#         await post_dal.updateIsSent(post_id=1)
#
# if __name__ == "__main__":
#     asyncio.run(test())
