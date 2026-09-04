"""Provider registry — dispatches a URL to the first provider that claims it."""

from urllib.parse import urlparse

from yubal.models.enums import Source
from yubal.providers.base import SourceProvider
from yubal.providers.soundcloud import SoundCloudProvider
from yubal.providers.youtube_music import YouTubeMusicProvider

_PROVIDERS: tuple[SourceProvider, ...] = (YouTubeMusicProvider(), SoundCloudProvider())

_MUSIC_YOUTUBE_HOSTS = {"music.youtube.com"}


def get_provider(url: str) -> SourceProvider | None:
    """Return the first registered provider that claims this URL, or None."""
    for provider in _PROVIDERS:
        if provider.match(url) is not None:
            return provider
    return None


def is_supported_url(url: str) -> bool:
    """Whether any registered provider can handle this URL."""
    return get_provider(url) is not None


def classify_source(url: str) -> Source | None:
    """Classify a URL's user-facing platform, or None if unsupported.

    Display-only distinction: YouTube Music and plain YouTube both route
    through the same YouTubeMusicProvider/extraction pipeline (plain YouTube
    just uses its UGC-fallback path) — this only decides the label users see.
    """
    provider = get_provider(url)
    if isinstance(provider, SoundCloudProvider):
        return Source.SOUNDCLOUD
    if isinstance(provider, YouTubeMusicProvider):
        host = (urlparse(url).hostname or "").lower()
        return Source.YOUTUBE_MUSIC if host in _MUSIC_YOUTUBE_HOSTS else Source.YOUTUBE
    return None
