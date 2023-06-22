import asyncio
import datetime
from typing import Optional

import uvloop
from dotenv import load_dotenv
from pyrogram import Client

from Parsers.ParserInterface import ParserInterface
from Parsers.ParserInterface import Post

###

###

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

                    if message.id < last_postId:
                        iterate_status = False
                        break

                    if message.id <= 1:
                        iterate_status = False
                        break

                    if (message.date - date_offset).days < 0:
                        iterate_status = False
                        break

                    print(message)

                    posts.append(Post())
                    is_reply = (
                        True if message.forward_from_chat.id is not None else False
                    )
                    text = message.text
                    post_id = message.id
                    date = message.date
                    media_files = []

            #         post = {
            #             "id_post": message.id,
            #             "id_channel": target,
            #             "date": message.date,
            #             "text": message.text
            #             if message.text is not None
            #             else message.caption,
            #             "views": message.views if message.views is not None else 0,
            #             "id_channel_forward_from": message.forward_from_chat.id
            #             if message.forward_from_chat is not None
            #             else None,
            #             "media_group_id": message.media_group_id
            #             if message.media_group_id is not None
            #             else None
            #         }
            #
            #         posts.append(post)
            #         offset_id = posts[len(posts) - 1]["id_post"]
            #
            # mediaGroups = list()
            # i = 1
            # while i < len(posts):
            #
            #     mediaGroup = list()
            #     if (
            #             posts[i - 1]["media_group_id"] is not None
            #             and posts[i - 1]["media_group_id"] == posts[i]["media_group_id"]
            #     ):
            #
            #         while (
            #                 i < len(posts)
            #                 and posts[i - 1]["media_group_id"] == posts[i]["media_group_id"]
            #         ):
            #             mediaGroup.append(posts[i - 1])
            #             i += 1
            #
            #         mediaGroup.append(posts[i - 1])
            #
            #     if len(mediaGroup) != 0:
            #         mediaGroups.append(mediaGroup)
            #
            #     i += 1
            # print(i)
            #
            # for mediaGroup in mediaGroups:
            #     for msg in mediaGroup:
            #         if msg['text'] is None:
            #             posts.remove(msg)
            #
            # for post in posts:
            #     print(post, end="\n\n")

    async def parse_until_date(self, until_date: datetime, target: str | int):
        dateDiff: int = TGChannelParser.count_days_until_date(target_date=until_date)
        await self.parse_chat(target=target, days_for_date_offset=dateDiff)

    async def parse_until_id(self, until_id: int, target: str | int):
        await self.parse_chat(target=target, last_postId=until_id)

    async def parse_all(self, target: str | int):
        pass


uvloop.install()
# asyncio.run(
#     TGChannelParser.create_session(
#         session_name="session",
#         api_id=,
#         api_hash=""
#     )
# )

t = TGChannelParser()
# print(t.count_days_until_date(target_date="2023-06-20 00:00:00"))
# asyncio.run(
#     t.parse_chat(
#         target="@etp_invest",
#
#     )
# )

# asyncio.run(
#     t.download_media(file_id="AQADAgADKcExG5Az6EkAEAMAAwH2J-YW____eF_rv9K89FgABB4E")
# )
