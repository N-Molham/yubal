"""Provider registry — dispatches a URL to the first provider that claims it."""

from yubal.providers.base import SourceProvider
from yubal.providers.youtube_music import YouTubeMusicProvider

_PROVIDERS: tuple[SourceProvider, ...] = (YouTubeMusicProvider(),)


def get_provider(url: str) -> SourceProvider | None:
    """Return the first registered provider that claims this URL, or None."""
    for provider in _PROVIDERS:
        if provider.match(url) is not None:
            return provider
    return None


def is_supported_url(url: str) -> bool:
    """Whether any registered provider can handle this URL."""
    return get_provider(url) is not None
