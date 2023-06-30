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
from sqlalchemy.sql import text

from DataBase.Models import Chains
from DataBase.Models import User


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
