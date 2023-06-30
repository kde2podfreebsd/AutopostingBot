from typing import List
from typing import Optional
from typing import Union

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from DataBase.Models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createUser(self, chat_id):
        try:
            not_empty = await self.db_session.execute(
                select(User).where(User.chat_id == chat_id)
            )
            not_empty = not_empty.fetchone()
            if not_empty is None:
                self.db_session.add(User(chat_id=chat_id))
                await self.db_session.commit()
                return "User added"

            else:
                return "User already exist"

        except IntegrityError:
            await self.db_session.rollback()
            return IntegrityError
