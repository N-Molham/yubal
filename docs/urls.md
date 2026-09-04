## Supported URLs

Three sources are supported. A URL's host decides which pipeline handles it — this doc mirrors the matching logic in `packages/yubal/src/yubal/providers/` (that's the source of truth if this drifts).

### YouTube Music

- Hosts: `music.youtube.com`
- Album/playlist
  - Path: `/playlist?list={id}`
  - Path: `/watch?v={id}&list={id}` (a track opened within a playlist/album context)
  - Example: `https://music.youtube.com/playlist?list=OLAK5uy_m0Ye5titJYUtPwc3RZUwl5iXJ60NUJLEg`
- Track
  - Path: `/watch?v={id}`
  - Example: `https://music.youtube.com/watch?v=Vgpv5PtWsn4`
- Album (browse page)
  - Path: `/browse/{id}` — only recognized on this host
  - Example: `https://music.youtube.com/browse/MPREb_abc123`
- Not supported: homepage, search, anything else on this host not matching the shapes above.

### YouTube (plain, non-Music)

Routed to the same extraction pipeline as YouTube Music — ytmusicapi's `get_watch_playlist`/`get_playlist` work for any YouTube video ID, catalogued in YT Music or not. Split out as its own source purely for display/labeling (the "YouTube" vs "YouTube Music" badge in the UI), not a separate provider. Non-catalogued content (most plain YouTube videos) needs the `download_ugc` option enabled — the web UI's "Include non-music content" checkbox, `--download-ugc` on the CLI, or `download_ugc: true` in a job/subscription request — otherwise it's skipped.

- Hosts: `youtube.com`, `www.youtube.com`, `m.youtube.com`, `youtu.be`, `youtube-nocookie.com`, `www.youtube-nocookie.com`
- Playlist
  - Path: `/playlist?list={id}`
  - Example: `https://youtube.com/playlist?list=PLbE6wFkAlDUfy14yaVjdfGv4wDGmbebH4`
- Track
  - Path: `/watch?v={id}`
  - Short link: `youtu.be/{id}`
  - Other path shapes: `/shorts/{id}`, `/live/{id}`, `/embed/{id}`, `/e/{id}`, `/v/{id}`, `/vi/{id}`
  - Example: `https://youtube.com/watch?v=jNQXAC9IVRw`
- Can be classified as a **podcast episode** instead of music at job/subscription creation time — a user choice, never auto-detected. Changes the output folder to `_Podcasts/{channel}/{year} - {title}`, skips lyrics, and skips album-level ReplayGain. See the README for the UI toggle.
- Not supported: homepage, channel pages (`/channel/{id}`), search, anything not matching the shapes above.

### SoundCloud

No catalog API equivalent to ytmusicapi here — metadata comes straight from yt-dlp's own SoundCloud extractor (title, uploader, duration, thumbnail, and album/artist fields when the track belongs to a set).

- Hosts: `soundcloud.com`, `www.soundcloud.com`, `m.soundcloud.com`
- Track
  - Path: `/{user}/{track-slug}`
  - Example: `https://soundcloud.com/giovannisarani/mezzo-valzer`
- Set/album
  - Path: `/{user}/sets/{slug}`, `/{user}/albums/{slug}`
  - SoundCloud's own `set_type` distinguishes a real album from a generic playlist — reflected in the downloaded folder structure (`Artist/Year - Album/` for albums; flat `_Unofficial/` for tracks with no album)
  - Example: `https://soundcloud.com/leviryan/sets/out-of-spite`
- User likes (works as a sync subscription source, same as any playlist)
  - Path: `/{user}/likes`
  - Example: `https://soundcloud.com/some-user/likes`
- Podcast classification does not apply here — SoundCloud content always goes through the normal music path.
- Not supported: site-feature pages under these hosts (`/discover`, `/search`, `/you`, `/upload`, `/stream`, `/charts`, `/backstage`, `/pro`, `/creators`), or anything not matching the shapes above.

## Test URLs

Reference URLs used while developing/testing extraction and classification edge cases.

### YouTube Music

- OLAK playlist (top songs)
  - `https://music.youtube.com/playlist?list=OLAK5uy_meFrWp55M2SJ6yzAtKBPF1Uq_viHSihmE`
- PL playlist, 1 ATV + 1 OMV + 1 UGC (non-music) track mixed in
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUer3k6jGlQtV-4Sn5g-XhDv`
- PL playlist, 1 ATV
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUfy14yaVjdfGv4wDGmbebH4`
- PL playlist, 1 OMV
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUch0Yr7K_y_9_p5HWPC1uzg`
- PL playlist, 2 ATV tracks from the same album
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUeTMUZp1NAaD-Zw_yEBR_G_`
- PL playlist, full album (SABLE, fABLE)
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUfNsy9oWwd2UBYvAEtX74La`
- OLAK album (SABLE, fABLE)
  - `https://music.youtube.com/playlist?list=OLAK5uy_mxPcDF6PkoNTfDzi7SI69_U5BtA2VYqYM`
- PL playlist, full album (SABLE, fABLE) plus 1 UGC track
  - `https://music.youtube.com/playlist?list=PLxA687tYuMWjZfT1YGgX6xL0PYSMCpBIb`
- OLAK top charts playlist
  - `https://music.youtube.com/playlist?list=OLAK5uy_mzYnlaHgFOvLaxqIPnnouEr-idiUn4NIM`
- Single track, OMV
  - `https://music.youtube.com/watch?v=GkTWxDB21cA`
  - `https://music.youtube.com/watch?v=Lw2J5rZ8kvM`
- Single track, ATV
  - `https://music.youtube.com/watch?v=Vgpv5PtWsn4`
- Single track, OMV with no matching ATV
  - `https://www.youtube.com/watch?v=-HJ0ZGkdlTk`
- Single track, OFFICIAL_SOURCE_MUSIC video type
  - `https://music.youtube.com/watch?v=FPYgJks1Zy0`
  - `https://music.youtube.com/watch?v=k3UevKvP9RU`
- PL playlist with 1 OFFICIAL_SOURCE_MUSIC track
  - `https://music.youtube.com/playlist?list=PLbE6wFkAlDUf_oicZwbgEAEmBfKIy43Rf`

### Plain YouTube (UGC, needs `download_ugc`)

- Single track, UGC — "Me at the zoo", the first video ever uploaded to YouTube, not catalogued in YT Music at all
  - `https://www.youtube.com/watch?v=jNQXAC9IVRw`

### SoundCloud

- Single track, no album
  - `https://soundcloud.com/giovannisarani/mezzo-valzer`
- Set classified as an album (`set_type: album`), 8 tracks
  - `https://soundcloud.com/leviryan/sets/out-of-spite`
