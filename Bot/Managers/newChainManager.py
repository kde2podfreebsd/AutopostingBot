import asyncio  # noqa
from dataclasses import dataclass
from typing import List
from typing import Set

# import re


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

    def newChain(self, chat_id: int | str):
        self.chainStore[chat_id] = ChainBuilder(
            target_tg_channel_username=None, source_urls=[]
        )

    def add_source_url(self, chat_id: int | str, source_url: str, source_type: str):
        if chat_id not in self.chainStore:
            self.chainStore[chat_id] = ChainBuilder(
                target_tg_channel_username=None, source_urls=[]
            )

        chain_builder = self.chainStore[chat_id]
        if len(chain_builder.source_urls) >= 3:
            return "MaxSize"

        for source in chain_builder.source_urls:
            if source["url"] == source_url and source["source_type"] == source_type:
                return False

        chain_builder.source_urls.append(
            {"url": source_url, "source_type": source_type}
        )
        return True

    def get_source_urls(self, chat_id: int | str) -> str:
        if chat_id not in self.chainStore:
            return "Chat ID not found\."  # noqa

        chain_builder = self.chainStore[chat_id]
        if not chain_builder.source_urls:
            return "No source URLs found\."  # noqa

        result = "Вы выбрали:\n"
        for i, source in enumerate(chain_builder.source_urls, start=1):
            result += f"{i}\\. Тип \\- {source['source_type']} \\| Ссылка \\- {source['url']}\n\n"

        return result

    def add_target_channel(self, chat_id: int | str, channel: str):
        chain_builder = self.chainStore[chat_id]
        chain_builder.target_tg_channel_username = channel
