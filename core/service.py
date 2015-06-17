import json
import requests
import re
from .models import Author, Video, Category
from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



_API_URL = 'https://www.googleapis.com/youtube/v3'


class ChannelInfo:
    """
    Youtube channel info.

    @param str title: channel title
    @param str channel_id: channel id
    @param str description: channel description
    @param str medium_thumbnail: medium channel thumbnail
    @param str high_thumbnail: high channel thumbnail
    @param str | None standard_thumbnail: standard channel thumbnail
    @param str | None max_thumbnail: max channel thumbnail
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

    def __str__(self):
        return '<{0} {1}>'.format(
            type(self).__name__,
            {k: getattr(self, k) for k in self.__slots__}

        )


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
    @param int likes_count: video likes
    @param int dislikes_count: video dislikes
    @param int view_count: video views



    """
    __slots__ = [
        'title', 'video_id', 'description',
        'small_thumbnail', 'medium_thumbnail', 'high_thumbnail',
        'standard_thumbnail', 'max_thumbnail', 'author',
        'likes_count', 'dislikes_count', 'view_count'
    ]

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return '<{0} {1}>'.format(
            type(self).__name__,
            {k: getattr(self, k) for k in self.__slots__}

        )


def get_channel_info(channel_id):
    """
    Returns info by given channel id using YouTube Data API V3

    @param str channel_id: UCZVQF_796_ZqqEu48j7tnBg
    @rtype: ChannelInfo
    """
    url = (
        _API_URL +
        '/channels?part=contentDetails%2C+snippet'
        '&id={channel_id}'
        '&key={GOOGLE_API_KEY}'
    )
    json_url = url.format(
        channel_id=str(channel_id),
        GOOGLE_API_KEY=str(settings.GOOGLE_API_KEY)
    )

    data = json.loads(requests.get(json_url).text)
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
            name=channel_info.title,
            avatar_url=channel_info.medium_thumbnail,
            user=get_user_for_video_author(channel_info.google_plus_id),
            channel_id=channel_id
        )


def get_video_id(url):
    regexp = (
        r'http(s)?://(www\.)?youtu(.)?be(/)?(.com/watch\?v=)?(?P<video_id>.+)'
    )
    match = re.match(regexp, url)
    video_id = match.group('video_id')
    return video_id


def get_video_json(video_id):
    url = (
        _API_URL +
        '/videos?part=snippet%2C+statistics'
        '&id={video_id}'
        '&key={GOOGLE_API_KEY}'
    )
    json_url = url.format(
        video_id=str(video_id),
        GOOGLE_API_KEY=str(settings.GOOGLE_API_KEY)
    )
    data = json.loads(requests.get(json_url).text)
    return data

def get_video_rating(likes_count, dislikes_count):
    """
    Returns integer in range [1..4] representing video's rating where
    1 is the worst and 4 is the best.
    """
    likes_count = int(likes_count)
    dislikes_count = int(dislikes_count)
    ratio = likes_count / (likes_count + dislikes_count)
    if ratio < 0.5:
        return 1
    elif ratio < 0.7:
        return 2
    elif ratio < 0.9:
        return 3
    else:
        return 4

def get_category_videos(category, a=4):
    videos = Video.objects.filter(categories=category)
    return {
        'category': category,
        'videos': videos[0:a]
    }

def get_video_info(url):
    """
    Returns info by given video url using YouTube Data API V3

    @param str url: valid YouTube video url
    @rtype: VideoInfo
    """
    video_id = get_video_id(url)
    data = get_video_json(video_id)
    into_items = data['items'][0]
    channel_id = into_items['snippet']['channelId']
    into_snippet_thumbnail = into_items['snippet']['thumbnails']
    into_items_snippet = into_items['snippet']
    likes_count = into_items['statistics']['likeCount']
    dislikes_count = into_items['statistics']['dislikeCount']
    view_count = into_items['statistics']['viewCount']

    return VideoInfo(
        title=into_items_snippet['title'],
        video_id=into_items['id'],
        description=into_items_snippet['description'],
        small_thumbnail=into_snippet_thumbnail['default']['url'],
        medium_thumbnail=into_snippet_thumbnail['medium']['url'],
        high_thumbnail=into_snippet_thumbnail['high']['url'],
        standard_thumbnail=into_snippet_thumbnail.get('standard', {}).get('url'),
        max_thumbnail=into_snippet_thumbnail.get('maxres', {}).get('url'),
        author=get_author_of_video(channel_id),
        likes_count=likes_count,
        dislikes_count=dislikes_count,
        view_count=view_count
    )
