import json
import requests
import re
from .models import Author
from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth


class ChannelInfo:

    """
    Youtube channel info.

    @param str title: channel title
    @param str video_id: channel id
    @param str description: channel description
    @param str small_thumbnail: small channel thumbnail
    @param str medium_thumbnail: medium channel thumbnail
    @param str high_thumbnail: high channel thumbnail
    @param str standard_thumbnail: standard channel thumbnail
    @param str max_thumbnail: max channel thumbnail
    @param str google_plus_id: channel owner`s google id


    """
    __slots__ = [
        'title', 'channel_id', 'description',
        'medium_thumbnail', 'high_thumbnail',
        'google_plus_id'
    ]

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


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
        'title', 'video_id', 'description',
        'small_thumbnail', 'medium_thumbnail', 'high_thumbnail',
        'standard_thumbnail', 'max_thumbnail', 'author'
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
    data = json.loads(r.text)
    into_items = data['items'][0]
    into_snippet_thumbnail = into_items['snippet']['thumbnails']
    into_items_snippet = into_items['snippet']
    return ChannelInfo(
        title=into_items_snippet['title'],
        channel_id=into_items['id'],
        description=into_items_snippet['description'],
        medium_thumbnail=into_snippet_thumbnail['medium']['url'],
        high_thumbnail=into_snippet_thumbnail['high']['url'],
        google_plus_id=into_items['contentDetails']['googlePlusUserId']
    )


def get_user_for_video_author(google_uid):
    try:
        return UserSocialAuth.objects.get(uid=google_uid).user
    except UserSocialAuth.DoesNotExist:
        return None


def get_author_of_video(channel_id):
    channel_info = get_channel_info(channel_id)
    try:
        return Author.objects.get(google_uid=channel_info.google_plus_id)
    except Author.DoesNotExist:
        return Author.objects.create(
            google_uid=channel_info.google_plus_id,
            user=get_user_for_video_author(
                channel_info.google_plus_id),
            name=channel_info.title,
            avatar_url=channel_info.medium_thumbnail
        )


def get_video_id(url):
    regexp = (
        r'http(s)?://(www\.)?youtu(.)?be(/)?(.com/watch\?v=)?(?P<video_id>.+)'
    )
    match = re.match(regexp, url)
    video_id = match.group('video_id')
    return video_id


def get_video_json(video_id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos?\
part=snippet&id={video_id}&key={GOOGLE_API_KEY}'
    json_url = video_url.format(
        video_id=str(video_id),
        GOOGLE_API_KEY=str(settings.GOOGLE_API_KEY)
    )
    r = requests.get(json_url)
    data = json.loads(r.text)
    return data


def get_video_info(url):
    video_id = get_video_id(url)
    data = get_video_json(video_id)
    into_items = data['items'][0]
    channel_id = into_items['snippet']['channelId']
    into_snippet_thumbnail = into_items['snippet']['thumbnails']
    into_items_snippet = into_items['snippet']

    return VideoInfo(
        title=into_items_snippet['title'],
        video_id=into_items['id'],
        description=into_items_snippet['description'],
        small_thumbnail=into_snippet_thumbnail['default']['url'],
        medium_thumbnail=into_snippet_thumbnail['medium']['url'],
        high_thumbnail=into_snippet_thumbnail['high']['url'],
        standard_thumbnail=into_snippet_thumbnail['standard']['url'],
        max_thumbnail=into_snippet_thumbnail['maxres']['url'],
        author=get_author_of_video(channel_id)
    )

get_video_info('https://youtu.be/yYfYVB1e988')
