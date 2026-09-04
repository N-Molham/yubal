"""Enumerations for yubal domain models."""

from enum import StrEnum


class VideoType(StrEnum):
    """YouTube Music video types.

    Maps to ytmusicapi.models.content.enums.VideoType values.
    """

    ATV = "MUSIC_VIDEO_TYPE_ATV"  # Audio Track Video (album version)
    OMV = "MUSIC_VIDEO_TYPE_OMV"  # Official Music Video
    OFFICIAL_SOURCE_MUSIC = "MUSIC_VIDEO_TYPE_OFFICIAL_SOURCE_MUSIC"  # Official source
    UGC = "MUSIC_VIDEO_TYPE_UGC"  # User Generated Content
    PODCAST_EPISODE = "MUSIC_VIDEO_TYPE_PODCAST_EPISODE"  # Podcast episode


class DownloadStatus(StrEnum):
    """Status of a download operation."""

    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"


class SkipReason(StrEnum):
    """Reason why a track was skipped.

    Used in both extraction and download phases:
    - Extraction: UNSUPPORTED_VIDEO_TYPE, NO_VIDEO_ID, REGION_UNAVAILABLE
    - Download: FILE_EXISTS
    """

    FILE_EXISTS = "file_exists"
    UNSUPPORTED_VIDEO_TYPE = "unsupported_video_type"
    UGC = "ugc"
    NO_VIDEO_ID = "no_video_id"
    REGION_UNAVAILABLE = "region_unavailable"

    @property
    def label(self) -> str:
        """Human-readable label for display."""
        match self:
            case SkipReason.FILE_EXISTS:
                return "file exists"
            case SkipReason.UNSUPPORTED_VIDEO_TYPE:
                return "unsupported video type"
            case SkipReason.UGC:
                return "user-generated content (UGC)"
            case SkipReason.NO_VIDEO_ID:
                return "no video ID"
            case SkipReason.REGION_UNAVAILABLE:
                return "region unavailable"


class MatchResult(StrEnum):
    """Track matching outcome for download routing.

    Determines which folder a track is downloaded to:
    - MATCHED: Album-structured path (Artist/Year - Album/NN - Title)
    - UNMATCHED: Flat _Unmatched/ folder (OMVs with no confident album match)
    - UNOFFICIAL: Flat _Unofficial/ folder (UGC tracks with unreliable metadata)
    """

    MATCHED = "matched"
    UNMATCHED = "unmatched"
    UNOFFICIAL = "unofficial"


class ContentKind(StrEnum):
    """Type of music content (album vs playlist vs track)."""

    ALBUM = "album"
    PLAYLIST = "playlist"
    TRACK = "track"


class Source(StrEnum):
    """User-facing platform a piece of content came from.

    A display/classification concept, not a 1:1 mirror of the provider
    registry — YOUTUBE_MUSIC and YOUTUBE both route through the same
    YouTubeMusicProvider/extraction pipeline (see providers.registry), but
    users pasting a plain youtube.com link expect a "YouTube" label, not
    "YouTube Music".
    """

    YOUTUBE_MUSIC = "youtube_music"
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
