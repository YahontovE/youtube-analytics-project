import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YouTube-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        video_response = self.youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        self.video_id = video_id
        try:
            self.title = video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
        try:
            self.video_url = f"https://www.youtube.com/video/{video_response['items'][0]['id']}"
        except IndexError:
            self.video_url = None
        try:
            self.viewCount = video_response['items'][0]['statistics']['viewCount']
        except IndexError:
            self.viewCount = None
        try:
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        video_response = self.youtube.videos().list(part='snippet,statistics', id=self.video_id).execute()
        return video_response


class PLVideo(Video):

    def __init__(self, video_id, playList_id):
        super().__init__(video_id)
        self.playList_id = playList_id
