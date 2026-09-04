"""Tests for SoundCloudExtractorService.

Uses canned yt-dlp info-dicts (captured from real extractions) rather than
hitting the network, mirroring how test_download_service.py mocks yt-dlp.
"""

from unittest.mock import patch

from yubal.models.enums import ContentKind, MatchResult
from yubal.services.soundcloud_extractor import SoundCloudExtractorService

# Shape captured from a real single-track extraction (soundcloud.com/.../mezzo-valzer)
SINGLE_TRACK_INFO = {
    "_type": "video",
    "id": "583011102",
    "title": "Mezzo Valzer",
    "track": "Mezzo Valzer",
    "uploader": "Giovanni Sarani",
    "artists": None,
    "artist": None,
    "album": None,
    "album_artist": None,
    "album_type": None,
    "track_number": None,
    "timestamp": 1551394171,
    "duration": 180.134,
    "thumbnail": "https://i1.sndcdn.com/artworks-original.jpg",
    "webpage_url": "https://soundcloud.com/giovannisarani/mezzo-valzer",
}

# Shape captured from a real set extraction (soundcloud.com/.../sets/out-of-spite)
SET_INFO = {
    "_type": "playlist",
    "id": "1524158182",
    "title": "out of spite",
    "uploader": "Levi Ryan",
    "thumbnail": None,
    "album_type": "album",
    "entries": [
        {
            "id": "1378985008",
            "title": "crackshot w/gl0wrm",
            "track": "crackshot w/gl0wrm",
            "uploader": "Levi Ryan",
            "artists": ["Levi Ryan"],
            "artist": "Levi Ryan",
            "album": "out of spite",
            "album_artist": "Levi Ryan",
            "album_type": "album",
            "track_number": None,
            "playlist_index": 1,
            "timestamp": 1667935703,
            "duration": 207.614,
            "thumbnail": "https://i1.sndcdn.com/artworks-1.jpg",
            "webpage_url": "https://soundcloud.com/leviryan/crackshot-wgl0wrm",
        },
        {
            "id": "1378983277",
            "title": "matrix w/david shawty",
            "track": "matrix w/david shawty",
            "uploader": "Levi Ryan",
            "artists": ["Levi Ryan"],
            "artist": "Levi Ryan",
            "album": "out of spite",
            "album_artist": "Levi Ryan",
            "album_type": "album",
            "track_number": None,
            "playlist_index": 2,
            "timestamp": 1667935488,
            "duration": 183.969,
            "thumbnail": "https://i1.sndcdn.com/artworks-2.jpg",
            "webpage_url": "https://soundcloud.com/leviryan/matrix-wdavid-shawty",
        },
        # yt-dlp's ignoreerrors=True replaces a failed entry (e.g. DRM) with
        # a literal None in the entries list — must be skipped, not crash.
        None,
    ],
}


class TestExtractSingleTrack:
    def test_maps_standalone_track_to_unofficial_bucket(self) -> None:
        service = SoundCloudExtractorService()
        with patch.object(service, "fetch_info", return_value=SINGLE_TRACK_INFO):
            progress = list(service.extract("https://soundcloud.com/x/mezzo-valzer"))

        assert len(progress) == 1
        track = progress[0].track
        assert track is not None
        assert track.title == "Mezzo Valzer"
        assert track.artists == ["Giovanni Sarani"]
        assert track.album == "Mezzo Valzer"  # no album -> falls back to title
        assert track.year == "2019"  # from timestamp 1551394171
        assert track.source_video_id == "583011102"
        assert (
            track.download_url == "https://soundcloud.com/giovannisarani/mezzo-valzer"
        )
        assert track.match_result == MatchResult.UNOFFICIAL
        assert progress[0].playlist_info.kind == ContentKind.TRACK

    def test_returns_empty_progress_when_extraction_fails(self) -> None:
        service = SoundCloudExtractorService()
        with patch.object(service, "fetch_info", return_value=None):
            progress = list(service.extract("https://soundcloud.com/x/gone"))

        assert len(progress) == 1
        assert progress[0].track is None
        assert progress[0].total == 0


class TestExtractSet:
    def test_maps_set_tracks_with_album_fields(self) -> None:
        service = SoundCloudExtractorService()
        with patch.object(service, "fetch_info", return_value=SET_INFO):
            progress = list(
                service.extract("https://soundcloud.com/leviryan/sets/out-of-spite")
            )

        # 3 entries in the fixture, 1 is DRM-broken and must be skipped
        assert len(progress) == 2
        first = progress[0]
        assert first.playlist_info.kind == ContentKind.ALBUM
        assert first.playlist_info.title == "out of spite"
        assert first.track is not None
        assert first.track.album == "out of spite"
        assert first.track.album_artists == ["Levi Ryan"]
        assert first.track.track_number == 1  # from playlist_index fallback
        assert first.track.match_result == MatchResult.MATCHED
        assert first.track.total_tracks == 2  # 2 usable entries, DRM one excluded

        second = progress[1]
        assert second.track is not None
        assert second.track.track_number == 2

    def test_respects_max_items(self) -> None:
        service = SoundCloudExtractorService()
        with patch.object(service, "fetch_info", return_value=SET_INFO):
            progress = list(
                service.extract(
                    "https://soundcloud.com/leviryan/sets/out-of-spite", max_items=1
                )
            )

        assert len(progress) == 1
        assert progress[0].playlist_total == 2  # true total, before max_items slice

    def test_non_album_playlist_type_maps_to_playlist_kind(self) -> None:
        likes_info = {**SET_INFO, "album_type": None}
        service = SoundCloudExtractorService()
        with patch.object(service, "fetch_info", return_value=likes_info):
            progress = list(service.extract("https://soundcloud.com/x/likes"))

        assert progress[0].playlist_info.kind == ContentKind.PLAYLIST
        assert progress[0].track is not None
        # No per-track "album" field in this fixture variant's first entry
        # is still present (inherited from SET_INFO) so match stays MATCHED;
        # total_tracks is only populated for ALBUM-kind containers.
        assert progress[0].track.total_tracks is None
