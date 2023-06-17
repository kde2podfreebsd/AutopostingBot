import requests

def download_video_by_track_code(track_code, save_path):
    # Получаем информацию о видео через API ВКонтакте
    video_info_url = f"https://api.vk.com/method/video.get?videos={track_code}"
    response = requests.get(video_info_url)
    data = response.json()

    if 'response' in data and data['response'].get('items'):
        video_items = data['response']['items']
        if len(video_items) > 0:
            # Получаем URL видео из ответа API
            video_url = video_items[0]['player']
            # Скачиваем видео
            response = requests.get(video_url)
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Видео успешно скачано!")
        else:
            print("Видео не найдено.")
    else:
        print("Ошибка при получении информации о видео.")

# Пример использования функции
track_code = 'video_2689f0c9UXYA3O80vxHcULolXP5-rjs7C3rJ7ZyHhxH2ggODQ3pjWhXe7je-dt9SuC47_kuYCQ86Q_zZmPDmfZqCEq5xSg'
save_path = 'path_to_save_video/video.mp4'
download_video_by_track_code(track_code, save_path)