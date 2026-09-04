"""Tests for the SoundCloud URL provider."""

from yubal.providers.base import UrlMatch
from yubal.providers.soundcloud import SoundCloudProvider


class TestSoundCloudProvider:
    """Tests for SoundCloudProvider.match / resolve_download_url."""

    def test_matches_single_track_url(self) -> None:
        provider = SoundCloudProvider()
        match = provider.match("https://soundcloud.com/artist-name/track-slug")
        assert match == UrlMatch(
            kind="track",
            content_id="https://soundcloud.com/artist-name/track-slug",
        )

    def test_matches_set_url_as_playlist(self) -> None:
        provider = SoundCloudProvider()
        url = "https://soundcloud.com/artist-name/sets/album-slug"
        match = provider.match(url)
        assert match == UrlMatch(kind="playlist", content_id=url)

    def test_matches_albums_path_as_playlist(self) -> None:
        provider = SoundCloudProvider()
        url = "https://soundcloud.com/artist-name/albums/album-slug"
        match = provider.match(url)
        assert match == UrlMatch(kind="playlist", content_id=url)

    def test_matches_likes_url_as_playlist(self) -> None:
        provider = SoundCloudProvider()
        url = "https://soundcloud.com/some-user/likes"
        match = provider.match(url)
        assert match == UrlMatch(kind="playlist", content_id=url)

    def test_rejects_non_content_pages(self) -> None:
        provider = SoundCloudProvider()
        assert provider.match("https://soundcloud.com/discover") is None
        assert provider.match("https://soundcloud.com/search?q=x") is None

    def test_rejects_non_soundcloud_host(self) -> None:
        provider = SoundCloudProvider()
        assert provider.match("https://music.youtube.com/watch?v=abc123") is None

    def test_rejects_bare_host_with_no_path(self) -> None:
        provider = SoundCloudProvider()
        assert provider.match("https://soundcloud.com/") is None

    def test_resolve_download_url_is_identity(self) -> None:
        provider = SoundCloudProvider()
        url = "https://soundcloud.com/artist-name/track-slug"
        assert provider.resolve_download_url(url) == url
