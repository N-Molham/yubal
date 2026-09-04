"""Provider protocol and match result shared by every source."""

from dataclasses import dataclass
from typing import Literal, Protocol

ContentKind = Literal["track", "playlist"]


@dataclass(frozen=True)
class UrlMatch:
    """Result of a provider claiming a URL.

    kind: whether the URL points at a single track or a playlist/album.
    content_id: the source-native ID extracted from the URL (video ID,
        playlist ID, SoundCloud track/set path, etc).
    """

    kind: ContentKind
    content_id: str


class SourceProvider(Protocol):
    """One yt-dlp-backed source (YouTube Music, YouTube, SoundCloud, ...).

    A provider owns URL recognition/parsing and knows how to turn a
    source-native content ID back into a URL yt-dlp can download.
    """

    name: str

    def match(self, url: str) -> UrlMatch | None:
        """Return a UrlMatch if this provider handles the URL, else None."""
        ...

    def resolve_download_url(self, video_id: str) -> str:
        """Build the URL yt-dlp should download for a given content ID."""
        ...
