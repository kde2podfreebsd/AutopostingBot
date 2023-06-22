import asyncio
import re
from dataclasses import dataclass
from typing import List
from typing import Set

from Bot.Config.bot import bot


@dataclass
class ChainBuilder:
    target_tg_channel_username: int | str
    source_urls: List[Set]


class NewChainManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.chainStore = dict()

    @classmethod
    def is_valid_url(cls, url):
        pattern = re.compile(
            r"^(https?://)?"  # http:// или https://
            r"((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"  # доменное имя
            r"((\d{1,3}\.){3}\d{1,3}))"  # IP-адрес
            r"(:\d+)?"  # необязательный порт
            r"(/[-a-z\d%_.~+]*)*"  # путь и параметры
            r"(\?[;&a-z\d%_.~+=-]*)?"  # параметры запроса
            r"(\#[-a-z\d_]*)?$",  # фрагмент-идентификатор
            re.IGNORECASE,
        )
        return bool(re.match(pattern, url))

    def newChain(self, chat_id: int | str):
        self.chainStore[chat_id] = []
        self.chainStore[chat_id].append(
            ChainBuilder(target_tg_channel_username=None, source_urls=[])
        )

    async def add_target_channel(self, chat_id: int | str, target_username: str):
        try:
            await bot.get_chat_administrators(chat_id=target_username)
        except Exception:
            return False
        builder = ChainBuilder(
            target_tg_channel_username=target_username, source_urls=[]
        )
        self.chainStore[chat_id] = builder
        return True

    def add_source_url(self, chat_id: int | str, source_url: str, source_type: str):
        builder = self.chainStore[chat_id]
        if builder is not None:
            builder.add_source_url(source_url, source_type)
