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
        self.vk: vk_api.VkApiMethod = self.vk_session.get_api()
        self.vk_upload: vk_api.VkUpload = vk_api.VkUpload(vk=self.vk)
        self.media: str = f"{os.path.abspath(os.path.dirname(__file__))}/../../media/"

    async def parse_posts(
        self,
        target: Union[int, str],
        until_postId: Optional[int] = None,
        until_date: Optional[int] = None,
    ) -> List[Post]:
        """
        Основной метод парсинга ВКонтакте

        Args:
            target (int | str): ID или короткое имя группы.
            until_postId (int, optional): ID последнего поста, до которого парсить посты. Defaults to None.
            until_date (int, optional): Дата, до которой парсить посты (timestamp). Defaults to None.

        Returns:
            List[Post]: Список объектов Post, представляющих посты.
        """
        try:
            offset: int = 0
            dataset: List[Post] = []
            flag: bool = True

            async with aiohttp.ClientSession() as session:
                while flag:
                    posts: Dict = await self.vk_request(
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
                        if until_postId is not None and post_id < until_postId:
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
                                media_group_id=None,
                                caption=None,
                                reply_to_message_id=None,
                            )
                        )

                    offset += 100

            for data in dataset:
                print(data, end="\n\n")
            return dataset

        except vk_api.exceptions.ApiError as e:
            print(f"Произошла ошибка при получении постов из группы. Ошибка: {e}")

    async def vk_request(
        self, session: aiohttp.ClientSession, method: str, **kwargs
    ) -> Dict:
        """
        VK API Async middleware

        Args:
            session (aiohttp.ClientSession): Сессия aiohttp.
            method (str): Название метода VK API.
            **kwargs: Дополнительные параметры для запроса.

        Returns:
            Dict: Ответ от VK API в виде словаря.
        """
        url: str = f"https://api.vk.com/method/{method}"
        params: Dict = {
            "access_token": os.getenv("VK_ACCESS_TOKEN"),
            "v": "5.131",
            **kwargs,
        }

        async with session.post(url, params=params) as response:
            response_data: Dict = await response.json()

            if "error" in response_data:
                raise vk_api.exceptions.ApiError(response_data["error"])

            return response_data["response"]

    async def parse_until_date(
        self, until_date: datetime.datetime, target: Union[int, str]
    ) -> None:
        """
        Парсит посты из группы ВКонтакте до указанной даты.

        Args:
            until_date (datetime.datetime): Дата, до которой парсить посты.
            target (int | str): ID или короткое имя группы.
        """
        dt: int = VKGroupParser.datetime_to_timestamp(dt_str=until_date)
        await self.parse_posts(target=target, until_date=dt)

    async def parse_until_id(self, until_id: int, target: Union[int, str]) -> None:
        """
        Парсит посты из группы ВКонтакте до указанного ID поста.

        Args:
            until_id (int): ID поста, до которого парсить посты.
            target (int | str): ID или короткое имя группы.
        """
        await self.parse_posts(target=target, until_postId=until_id)

    async def parse_all(self, target: Union[int, str]) -> None:
        """
        Парсит все посты из группы ВКонтакте до самого начала

        Args:
            target (int | str): ID или короткое имя группы.
        """
        await self.parse_posts(target=target)

    @staticmethod
    def datetime_to_timestamp(dt_str: str) -> int:
        """
        Преобразует объект datetime.datetime в timestamp.

        Args:
            dt_str (str): Строка с датой и временем в формате "%Y-%m-%d %H:%M:%S".

        Returns:
            int: Значение timestamp.
        """
        dt: datetime.datetime = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        epoch: datetime.datetime = datetime.datetime.utcfromtimestamp(0)
        delta: datetime.timedelta = dt - epoch
        return int(delta.total_seconds())
