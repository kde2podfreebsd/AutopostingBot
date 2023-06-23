import asyncio
import datetime
from typing import Optional

import pyrogram  # noqa
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram import types  # noqa
from pyrogram.enums import MessageEntityType
from pyrogram.raw.types.message_entity_bold import MessageEntityBold  # noqa
from pyrogram.raw.types.message_entity_code import MessageEntityCode  # noqa
from pyrogram.raw.types.message_entity_italic import MessageEntityItalic  # noqa
from pyrogram.raw.types.message_entity_spoiler import MessageEntitySpoiler  # noqa
from pyrogram.raw.types.message_entity_underline import MessageEntityUnderline  # noqa
from pyrogram.types import Audio  # noqa
from pyrogram.types import Message  # noqa
from pyrogram.types import MessageEntity  # noqa
from pyrogram.types import Photo  # noqa
from pyrogram.types import Video  # noqa
from pyrogram.types import VideoNote  # noqa
from pyrogram.types import Voice  # noqa

from Parsers.ParserInterface import ParserInterface
from Parsers.ParserInterface import Post

load_dotenv()


class TGChannelParser(ParserInterface):
    def __init__(self, session_name: str = "session"):
        self.app = Client(f"sessions/{session_name}")

    @staticmethod
    async def create_session(api_id: int, api_hash: str, session_name: str = "session"):
        async with Client(
            name=f"sessions/{session_name}", api_id=api_id, api_hash=api_hash
        ) as app:
            await app.send_message("me", "Init session from server!")

    @staticmethod
    def count_days_until_date(target_date: str) -> int:
        dt = datetime.datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.datetime.now().date()
        target_date = dt.date()
        days_diff = (current_date - target_date).days
        return days_diff

    async def download_media(self, file_id):
        try:
            async with self.app as app:
                pwd = await app.download_media(file_id)
                return pwd
        except Exception as e:
            return e

    async def parse_chat(
        self,
        target: int | str,
        last_postId: Optional[int] = None,
        days_for_date_offset: Optional[int] = 2,
    ):
        async with self.app as app:

            posts = []
            iterate_status = True
            offset_id = 0
            date_offset = datetime.datetime.now() - datetime.timedelta(
                days=days_for_date_offset
            )

            while iterate_status:
                async for message in app.get_chat_history(
                    chat_id=target, offset_id=offset_id, limit=100
                ):

                    if last_postId is not None and message.id < last_postId:
                        iterate_status = False
                        break

                    if message.id <= 1:
                        iterate_status = False
                        break

                    if (message.date - date_offset).days < 0:
                        iterate_status = False
                        break

                    print(f"\n\n ↓ ПОСТ №{message.id} ↓ \n\n", message)

                    media_files = []

                    # Форматирование текста в Markdown
                    if message.entities is not None:
                        for entity in message.entities:
                            if entity.type is MessageEntityType.ITALIC:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "*"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "*"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.UNDERLINE:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "__"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "__"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.BOLD:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "**"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "**"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.SPOILER:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "||"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "||"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.STRIKETHROUGH:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "~~"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "~~"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.CODE:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "`"
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "`"
                                    + message.text[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.TEXT_LINK:
                                message.text = (
                                    message.text[: entity.offset]
                                    + "["
                                    + message.text[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "]("
                                    + entity.url
                                    + ")"
                                    + message.text[entity.offset + entity.length :]
                                )

                    # Форматирование описания к медиагруппе / фото / видео в Markdown
                    if (
                        message.caption is not None
                        and message.caption_entities is not None
                    ):
                        for entity in message.caption_entities:
                            if entity.type is MessageEntityType.ITALIC:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "*"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "*"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.UNDERLINE:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "__"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "__"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.BOLD:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "**"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "**"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.SPOILER:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "||"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "||"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.STRIKETHROUGH:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "~~"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "~~"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.CODE:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "`"
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "`"
                                    + message.caption[entity.offset + entity.length :]
                                )
                            elif entity.type is MessageEntityType.TEXT_LINK:
                                message.caption = (
                                    message.caption[: entity.offset]
                                    + "["
                                    + message.caption[
                                        entity.offset : entity.offset + entity.length
                                    ]
                                    + "]("
                                    + entity.url
                                    + ")"
                                    + message.caption[entity.offset + entity.length :]
                                )

                    # Добавляем фото
                    if message.photo is not None:
                        pwd = self.download_media(message.photo.file_id)
                        media_files.append(pwd)

                    # Добавляем аудио (не больше 1 часа по длительности)
                    if message.audio is not None:
                        if message.audio.duration < 3600:
                            pwd = self.download_media(message.audio.file_id)
                            media_files.append(pwd)
                        else:
                            continue

                    # Добавляем голосовое сообщение
                    if message.voice is not None:
                        pwd = self.download_media(message.voice.file_id)
                        media_files.append(pwd)

                    # Добавляем видео (не больше 10 минут)
                    if message.video is not None:
                        if message.video.duration < 600:
                            pwd = self.download_media(message.video.file_id)
                            media_files.append(pwd)
                        else:
                            info_video = print("Видео длительностью больше 10-ти минут")
                            media_files.append(info_video)

                    # Добавляем видео-кружок
                    if message.video_note is not None:
                        pwd = self.download_media(message.video_note.file_id)
                        media_files.append(pwd)

                    # Объединяем медиа-группу из нескольких фото или видео в один пост
                    if message.media_group_id is not None:
                        found_group = False
                        for previous_post in posts:
                            if message.media_group_id == previous_post.media_group_id:
                                found_group = True
                                if message.photo is not None:
                                    pwd = self.download_media(message.photo.file_id)
                                    previous_post.media_files.append(pwd)
                                elif message.video is not None:
                                    pwd = self.download_media(message.video.file_id)
                                    previous_post.media_files.append(pwd)
                                break
                        if found_group:
                            continue

                        # Определяем id поста, на которое ответили другим сообщением
                        if message.reply_to_message_id is not None:
                            return message.reply_to_message_id

                        # Пропускаем стикеры
                        if message.sticker is not None:
                            continue

                        # Пропускаем опросы
                        if message.poll is not None:
                            continue

                    posts.append(
                        Post(
                            text=message.text,
                            id=message.id,
                            date=message.date,
                            media_files=media_files,
                            media_group_id=message.media_group_id,
                            caption=message.caption,
                            reply_to_message_id=message.reply_to_message_id,
                        )
                    )

                offset_id += 100

            for one_post in posts:
                print(one_post, sep="\n")

            return posts

    async def parse_until_date(self, until_date: datetime, target: str | int):
        dateDiff: int = TGChannelParser.count_days_until_date(target_date=until_date)
        await self.parse_chat(target=target, days_for_date_offset=dateDiff)

    async def parse_until_id(self, until_id: int, target: str | int):
        await self.parse_chat(target=target, last_postId=until_id)

    async def parse_all(self, target: str | int):
        pass


# uvloop.install()
# # asyncio.run(
# #     TGChannelParser.create_session(
# #         session_name="session",
# #         api_id=,
# #         api_hash=""
# #     )
# # )

t = TGChannelParser()
print(t.count_days_until_date(target_date="2023-06-23 15:00:00"))
asyncio.run(
    t.parse_chat(
        target="@wowparser",
    )
)

# asyncio.run(
#     t.download_media(file_id="AQADAgADKcExG5Az6EkAEAMAAwH2J-YW____eF_rv9K89FgABB4E")
# )
