import asyncio
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
from DataBase.session import async_session


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

    async def getUserChains(self, chat_id):
        user = await self.db_session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        user = user.fetchone()
        if user is None:
            return None
        chains = []
        for post in user.posts:
            chain_id = post.chain_id
            if chain_id not in chains:
                chains.append(chain_id)
        return chains

    async def getUserByChatId(self, chat_id):
        user = await self.db_session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        user = user.fetchone()
        return user

    async def getAllUsers(self):
        users = await self.db_session.execute(select(User))
        return users.fetchall()


async def test():
    async with async_session() as session:
        user = UserDAL(session)

        status = await user.createUser(chat_id=12345679)
        print(status)
        status = await user.createUser(chat_id=12345678)
        print(status)

        user = await user.getUserByChatId(chat_id=12345678)
        user_obj = user[0]

        print(user_obj.chat_id)

        users = await UserDAL(session).getAllUsers()
        print(users)


if __name__ == "__main__":
    asyncio.run(test())
