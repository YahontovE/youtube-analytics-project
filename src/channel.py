import os
from googleapiclient.discovery import build
import isodate
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YouTube-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        get_channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = get_channel['items'][0]['snippet']['title']
        self.video_count = get_channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/channel/{get_channel['items'][0]['id']}"
        self.description = get_channel['items'][0]['snippet']['description']
        self.subscriber_count = get_channel['items'][0]['statistics']['subscriberCount']
        self.view_count = get_channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self,path):
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(f'Информация о канале:\nНазвание {self.title}\nКол-во видео {self.video_count}\n'
                            f'URL {self.url}\nОписание {self.description}\nКол-во подписчиков {self.subscriber_count}\n'
                            f'Кол-во просмотров {self.view_count}')
            return file

    @property
    def channel_id(self):
        return self.__channel_id





