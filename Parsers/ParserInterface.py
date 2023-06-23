import dataclasses
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import List
from typing import Optional


class ParserInterface(ABC):
    @abstractmethod
    async def parse_until_date(self, until_date: datetime, target: str | int):
        pass

    @abstractmethod
    async def parse_until_id(self, until_id: int, target: str | int):
        pass

    @abstractmethod
    async def parse_all(self, target: str | int):
        pass


class ParserMiddleware:
    @classmethod
    async def parse_until_date(cls, instance, until_date: datetime, target: str | int):
        await instance.parse_until_date(until_date=until_date, target=target)

    @classmethod
    async def parse_until_id(cls, instance, until_id: int, target: str | int):
        await instance.parse_until_id(until_id=until_id, target=target)

    @classmethod
    async def parse_all(cls, instance, target: str | int):
        await instance.parse_all(target=target)


@dataclasses.dataclass
class Post:
    id: int
    text: str
    date: datetime
    media_files: List[str]
    media_group_id: Optional[int]
    caption: Optional[str]
    reply_to_message_id: Optional[int]
    is_repost: Optional[bool] = None
