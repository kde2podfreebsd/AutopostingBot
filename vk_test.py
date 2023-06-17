import vk_api
import requests
import os
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv
import requests

load_dotenv()


class VKGroupParser:
    def __init__(self, access_token: str, group_id: int):
        self.vk_session = vk_api.VkApi(token=access_token)
        self.vk = self.vk_session.get_api()
        self.vk_upload = vk_api.VkUpload(vk=self.vk)
        self.group_id = group_id

    def parse_posts(self, last_post_id: Optional[int] = None) -> None:
        try:
            offset = 0
            dataset = []

            flag = True

            while flag:
                posts = self.vk.wall.get(owner_id='-' + str(self.group_id), count=100, offset=offset)
                if 'items' not in posts:
                    break

                for post in posts['items']:
                    post_id: int = post['id']
                    if last_post_id is not None and post_id <= last_post_id:
                        flag = False
                        continue

                    text: str = post['text']
                    date: int = post['date']
                    is_repost: bool = 'copy_history' in post
                    media_files: List[str] = []

                    print("\n\n\n","POST STRUCT:",post, end="\n\n\n")

                    if 'attachments' in post:
                        # print(post)
                        # self.vk.video.get(videos=)

                        for attachment in post['attachments']:
                            attachment_type: str = attachment['type']

                            try:
                                # if attachment_type == 'photo':
                                #     # print(attachment)
                                #     photo_url: str = attachment['photo']['sizes'][-1]['url']
                                #     photo_id: int = attachment['photo']['id']
                                #     filename: str = f'media/photo_{photo_id}.jpg'
                                #     response = requests.get(photo_url)
                                #
                                #     if response.status_code == 200:
                                #         with open(filename, 'wb') as file:
                                #             file.write(response.content)
                                #         media_files.append(filename)

                                if attachment_type == 'video':
                                    print(attachment['video']['id'])
                                    video_attachment = post['attachments'][0]['video']  # Получаем информацию о видео
                                    video_url = video_attachment['photo_1280']  # Выбираем разрешение 1280

                                    print(f'URL видео: {video_url}')
                                    response = requests.get(video_url, stream=True)
                                    if response.status_code == 200:
                                        # Определение имени файла на основе URL
                                        file_name = f'media/{attachment["video"]["id"]}.mp4'


                                        # # Сохранение видео на диск
                                        with open(file_name, 'wb') as file:
                                            for chunk in response.iter_content(1024):
                                                file.write(chunk)

                                        print(f'Видео сохранено в файл: {file_name}')
                                    else:
                                        print('Ошибка при загрузке видео.')

                                    # video_file = self.vk_upload.video(video_url)
                                    # video_file_path = f"media/{attachment['video']['id']}.mp4"
                                    # video_file.save(video_file_path)
                                    #
                                    # print(f'Видео сохранено в файл: {video_file_path}')

                                # elif attachment_type == 'doc' and attachment['doc']['type'] == 3:
                                #     gif_id: int = attachment['doc']['id']
                                #     filename: str = f'media/gif_{gif_id}.gif'
                                #     gif_url: str = attachment['doc']['url']
                                #     response = requests.get(gif_url)
                                #
                                #     if response.status_code == 200:
                                #         with open(filename, 'wb') as file:
                                #             file.write(response.content)
                                #         media_files.append(filename)

                            except Exception as e:
                                print(f'Ошибка при обработке вложения: {attachment_type}')
                                print(f'Ошибка: {e}')

                    dataset.append({'id': post_id, 'text': text, 'date': date, 'is_repost': is_repost,
                                    'media_files': media_files})

                offset += 100

            for data in dataset:
                print('ID:', data['id'])
                print('Text:', data['text'])
                print('Date:', data['date'])
                print('Is Repost:', data['is_repost'])
                print('Media files:', data['media_files'])

            print(len(dataset))

        except vk_api.exceptions.ApiError as e:
            print(f'Произошла ошибка при получении постов из группы. Ошибка: {e}')

    def parse_new_posts(self, last_post_id: int) -> None:
        self.parse_posts(last_post_id)


def getLastPostId():
    return 330124


# access_token: str = ''
access_token: str = str(os.getenv("VK_ACCESS_TOKEN"))
# print(access_token)
group_url: str = 'https://vk.com/roflwolf'
last_post_id: int = getLastPostId()  # Получение последнего id поста для этой группы из базы данных
group_id = "201880129"

parser: VKGroupParser = VKGroupParser(access_token, group_id)
# parser.parse_new_posts(last_post_id)
# parser.parse_posts()
parser.parse_new_posts(last_post_id=last_post_id)
