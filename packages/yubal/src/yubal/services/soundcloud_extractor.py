"""SoundCloud metadata extraction via yt-dlp directly (no catalog API).

Unlike MetadataExtractorService (YouTube Music via ytmusicapi), SoundCloud
has no separate metadata API — yt-dlp's own info-dict IS the metadata
source. Field mapping mirrors yt-dlp's own FFmpegMetadataPP fallback
chain: title <- (track, title), artist <- (artists, artist, uploader),
track_number <- (track_number, playlist_index) since SoundCloud has no
native track-number field.
"""

import logging
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import yt_dlp

from yubal.exceptions import CancellationError
from yubal.models.cancel import CancelToken
from yubal.models.enums import ContentKind, MatchResult
from yubal.models.progress import ExtractProgress
from yubal.models.track import PlaylistInfo, TrackMetadata

logger = logging.getLogger(__name__)


class SoundCloudExtractorService:
    """Extracts track/playlist metadata from SoundCloud URLs via yt-dlp."""

    def extract(
        self,
        url: str,
        max_items: int | None = None,
        cancel_token: CancelToken | None = None,
        cache: object | None = None,  # unused — no extraction cache for SoundCloud yet
    ) -> Iterator[ExtractProgress]:
        """Extract metadata for a SoundCloud track, set/album, or user-likes URL.

        Args:
            url: SoundCloud track, set, album, or `<user>/likes` URL.
            max_items: Maximum number of tracks to extract (None for all).
            cancel_token: Optional cancellation token.
            cache: Unused (accepted for interface parity with
                MetadataExtractorService.extract).

        Yields:
            ExtractProgress, one per extracted track (or a single empty
            progress if the URL yields nothing).
        """
        try:
            info = self.fetch_info(url)
        except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as e:
            logger.warning("SoundCloud extraction failed for %s: %s", url, e)
            info = None

        if info is None:
            yield ExtractProgress(
                current=0,
                total=0,
                playlist_total=0,
                track=None,
                playlist_info=PlaylistInfo(playlist_id="", kind=ContentKind.PLAYLIST),
            )
            return

        if info.get("_type") == "playlist":
            yield from self._extract_playlist(info, max_items, cancel_token)
        else:
            yield from self._extract_single_track(info)

    def fetch_info(self, url: str) -> dict[str, Any] | None:
        """Fetch yt-dlp's raw info-dict for a URL (public — reused by callers
        that only need top-level fields, e.g. a content-info preview,
        without the full track-by-track extraction below).
        """
        opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "ignoreerrors": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)

    def _extract_playlist(
        self,
        info: dict[str, Any],
        max_items: int | None,
        cancel_token: CancelToken | None,
    ) -> Iterator[ExtractProgress]:
        entries = [e for e in (info.get("entries") or []) if e]
        playlist_total = len(entries)
        if max_items is not None:
            entries = entries[:max_items]

        kind = (
            ContentKind.ALBUM
            if info.get("album_type") == "album"
            else ContentKind.PLAYLIST
        )
        cover_url = info.get("thumbnail") or next(
            (e.get("thumbnail") for e in entries if e.get("thumbnail")), None
        )
        playlist_info = PlaylistInfo(
            playlist_id=str(info.get("id") or ""),
            title=info.get("title"),
            cover_url=cover_url,
            kind=kind,
            author=info.get("uploader"),
        )

        total_tracks = len(entries) if kind == ContentKind.ALBUM else None
        current = 0
        for entry in entries:
            if cancel_token and cancel_token.is_cancelled:
                raise CancellationError("Extraction cancelled")

            track = self._entry_to_track(entry, total_tracks=total_tracks)
            if track is None:
                continue

            current += 1
            yield ExtractProgress(
                current=current,
                total=len(entries),
                playlist_total=playlist_total,
                track=track,
                playlist_info=playlist_info,
            )

        if current == 0:
            yield ExtractProgress(
                current=0,
                total=0,
                playlist_total=playlist_total,
                track=None,
                playlist_info=playlist_info,
            )

    def _extract_single_track(self, info: dict[str, Any]) -> Iterator[ExtractProgress]:
        track = self._entry_to_track(info, total_tracks=None)
        playlist_info = PlaylistInfo(
            playlist_id=str(info.get("id") or ""),
            title=info.get("title"),
            cover_url=info.get("thumbnail"),
            kind=ContentKind.TRACK,
            author=info.get("uploader"),
        )
        yield ExtractProgress(
            current=1 if track else 0,
            total=1,
            playlist_total=1,
            track=track,
            playlist_info=playlist_info,
        )

    def _entry_to_track(
        self, entry: dict[str, Any], *, total_tracks: int | None
    ) -> TrackMetadata | None:
        """Map a yt-dlp SoundCloud info-dict entry to TrackMetadata.

        Returns None for entries missing the minimum required fields
        (id, webpage_url, title) — e.g. DRM-restricted tracks yt-dlp
        could not fully resolve even with ignoreerrors.
        """
        video_id = entry.get("id")
        webpage_url = entry.get("webpage_url")
        title = entry.get("track") or entry.get("title")
        if not video_id or not webpage_url or not title:
            return None

        raw_artists = entry.get("artists")
        artists: list[str] = (
            [str(a) for a in raw_artists if a]
            if isinstance(raw_artists, list) and raw_artists
            else []
        )
        if not artists and entry.get("artist"):
            artists = [str(entry["artist"])]
        if not artists and entry.get("uploader"):
            artists = [str(entry["uploader"])]
        if not artists:
            artists = ["Unknown Artist"]

        has_album = bool(entry.get("album"))
        album = str(entry.get("album") or title)
        album_artist = entry.get("album_artist")
        album_artists: list[str] = [str(album_artist)] if album_artist else artists

        return TrackMetadata(
            source_video_id=str(video_id),
            download_url=webpage_url,
            title=title,
            artists=artists,
            album=album,
            album_artists=album_artists,
            track_number=entry.get("track_number") or entry.get("playlist_index"),
            total_tracks=total_tracks if has_album else None,
            year=self._extract_year(entry),
            cover_url=entry.get("thumbnail"),
            duration_seconds=(
                int(entry["duration"]) if entry.get("duration") else None
            ),
            match_result=MatchResult.MATCHED if has_album else MatchResult.UNOFFICIAL,
        )

    def _extract_year(self, entry: dict[str, Any]) -> str | None:
        timestamp = entry.get("release_timestamp") or entry.get("timestamp")
        if not timestamp:
            return None
        return str(datetime.fromtimestamp(timestamp, tz=UTC).year)
