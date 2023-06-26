import os
import asyncio
import datetime
from typing import Optional
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import TypeMessageEntity
from telethon.tl.types import Message
from telethon.types import Message
from telethon.tl.types import MessageEntityTextUrl, MessageEntityBold, MessageEntityCode, \
    MessageEntityItalic, MessageEntityStrike, MessageEntityUnderline, MessageEntityUrl, MessageEntitySpoiler
from telethon import types
from Parsers.ParserInterface import ParserInterface
from Parsers.ParserInterface import Post
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel
from telethon.client import MessageMethods
import asyncio

load_dotenv()


class TGParserBot(ParserInterface):
    def __init__(self):
        self.app = TelegramClient("sessions/session5",
                                  api_id=23677472,
                                  api_hash="6945657dfb3f7d10558065c24bd8d904")

    @staticmethod
    async def main():
        async with TelegramClient(
                "sessions/session5",
                api_id=23677472,
                api_hash="6945657dfb3f7d10558065c24bd8d904",
        ) as app:
            await app.send_message("me", "Greetings from **Telethon**!")

    @staticmethod
    def count_days_until_date(target_date: str) -> int:
        dt = datetime.datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.datetime.now().date()
        target_date = dt.date()
        days_diff = (current_date - target_date).days
        return days_diff


    #
    # @staticmethod
    # def formatting_entities(message_type, message_parameter):
    #     if message_type is not None and message_parameter is not None:
    #         formatting_symbols = {
    #             MessageEntityType.ITALIC: "_",
    #             MessageEntityType.UNDERLINE: "__",
    #             MessageEntityType.TEXT_LINK: None,
    #             MessageEntityType.BOLD: "*",
    #             MessageEntityType.SPOILER: "||",
    #             MessageEntityType.STRIKETHROUGH: "~",
    #             MessageEntityType.CODE: "```",
    #         }
    #
    #         def apply_text_link(entity, text):
    #             link_start = entity.offset
    #             link_end = entity.offset + entity.length
    #             url = entity.url
    #             url_length = len(url)
    #             return (
    #                     text[:link_start]
    #                     + "["
    #                     + text[link_start:link_end]
    #                     + "]"
    #                     + "("
    #                     + url
    #                     + ")"
    #                     + text[link_end:]
    #             )
    #
    #         def apply_formatting(entity, text):
    #             symbol = formatting_symbols[entity.type] if entity.type != MessageEntityType.TEXT_LINK else ""
    #             return (
    #                     text[:entity.offset]
    #                     + symbol
    #                     + text[entity.offset: entity.offset + entity.length]
    #                     + symbol
    #                     + text[entity.offset + entity.length:]
    #             )
    #
    #         entities = sorted(message_parameter, key=lambda e: e.offset, reverse=True)
    #         for entity in entities:
    #             if entity.type == MessageEntityType.TEXT_LINK:
    #                 message_type = apply_text_link(entity, message_type)
    #                 url_length = len(entity.url)
    #
    #                 entities = [
    #                     MessageEntity(
    #                         type=e.type,
    #                         offset=e.offset,
    #                         length=e.length + (2 + url_length),
    #                         url=e.url if e.type == MessageEntityType.TEXT_LINK else None,
    #                     )
    #                     if e.offset >= entity.offset + entity.length
    #                     else e
    #                     for e in entities
    #                 ]
    #                 for e in entities:
    #                     e.length = e.length + (4 + url_length)
    #             elif entity.type in formatting_symbols:
    #                 message_type = apply_formatting(entity, message_type)
    #                 entities = [
    #                     MessageEntity(
    #                         type=e.type,
    #                         offset=e.offset + len(formatting_symbols[entity.type]) * 2,
    #                         length=e.length,
    #                         url=e.url if e.type == MessageEntityType.TEXT_LINK else None,
    #                     )
    #                     if e.offset >= entity.offset + entity.length
    #                     else e
    #                     for e in entities
    #                 ]
    #     return message_type

    async def download_media(self, file_id):
        try:
            async with self.app as app:
                pwd = await app.download_media(file_id)
                return pwd
        except Exception as e:
            return e

    async def parse_chat(
        self,
        chat_id: int,
        stored_channels: Optional[dict[str, int]] = None,
        days_for_date_offset: int = 183,
    ) -> ChatObject:
        try:
            async with self.app as app:
                posts = []
                mentions = []
                date_offset = datetime.datetime.now() - datetime.timedelta(days=days_for_date_offset)

                channel = await app.get_input_entity(chat_id)

                async for message in app.iter_messages(entity=channel):

                    if message.views == 0:
                        continue

                    if (message.date.replace(tzinfo=None) - date_offset).days < 0:
                        break

                    if stored_channels is not None:
                        for name in stored_channels:

                            text = message.message

                            if (
                                f"{name} " in str(text)
                                and (name is not None)
                            ):
                                mention = Mention(
                                    id_mentioned_channel=stored_channels[name],
                                    id_post=message.id,
                                    id_channel=chat_id,
                                )
                                mentions.append(mention)
                    from_id = None

                    if message.fwd_from is not None:
                        try:
                            from_id = message.fwd_from.from_id.channel_id
                        except:
                            from_id = None

                    post = Post(
                        id_post=message.id,
                        id_channel=chat_id,
                        date=message.date.replace(tzinfo=None),
                        text=message.message if message.message != "" else None,
                        views=message.views if message.views is not None else 0,
                        id_channel_forward_from=from_id,
                        media_group_id=message.grouped_id
                        if message.grouped_id is not None
                        else None,
                    )

                    posts.append(post)

                mediaGroups = list()
                i = 1
                while i < len(posts):

                    mediaGroup = list()
                    if (
                            posts[i - 1].media_group_id is not None
                            and posts[i - 1].media_group_id == posts[i].media_group_id
                    ):

                        while (
                                i < len(posts)
                                and posts[i - 1].media_group_id == posts[i].media_group_id
                        ):
                            mediaGroup.append(posts[i - 1])
                            i += 1

                        mediaGroup.append(posts[i - 1])

                    if len(mediaGroup) != 0:
                        mediaGroups.append(mediaGroup)

                    i += 1
                print(i)

                for mediaGroup in mediaGroups:
                    for msg in mediaGroup:
                        if msg.text is None:
                            posts.remove(msg)

            return ChatObject(posts=posts, mentions=mentions)

        except ValueError or Exception as e:
            print(e)

    async def parse_until_date(self, until_date: datetime, target: str | int):
        dateDiff: int = TGChannelParser.count_days_until_date(target_date=until_date)
        await self.parse_chat(target=target, days_for_date_offset=dateDiff)

    async def parse_until_id(self, until_id: int, target: str | int):
        await self.parse_chat(target=target, last_postId=until_id)

    async def parse_all(self, target: str | int):
        pass


# uvloop.install()
# asyncio.run(
#     TGChannelParser.create_session(
#         session_name="session",
#         api_id=os.getenv('API_ID'),
#         api_hash=os.getenv('API_HASH'),
#     )
# )

t = TGParserBot()
print(t.count_days_until_date(target_date="2023-06-23 15:00:00"))
asyncio.run(
    t.parse_chat(
        target="@wowparser",
    )
)


# asyncio.run(
#     t.download_media(file_id="AQADAgADKcExG5Az6EkAEAMAAwH2J-YW____eF_rv9K89FgABB4E")
# )
