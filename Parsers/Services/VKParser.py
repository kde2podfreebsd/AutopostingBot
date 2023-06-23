import datetime
import os
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiohttp
import vk_api
from dotenv import load_dotenv

from Parsers.ParserInterface import ParserInterface
from Parsers.ParserInterface import Post

load_dotenv()


class VKGroupParser(ParserInterface):
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=os.getenv("VK_ACCESS_TOKEN"))
        self.vk = self.vk_session.get_api()
        self.vk_upload = vk_api.VkUpload(vk=self.vk)
        self.media = f"{os.path.abspath(os.path.dirname(__file__))}/../media/"

    async def parse_posts(
        self,
        target: int | str,
        last_postId: Optional[int] = None,
        until_date: Optional[int] = None,
    ) -> None:
        try:
            offset = 0
            dataset = []

            flag = True

            async with aiohttp.ClientSession() as session:
                while flag:
                    posts = await self.vk_request(
                        session,
                        "wall.get",
                        owner_id="-" + str(target),
                        count=100,
                        offset=offset,
                    )

                    if len(posts["items"]) == 0:
                        break

                    for post in posts["items"]:
                        post_id: int = post["id"]
                        if last_postId is not None and post_id < last_postId:
                            flag = False
                            continue

                        if until_date is not None:
                            if post["date"] > until_date:
                                flag = True
                            if post["date"] < until_date:
                                flag = False
                                continue

                        text: str = post["text"]
                        date: int = post["date"]
                        is_repost: bool = "copy_history" in post
                        media_files: List[str] = []

                        if "attachments" in post:
                            for attachment in post["attachments"]:
                                attachment_type: str = attachment["type"]

                                try:
                                    if attachment_type == "photo":
                                        photo_url: str = attachment["photo"]["sizes"][
                                            -1
                                        ]["url"]
                                        photo_id: int = attachment["photo"]["id"]
                                        filename: str = (
                                            f"{self.media}photo_{photo_id}.jpg"
                                        )

                                        async with session.get(photo_url) as response:
                                            if response.status == 200:
                                                with open(filename, "wb") as file:
                                                    file.write(await response.read())
                                                media_files.append(filename)

                                    if attachment_type == "video":
                                        media_files.append("video")

                                    if attachment_type == "doc":
                                        media_files.append("doc")

                                    if attachment_type == "audio":
                                        media_files.append("audio")

                                except Exception as e:
                                    print(
                                        f"Ошибка при обработке вложения: {attachment_type}"
                                    )
                                    print(f"Ошибка: {e}")

                        dataset.append(
                            Post(
                                id=post_id,
                                text=text,
                                date=date,
                                is_repost=is_repost,
                                media_files=media_files,
                            )
                        )

                    offset += 100

            print(dataset)
            return dataset

        except vk_api.exceptions.ApiError as e:
            print(f"Произошла ошибка при получении постов из группы. Ошибка: {e}")

    async def vk_request(
        self, session: aiohttp.ClientSession, method: str, **kwargs
    ) -> Dict:
        url = f"https://api.vk.com/method/{method}"
        params = {"access_token": os.getenv("VK_ACCESS_TOKEN"), "v": "5.131", **kwargs}

        async with session.post(url, params=params) as response:
            response_data = await response.json()

            if "error" in response_data:
                raise vk_api.exceptions.ApiError(response_data["error"])

            return response_data["response"]

    async def parse_until_date(
        self, until_date: datetime.datetime, target: int | str
    ) -> None:
        dt = VKGroupParser.datetime_to_timestamp(dt_str=until_date)
        await self.parse_posts(target=target, until_date=dt)

    async def parse_until_id(self, until_id: int, target: int | str) -> None:
        await self.parse_posts(target=target, last_postId=until_id)

    async def parse_all(self, target) -> None:
        await self.parse_posts(target=target)

    @staticmethod
    def datetime_to_timestamp(dt_str):
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = dt - epoch
        return int(delta.total_seconds())
