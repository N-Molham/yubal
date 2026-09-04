# Contributing to yubal

Thanks for your interest in yubal! This document explains how you can help.

## Project Status

yubal is under active solo development and evolving quickly. At this stage, I'm not able to review or merge large feature PRs — they tend to create merge conflicts and review overhead that slow things down.

## How to Contribute

### Reporting Bugs

Before reporting a bug:

1. Check [existing issues](https://github.com/guillevc/yubal/issues) to avoid duplicates
2. Use the latest version to see if the issue has been fixed

When reporting, please include:

- yubal version
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or screenshots

[Open a bug report](https://github.com/guillevc/yubal/issues/new)

### Suggesting Features

Feature ideas are welcome! Please [open an issue](https://github.com/guillevc/yubal/issues/new) to share your idea.

### Questions & Support

For questions or troubleshooting, [open an issue](https://github.com/guillevc/yubal/issues/new).

### Pull Requests

**What's welcome:**

- Bug fixes
- Typos and documentation improvements
- Small, focused changes

**What to avoid for now:**

- Large feature additions
- Major refactors

If you're unsure whether a PR would be welcome, please open an issue first to discuss.

> **Note:** I prefer to handle feature development myself until the project stabilizes. Feel free to fork for personal use, but please don't expect large PRs to be merged.

## Adding a Source

This fork generalized the download pipeline behind a `SourceProvider` protocol (`packages/yubal/src/yubal/providers/`) so a new yt-dlp-supported site doesn't need its own copy of the tagging/cover/M3U/ReplayGain pipeline — only URL matching and metadata extraction differ per source.

To add one:

1. Implement `SourceProvider` (`match(url)` → `UrlMatch | None`, `resolve_download_url(id)` → a URL yt-dlp can download) — see `providers/soundcloud.py` for a source with no catalog API, or `providers/youtube_music.py` for one that wraps an existing client.
2. Register it in `providers/registry.py`.
3. If the source has no catalog API (like SoundCloud), add an extractor mapping yt-dlp's own info-dict fields to `TrackMetadata` — see `services/soundcloud_extractor.py`. If it does (like YouTube Music via ytmusicapi), wire a client implementing the relevant protocol instead.
4. Wire the new extractor/downloader pair into `PlaylistDownloadService`'s dispatch (`services/playlist_download_service.py`) — the same pattern SoundCloud follows: reuse the default YouTube Music pipeline unless the URL matches the new provider.

See `docs/urls.md` for the URL shapes each existing provider matches.
