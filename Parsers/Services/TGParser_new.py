import os
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
        self.media: str = f"{os.path.abspath(os.path.dirname(__file__))}/../../media/"

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

    @staticmethod
    def formatting_entities(message_type, message_parameter):
        if message_type is not None and message_parameter is not None:
            formatting_symbols = {
                MessageEntityType.ITALIC: "_",
                MessageEntityType.UNDERLINE: "__",
                MessageEntityType.TEXT_LINK: None,
                MessageEntityType.BOLD: "*",
                MessageEntityType.SPOILER: "||",
                MessageEntityType.STRIKETHROUGH: "~",
                MessageEntityType.CODE: "```",
            }

            def apply_text_link(entity, text):
                link_start = entity.offset
                link_end = entity.offset + entity.length
                url = entity.url
                url_length = len(url)
                return (
                        text[:link_start]
                        + "["
                        + text[link_start:link_end]
                        + "]"
                        + "("
                        + url
                        + ")"
                        + text[link_end:]
                )

            def apply_formatting(entity, text):
                symbol = formatting_symbols[entity.type] if entity.type != MessageEntityType.TEXT_LINK else ""
                return (
                        text[:entity.offset]
                        + symbol
                        + text[entity.offset: entity.offset + entity.length]
                        + symbol
                        + text[entity.offset + entity.length:]
                )

            entities = sorted(message_parameter, key=lambda e: e.offset, reverse=True)
            for entity in entities:
                if entity.type == MessageEntityType.TEXT_LINK:
                    message_type = apply_text_link(entity, message_type)
                    url_length = len(entity.url)

                    entities = [
                        MessageEntity(
                            type=e.type,
                            offset=e.offset,
                            length=e.length + (2 + url_length),
                            url=e.url if e.type == MessageEntityType.TEXT_LINK else None,
                        )
                        if e.offset >= entity.offset + entity.length
                        else e
                        for e in entities
                    ]
                    for e in entities:
                        e.length = e.length + (4 + url_length)
                elif entity.type in formatting_symbols:
                    message_type = apply_formatting(entity, message_type)
                    entities = [
                        MessageEntity(
                            type=e.type,
                            offset=e.offset + len(formatting_symbols[entity.type]) * 2,
                            length=e.length,
                            url=e.url if e.type == MessageEntityType.TEXT_LINK else None,
                        )
                        if e.offset >= entity.offset + entity.length
                        else e
                        for e in entities
                    ]
        return message_type

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
            days_for_date_offset: Optional[int] = 10,
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
                    message.text = self.formatting_entities(message.text, message.entities)
                    message.caption = self.formatting_entities(message.caption, message.caption_entities)

                    # Добавляем фото
                    if message.photo is not None:
                        photo_id: str = str(message.photo.file_id)
                        filename: str = f"{self.media}TG_photo_{photo_id}.jpg"
                        await app.download_media(message.photo, file_name=filename)
                        media_files.append(filename)

                    # Добавляем аудио (не больше 1 часа по длительности)
                    if message.audio is not None:
                        if message.audio.duration < 3600:
                            audio_id: str = str(message.audio.file_id)
                            audio_name: str = str(message.audio.file_name)
                            filename: str = f"{self.media}TG_audio_{audio_id}_name_{audio_name}"
                            await app.download_media(message.audio, file_name=filename)
                            media_files.append(filename)
                        else:
                            info_audio = "Аудио длительностью больше 1 часа"
                            media_files.append(info_audio)

                    # Добавляем голосовое сообщение
                    if message.voice is not None:
                        voice_id: str = str(message.voice.file_id)
                        filename: str = f"{self.media}TG_voice_{voice_id}.ogg"
                        await app.download_media(message.voice, file_name=filename)
                        media_files.append(filename)

                    # Добавляем видео (не больше 10 минут)
                    if message.video is not None:
                        if message.video.duration < 600:
                            video_id: str = str(message.video.file_id)
                            video_name: str = str(message.video.file_name)
                            filename: str = f"{self.media}TG_video_{video_id}_name_{video_name}"
                            await app.download_media(message.video, file_name=filename)
                            media_files.append(filename)
                        else:
                            info_video = "Видео длительностью больше 10-ти минут"
                            media_files.append(info_video)

                    # Добавляем видео-кружок
                    if message.video_note is not None:
                        videonote_id: str = str(message.video_note.file_id)
                        filename: str = f"{self.media}TG_videonote_{videonote_id}.mp4"
                        await app.download_media(message.video_note, file_name=filename)
                        media_files.append(filename)

                    # Объединяем медиа-группу из нескольких фото или видео в один пост
                    if message.media_group_id is not None:
                        found_group = False
                        for previous_post in posts:
                            if message.media_group_id == previous_post.media_group_id:
                                found_group = True
                                if message.photo is not None:
                                    if message.caption is not None:
                                        previous_post.text = message.caption
                                    photo_id: str = str(message.photo.file_id)
                                    filename: str = f"{self.media}TG_photo_{photo_id}.jpg"
                                    await app.download_media(message.photo, file_name=filename)
                                    previous_post.media_files.append(filename)
                                elif message.video is not None:
                                    if message.caption is not None:
                                        message.caption = message.text
                                        message.caption = None
                                    if message.video.duration < 600:
                                        video_id: str = str(message.video.file_id)
                                        video_name: str = str(message.video.file_name)
                                        filename: str = f"{self.media}TG_video_{video_id}_name_{video_name}"
                                        await app.download_media(message.video, file_name=filename)
                                        previous_post.media_files.append(filename)
                                    else:
                                        info_video = "Видео длительностью больше 10-ти минут"
                                        previous_post.media_files.append(info_video)
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
                            text=message.text or message.caption,
                            id=message.id,
                            date=message.date,
                            media_files=media_files,
                            media_group_id=message.media_group_id,
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
# asyncio.run(
#     TGChannelParser.create_session(
#         session_name="session",
#         api_id=os.getenv('API_ID'),
#         api_hash=os.getenv('API_HASH'),
#     )
# )

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