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

from DataBase.Models import Chains
from DataBase.Models import User
from DataBase.session import async_session


class ChainDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createChain(
        self,
        chat_id: int,
        target_channel: str,
        source_urls: List[dict],
        parsing_type: Union[str, datetime],
        parsing_time: List[str],
        additional_text: str,
        active_due_date: datetime,
    ):
        try:
            chain = Chains(
                target_channel=target_channel,
                source_urls=source_urls,
                parsing_type=str(parsing_type),
                parsing_time=parsing_time,
                additional_text=additional_text,
                active_due_date=active_due_date,
            )
            user = await self.db_session.execute(
                select(User).where(User.chat_id == chat_id)
            )
            user = user.fetchone()
            if user is None:
                return "User not found"
            chain.user = user
            self.db_session.add(chain)
            await self.db_session.commit()
            return "Chain added"
        except IntegrityError:
            await self.db_session.rollback()
            return "Failed to add chain"

    async def getActiveChains(self):
        current_datetime = func.now()
        chains = await self.db_session.execute(
            select(Chains).where(Chains.active_due_date > current_datetime)
        )
        return chains.fetchall()

    async def updateChain(self, chain_id, **kwargs):
        chain = await self.db_session.execute(
            select(Chains).where(Chains.chain_id == chain_id)
        )
        chain = chain.fetchone()
        if chain is None:
            return "Chain not found"
        chain_obj = chain[0]  # Получение объекта Chains из кортежа
        for key, value in kwargs.items():
            setattr(chain_obj, key, value)
        await self.db_session.commit()
        return "Chain updated"

    async def updateActiveDueDate(self, chain_id: int, new_due_date: datetime):
        chain = await self.db_session.execute(
            select(Chains).where(Chains.chain_id == chain_id)
        )
        chain = chain.fetchone()
        if chain is None:
            return "Chain not found"
        chain_obj = chain[0]  # Получение объекта Chains из кортежа
        setattr(chain_obj, "active_due_date", new_due_date)
        await self.db_session.commit()
        return "Active due date updated"


async def test():
    async with async_session() as session:
        chain_dal = ChainDAL(session)

        # res1 = await chain_dal.createChain(
        #     chat_id=12345679,
        #     target_channel="channel_name",
        #     source_urls=[{"url": "example.com"}, {"url": "another.com"}],
        #     parsing_type="type",
        #     parsing_time=["10:00", "14:00"],
        #     additional_text="Additional text",
        #     active_due_date=datetime.datetime(2023, 12, 31)
        # )

        # print(res1)

        # Получение всех активных связок (цепочек)
        # active_chains = await chain_dal.getActiveChains()
        # print(active_chains)
        #
        # Обновление полей в связке по заданному chain_id
        # res3 = await chain_dal.updateChain(
        #     chain_id=1,
        #     target_channel="new_channel",
        #     additional_text="New additional kek"
        # )
        #
        # print(res3)
        #
        # result = await chain_dal.updateActiveDueDate(chain_id=1, new_due_date=datetime(2023, 12, 29))
        # print(result)


if __name__ == "__main__":
    asyncio.run(test())
