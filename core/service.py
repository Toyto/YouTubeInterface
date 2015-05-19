import json
import requests
import re
from .models import Author
from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth


class VideoInfo:

    """
    Youtube video info.

    @param str title: video title
    @param str video_id: video id
    @param str description: video description
    @param str small_thumbnail: small video thumbnail
    @param str medium_thumbnail: medium video thumbnail
    @param str high_thumbnail: high video thumbnail
    @param str standard_thumbnail: standard video thumbnail
    @param str max_thumbnail: max video thumbnail
    @param core.models.Author author: Author object

    """
    __slots__ = [
        'title', 'video_id', 'description', 'small_thumbnail',
        'medium_thumbnail', 'high_thumbnail', 'standard_thumbnail',
        'max_thumbnail', 'author'
    ]

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


def get_channel_info(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels?\
part=contentDetails%2C+snippet&id=\
{channel_id}&key={GOOGLE_API_KEY}'
    json_url = url.format(
        channel_id=str(channel_id),
        GOOGLE_API_KEY=str(settings.GOOGLE_API_KEY)
    )
    r = requests.get(json_url)
    # Convert it to a Python dictionary
    data_channel = json.loads(r.text)
    return data_channel


def user_object(google_plus_id):
    user_obj = UserSocialAuth.objects.filter(uid=google_plus_id)
    return user_obj


def get_video_info(url):
    regexp = r'http(s)?://(www\.)?youtube\.com/watch\?v=(?P<video_id>.+)'
    match = re.match(regexp, url)
    video_id = match.group('video_id')
    video_url = 'https://www.googleapis.com/youtube/v3/videos?\
part=snippet&id={video_id}&key={GOOGLE_API_KEY}'
    json_url = video_url.format(
        video_id=str(video_id),
        GOOGLE_API_KEY=str(settings.GOOGLE_API_KEY)
    )
    print(json_url)
    r = requests.get(json_url)
    # Convert it to a Python dictionary
    data = json.loads(r.text)
    # Loop through the result.
    into_items = data['items'][0]
    channel_id = into_items['snippet']['channelId']
    channel_info = get_channel_info(channel_id)
    into_snippet_thumbnail = into_items['snippet']['thumbnails']
    into_items_snippet = into_items['snippet']
    channel_items = channel_info['items'][0]
    google_plus_id = channel_items['contentDetails']['googlePlusUserId']
    into_channel_items_thumbnail = channel_items['snippet']['thumbnails']

    return VideoInfo(
        title=into_items_snippet['title'],
        video_id=into_items['id'],
        description=into_items_snippet['description'],
        small_thumbnail=into_snippet_thumbnail['default']['url'],
        medium_thumbnail=into_snippet_thumbnail['medium']['url'],
        high_thumbnail=into_snippet_thumbnail['high']['url'],
        standard_thumbnail=into_snippet_thumbnail['standard']['url'],
        max_thumbnail=into_snippet_thumbnail['maxres']['url'],
        author=Author.objects.get_or_create(
            name=into_items_snippet['channelTitle'],
            avatar_url=into_channel_items_thumbnail
            ['medium']['url'],
            defaults={'user': user_object(google_plus_id)}
        )
    )
