import os

import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YouTube-API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_PlayList):
        playlist_videos = self.youtube.playlists().list(part='snippet', id=id_PlayList).execute()
        self.id_PlayList = id_PlayList
        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_videos['items'][0]['id']}"

    def show_best_video(self):
        '''возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)'''
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id_PlayList, part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        total = 0
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > total:
                total = int(video['statistics']['likeCount'])
                best_like_video = f"https://youtu.be/{video['id']}"
        return best_like_video

    def total_duration1(self):
        '''возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
         (обращение как к свойству, использовать @property)'''
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id_PlayList, part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        d1 = timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            d1 += duration
            # print(video)
        # print(video_response)
        return d1

    @property
    def total_duration(self):
        return self.total_duration1()

