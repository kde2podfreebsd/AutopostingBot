import asyncio
import datetime
from datetime import datetime, timedelta
import json
# from datetime import datetime
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
                chat_id=chat_id,
                target_channel=target_channel,
                source_urls=source_urls,
                parsing_type=str(parsing_type),
                parsing_time=parsing_time,
                additional_text=additional_text,
                active_due_date=active_due_date,
            )
            self.db_session.add(chain)
            await self.db_session.commit()
            return "Chain added"
        except IntegrityError:
            await self.db_session.rollback()
            return "Failed to add chain"

    async def getChainsByChatId(self, chat_id: int):
        chains = await self.db_session.execute(
            select(Chains).where(Chains.chat_id == chat_id)
        )
        return chains.fetchall()

    async def countActiveChainsByChatId(self, chat_id: int):
        current_datetime = datetime.now()
        count = await self.db_session.scalar(
            select(func.count(Chains.chain_id)).where(
                and_(Chains.chat_id == chat_id, Chains.active_due_date > current_datetime)
            )
        )
        return count

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

    async def updateActiveDueDate(self, chain_id: int, interval_days: int):
        chain = await self.db_session.execute(
            select(Chains).where(Chains.chain_id == chain_id)
        )
        chain = chain.fetchone()
        if chain is None:
            return "Chain not found"
        chain_obj = chain[0]
        current_date = datetime.now()

        if chain_obj.active_due_date < current_date:
            chain_obj.active_due_date = current_date + timedelta(days=interval_days)
        else:
            chain_obj.active_due_date += timedelta(days=interval_days)

        await self.db_session.commit()
        return "Active due date updated"


# async def test():
#     async with async_session() as session:
#         chain_dal = ChainDAL(session)

        # res1 = await chain_dal.createChain(
        #     chat_id=12345679,
        #     target_channel="channel_name",
        #     source_urls=[{"url": "example.com"}, {"url": "another.com"}],
        #     parsing_type="type",
        #     parsing_time=["10:00", "14:00"],
        #     additional_text="Additional text",
        #     active_due_date=datetime.datetime(2023, 12, 31)
        # )
        #
        # await chain_dal.createChain(
        #     chat_id=12345679,
        #     target_channel="channel_name",
        #     source_urls=[{"url": "example.com"}, {"url": "another.com"}],
        #     parsing_type="type",
        #     parsing_time=["10:00", "14:00"],
        #     additional_text="Additional text",
        #     active_due_date=datetime.datetime(2023, 12, 31)
        # )
        #
        # # Получение всех связок пользователя с chat_id 12345679
        # user_chat_id = 12345679
        # user_chains = await chain_dal.getChainsByChatId(user_chat_id)
        # print(user_chains)

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



# if __name__ == "__main__":
#     asyncio.run(test())
