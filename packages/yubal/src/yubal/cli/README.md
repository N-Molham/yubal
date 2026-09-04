# yubal CLI

Command-line interface for extracting metadata and downloading tracks from YouTube Music, YouTube, and SoundCloud. The source is detected from the URL — no flag needed.

> **Note:** The CLI covers core workflows (metadata inspection, downloading, tag inspection). For playlist sync and job management, use the web UI.

## Installation

Install the CLI so `yubal` is available on your PATH:

```sh
uv tool install './packages/yubal[cli]'
```

To update after pulling new changes:

```sh
uv tool upgrade yubal
```

To uninstall:

```sh
uv tool uninstall yubal
```

For development, run it via:

```sh
uv run yubal        # from the repo root
just cli             # shorthand
```

## Usage

```
yubal [OPTIONS] COMMAND [ARGS]
```

### Global options

| Option            | Description          |
| ----------------- | -------------------- |
| `-v`, `--verbose` | Enable debug logging |

### Commands

#### `meta` - Extract metadata

Extract structured metadata from a YouTube Music, YouTube, or SoundCloud URL without downloading.

```sh
yubal meta "https://music.youtube.com/playlist?list=OLAK5uy_xxx"
yubal meta "https://music.youtube.com/watch?v=VIDEO_ID" --json
yubal meta "https://soundcloud.com/artist/track"
```

| Option           | Description                                                            |
| ---------------- | ---------------------------------------------------------------------- |
| `--json`         | Output as JSON                                                         |
| `--cookies PATH` | Path to cookies.txt for authentication (YouTube/YouTube Music only)    |
| `--download-ugc` | Extract non-music/UGC videos too (title/uploader/year, no album match) |

#### `download` - Download tracks

Download tracks from a YouTube Music, YouTube, or SoundCloud URL (single track, album/set, or playlist).

```sh
yubal download "https://music.youtube.com/playlist?list=OLAK5uy_xxx" ~/Music
yubal download "https://music.youtube.com/watch?v=VIDEO_ID" ~/Music --codec flac
yubal download "https://soundcloud.com/artist/sets/album-slug" ~/Music
```

| Option            | Description                                                         |
| ----------------- | ------------------------------------------------------------------- |
| `--codec`         | Audio codec: `opus` (default), `flac`, `m4a`, `mp3`                 |
| `--quality`       | Audio quality, 0 (best) to 10 (worst). Lossy codecs only            |
| `--max-items`     | Maximum number of tracks to download                                |
| `--cookies PATH`  | Path to cookies.txt for authentication (YouTube/YouTube Music only) |
| `--download-ugc`  | Download non-music/UGC videos too, to `_Unofficial/`                |
| `--no-m3u`        | Disable M3U playlist file generation                                |
| `--no-cover`      | Disable cover image saving                                          |
| `--no-replaygain` | Disable ReplayGain tagging                                          |

SoundCloud uses yt-dlp's own anonymous client — no cookies needed or supported. See [`docs/urls.md`](../../../../../docs/urls.md) for the exact URL shapes each source matches, and podcast classification (plain YouTube only, not exposed as a CLI flag today — use the web UI or API for that).

ReplayGain applies track gain to downloaded files. Album gain is only calculated
for complete album downloads; playlists and partial album downloads use track
gain only.

#### `tags` - Inspect audio file tags

Display metadata tags from audio files, with ReplayGain/R128 highlighting.

```sh
yubal tags ~/Music/Artist/Album/track.opus
yubal tags ~/Music/Artist/Album/*.opus
yubal tags ~/Music/Artist/Album/ -r
```

| Option                    | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `--json`                  | Output as JSON                                   |
| `-r`, `--replaygain-only` | Show only ReplayGain/R128 fields in table format |

#### `version` - Show version

```sh
yubal version
```
