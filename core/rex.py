import re

regexp = (
        r'http(s)?://(www\.)?youtu(.)?be(/)?(.com/watch\?v=)?(?P<video_id>.+)'
    )
match = re.match(regexp, 'https://youtu.be/NL80bM3WsYQ')
print(type(match))
video_id = match.group('video_id')
print(video_id)

'https://youtu.be/yYfYVB1e988'