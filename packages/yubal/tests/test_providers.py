"""Tests for the source-provider abstraction."""

from yubal.models.enums import Source
from yubal.providers import UrlMatch, classify_source, get_provider, is_supported_url
from yubal.providers.youtube_music import YouTubeMusicProvider


class TestYouTubeMusicProvider:
    """Tests for YouTubeMusicProvider."""

    def test_matches_track_url(self) -> None:
        provider = YouTubeMusicProvider()
        match = provider.match("https://music.youtube.com/watch?v=Vgpv5PtWsn4")
        assert match == UrlMatch(kind="track", content_id="Vgpv5PtWsn4")

    def test_matches_playlist_url(self) -> None:
        provider = YouTubeMusicProvider()
        match = provider.match("https://music.youtube.com/playlist?list=PLtest123")
        assert match == UrlMatch(kind="playlist", content_id="PLtest123")

    def test_returns_none_for_unsupported_url(self) -> None:
        provider = YouTubeMusicProvider()
        assert provider.match("https://open.spotify.com/track/abc123") is None

    def test_returns_none_for_soundcloud_url(self) -> None:
        """SoundCloud is a different provider's territory, not YouTube Music's."""
        provider = YouTubeMusicProvider()
        assert provider.match("https://soundcloud.com/artist/track") is None

    def test_resolve_download_url_builds_watch_url(self) -> None:
        provider = YouTubeMusicProvider()
        assert provider.resolve_download_url("abc123") == (
            "https://music.youtube.com/watch?v=abc123"
        )


class TestRegistry:
    """Tests for the provider registry."""

    def test_get_provider_returns_youtube_music_for_track_url(self) -> None:
        provider = get_provider("https://music.youtube.com/watch?v=Vgpv5PtWsn4")
        assert provider is not None
        assert provider.name == "youtube_music"

    def test_get_provider_returns_soundcloud_for_soundcloud_url(self) -> None:
        provider = get_provider("https://soundcloud.com/artist/track")
        assert provider is not None
        assert provider.name == "soundcloud"

    def test_get_provider_returns_none_for_unsupported_url(self) -> None:
        assert get_provider("https://open.spotify.com/track/abc123") is None

    def test_is_supported_url_true_for_youtube_music(self) -> None:
        assert is_supported_url("https://music.youtube.com/watch?v=Vgpv5PtWsn4")

    def test_is_supported_url_true_for_soundcloud(self) -> None:
        assert is_supported_url("https://soundcloud.com/artist/track")

    def test_is_supported_url_false_for_unsupported(self) -> None:
        assert not is_supported_url("https://open.spotify.com/track/abc123")


class TestClassifySource:
    """Tests for classify_source — display-only platform labeling."""

    def test_music_youtube_host_classified_as_youtube_music(self) -> None:
        url = "https://music.youtube.com/watch?v=Vgpv5PtWsn4"
        assert classify_source(url) == Source.YOUTUBE_MUSIC

    def test_plain_youtube_host_classified_as_youtube(self) -> None:
        """Same provider/pipeline as YouTube Music, different display label."""
        url = "https://www.youtube.com/watch?v=Vgpv5PtWsn4"
        assert classify_source(url) == Source.YOUTUBE

    def test_youtu_be_classified_as_youtube(self) -> None:
        assert classify_source("https://youtu.be/Vgpv5PtWsn4") == Source.YOUTUBE

    def test_soundcloud_classified_as_soundcloud(self) -> None:
        url = "https://soundcloud.com/artist/track"
        assert classify_source(url) == Source.SOUNDCLOUD

    def test_unsupported_url_classified_as_none(self) -> None:
        assert classify_source("https://open.spotify.com/track/abc123") is None
