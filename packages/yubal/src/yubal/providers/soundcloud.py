"""SoundCloud provider.

Unlike YouTube Music, SoundCloud has no catalog API — the URL itself is
already the yt-dlp-downloadable identifier, so ``resolve_download_url``
is an identity passthrough.
"""

from urllib.parse import urlparse

from yubal.providers.base import UrlMatch

_SOUNDCLOUD_HOSTS = {"soundcloud.com", "www.soundcloud.com", "m.soundcloud.com"}

# First path segment on soundcloud.com that is a site feature, not a
# user profile (so e.g. /discover/... never gets treated as a track).
_NON_CONTENT_SEGMENTS = {
    "discover",
    "search",
    "you",
    "upload",
    "stream",
    "charts",
    "backstage",
    "pro",
    "creators",
}


class SoundCloudProvider:
    """Provider for soundcloud.com track, set/album, and user-likes URLs."""

    name = "soundcloud"

    def match(self, url: str) -> UrlMatch | None:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host not in _SOUNDCLOUD_HOSTS:
            return None

        segments = [s for s in parsed.path.split("/") if s]
        if not segments or segments[0] in _NON_CONTENT_SEGMENTS:
            return None

        # /<user>/sets/<slug> or /<user>/albums/<slug> — a set/album/playlist
        if len(segments) >= 3 and segments[1] in ("sets", "albums"):
            return UrlMatch(kind="playlist", content_id=url)

        # /<user>/likes — the user's liked tracks, usable as a sync source
        if len(segments) == 2 and segments[1] == "likes":
            return UrlMatch(kind="playlist", content_id=url)

        # /<user>/<track-slug> — a single track
        if len(segments) == 2:
            return UrlMatch(kind="track", content_id=url)

        return None

    def resolve_download_url(self, video_id: str) -> str:
        # video_id here is already the track's canonical URL (see
        # SoundCloudExtractorService — TrackMetadata.download_url).
        return video_id
