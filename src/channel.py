import os
from googleapiclient.discovery import build
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

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        '''метод для операции сложения'''
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        '''метод для операции вычитания'''
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        '''метод для операции сравнения «больше»'''
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __lt__(self, other):
        '''метод для операции сравнения «меньше»'''
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        '''метод для операции сравнения «меньше или равно»'''
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __ge__(self, other):
        '''метод для операции сравнения «больше или равно»'''
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            data = dict(title=self.title, video_count=self.video_count,
                        URL=self.url, description=self.description,
                        subscriber_count=self.subscriber_count,
                        view_count=self.view_count)
            json.dump(data, file, indent=2, ensure_ascii=False)
            return file

    @property
    def channel_id(self):
        return self.__channel_id
