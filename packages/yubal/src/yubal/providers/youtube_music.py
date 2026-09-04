"""YouTube Music provider.

Wraps the existing regex-based URL parsing in ``yubal.utils.url`` — no
parsing logic duplicated or changed here, just adapted to the
``SourceProvider`` shape.
"""

from yubal.providers.base import UrlMatch
from yubal.utils.url import is_supported_url, parse_playlist_id, parse_video_id

YOUTUBE_MUSIC_WATCH_URL = "https://music.youtube.com/watch?v={video_id}"


class YouTubeMusicProvider:
    """Provider for music.youtube.com / youtube.com URLs (existing behavior)."""

    name = "youtube_music"

    def match(self, url: str) -> UrlMatch | None:
        if not is_supported_url(url):
            return None
        if video_id := parse_video_id(url):
            return UrlMatch(kind="track", content_id=video_id)
        return UrlMatch(kind="playlist", content_id=parse_playlist_id(url))

    def resolve_download_url(self, video_id: str) -> str:
        return YOUTUBE_MUSIC_WATCH_URL.format(video_id=video_id)
