## [0.12.0] - 2026-11-10

### 🚀 Features

- _(db)_ Add subscription origin and runtime settings store
- _(yubal)_ Expose library playlist discovery via YTMusic client
- _(api)_ Add runtime library-sync settings
- _(api)_ Track subscription origin and editable max items
- _(api)_ Discover liked music and saved playlists
- _(api)_ Wire library auto-sync into scheduler and API
- _(web)_ Add library sync settings page
- _(api)_ Expose runtime settings for jobs and scheduler
- _(web)_ Expand settings page to all runtime options

### 🐛 Bug Fixes

- _(api)_ Probe auth before discovering library content
- _(yubal)_ Fall back to broader yt-dlp formats when unavailable
- _(yubal)_ Try alternate clients before video+audio fallback
- Use musl bun as yt-dlp JS runtime instead of glibc deno
- Install libstdc++ so bun JS runtime can execute
- Prefer baked bun over stale config-volume copy

### 💼 Other

- Bake bun into the runtime image

### 📚 Documentation

- Document library auto-sync
- Document settings page precedence

### ⚙️ Miscellaneous Tasks

- Drop upstream attribution from release notes
- Bump mise-action to v4.3.0
- Bump version to 0.12.0

## [0.11.1] - 2026-11-09

### 🐛 Bug Fixes

- Bump yt-dlp to resolve YouTube 403 errors by @guillevc
- Bump certifi and urllib3 for known vulnerabilities
- Treat one-track playlists as single-track downloads

### ⚙️ Miscellaneous Tasks

- Run workflows manually only
- Bump version to 0.11.1

## [0.11.0] - 2026-09-07

### 🚀 Features

- Expose per-job UGC/non-music download override
- Add SoundCloud provider for tracks, sets, and likes
- Add source platform field and badge
- Add podcast classification for plain YouTube content

### 🐛 Bug Fixes

- _(deploy)_ Fix multi-arch build failures on ghcr.io push
- _(docker)_ Install musl-native rsgain via apk

### 🚜 Refactor

- Introduce source provider abstraction
- Stop hand-syncing YouTube-only URL allowlists

### 📚 Documentation

- Fix broken star history chart (#174) by @CrustyMozarella

### ⚡ Performance

- Shrink docker image 474MB -> 139MB (71%)

### ⚙️ Miscellaneous Tasks

- Bump version to 0.11.0

## [0.10.0] - 2026-08-18

### 🚀 Features

- _(yubal)_ Use upload year as fallback for unmatched tracks by @guillevc
- Migrate web UI from HeroUI v2 to v3 by @guillevc
- Download unsupported video types to _Unofficial (#162) by @guillevc

### 🐛 Bug Fixes

- Don't skip tracks with missing videoType from API (#165) by @raiden076

### 📚 Documentation

- Improve wording by @guillevc

### ⚙️ Miscellaneous Tasks

- Bump actions/checkout from 6 to 7 in the actions group (#154) by @dependabot[bot]
- Drop redundant python from idiomatic version files by @guillevc
- Bump actions/cache from 5 to 6 in the actions group (#156) by @dependabot[bot]
- Bump yt-dlp from 2026.6.9 to 2026.7.4 in /packages/yubal (#157) by @dependabot[bot]
- Bump jdx/mise-action from 4 to 4.2.3 in the actions group (#167) by @dependabot[bot]
- Add AGENTS.md to gitignore by @guillevc
- Bump jdx/mise-action from 4.2.3 to 4.2.4 in the actions group (#169) by @dependabot[bot]
- Update dependencies by @guillevc
- Bump yt-dlp to latest nightly and ytmusicapi to latest patch by @guillevc
- Bump version to 0.10.0 by @guillevc
- Fix lint by @guillevc

## [0.9.1] - 2026-06-11

### ⚙️ Miscellaneous Tasks

- Fix cliff.toml by @guillevc
- Cliff improvements by @guillevc
- Bump codecov/codecov-action from 6 to 7 in the actions group (#147) by @dependabot[bot]
- Bump yt-dlp from 2026.3.17 to 2026.6.9 in /packages/yubal (#150) by @dependabot[bot]
- Update dependencies by @guillevc
- Bump version to 0.9.1 by @guillevc

## [0.9.0] - 2026-06-06

### 🚀 Features

- _(m3u)_ Emit #PLAYLIST directive for player display name (#143) by @nsainaney
- _(yubal)_ Fall back to YouTube Music lyrics on lrclib miss (#140) by @guillevc
- _(client)_ Support subscribing to Liked Music (list=LM) (#144) (#141) by @nsainaney

### 🎨 Styling

- Fix type checking by @guillevc

### ⚙️ Miscellaneous Tasks

- Update dependencies by @guillevc
- Bump version to 0.9.0 by @guillevc

## [0.8.1] - 2026-05-17

### 🐛 Bug Fixes

- _(docker)_ Run gosu with numeric PUID and PGID (#138) by @guillevc
- _(yubal)_ Cap generated filename components (#136) by @guillevc
- _(yubal)_ Log failed downloads at job end (#133) by @guillevc
- _(docker)_ Tolerate chown failures on data mount (#138) by @guillevc

### 💼 Other

- Allow current uv build backend by @guillevc

### 📚 Documentation

- Clarify ReplayGain album mode (#131) by @guillevc
- Format readme by @guillevc

### 🧪 Testing

- _(yubal)_ Type failed download log assertions by @guillevc

### ⚙️ Miscellaneous Tasks

- Update dependencies by @guillevc
- Update dependencies by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.8.1 by @guillevc

## [0.8.0] - 2026-05-04

### 🚀 Features

- _(docker)_ Add gosu entrypoint for PUID/PGID support and rootless compatibility (#88) by @guillevc
- _(yubal)_ Replace Dockerfile deno curl install with deno PyPI package by @guillevc
- Add reverse proxy subfolder support via YUBAL_BASE_PATH (#119) by @guillevc

### 🐛 Bug Fixes

- Resolve lint and typecheck errors by @guillevc

### 💼 Other

- Python 3.12 -> python 3.14 by @guillevc

### 🚜 Refactor

- _(web)_ Remove dead code by @guillevc

### 📚 Documentation

- Update README.md by @guillevc

### 🧪 Testing

- Add Playwright e2e and unit tests for base path feature by @guillevc

### ⚙️ Miscellaneous Tasks

- Improve release default message by @guillevc
- Bump requests from 2.32.5 to 2.33.0 in the uv group across 1 directory (#123) by @dependabot[bot]
- Bump codecov/codecov-action from 5 to 6 in the actions group (#125) by @dependabot[bot]
- Bump softprops/action-gh-release from 2 to 3 in the actions group (#130) by @dependabot[bot]
- Improve justfile recipe by @guillevc
- Revert CI to just install and remove install-no-cli recipes by @guillevc
- Improve copies by @guillevc
- Add .private folder to gitignore and add info to pyproject.toml by @guillevc
- Update dependencies by @guillevc
- Gitignore coverage files by @guillevc
- Bump version to 0.8.0 by @guillevc

## [0.7.2] - 2026-03-19

### ⚙️ Miscellaneous Tasks

- Bump yt-dlp from 2026.3.13 to 2026.3.17 in /packages/yubal (#114) by @dependabot[bot]
- Add docker to dependabot by @guillevc
- Bump version to 0.7.2 by @guillevc

## [0.7.1] - 2026-03-16

### 🐛 Bug Fixes

- _(api)_ Wire audio_quality setting through to yt-dlp and remove dead code by @guillevc
- _(api)_ Type error by @guillevc

### 💼 Other

- Use bun --bun flag to bypass mise node shim by @guillevc
- Add .bun-version by @guillevc
- _(web)_ Migrate to vite 8 and plugin-react 6 by @guillevc

### 📚 Documentation

- Update README by @guillevc
- Update image paths in README.md by @guillevc
- Fix badge order and update Chrome Extension link by @guillevc
- Modify Chrome extension badge and add README reference by @guillevc
- Nhance installation instructions in README.md by @guillevc

### ⚙️ Miscellaneous Tasks

- _(yubal)_ Switch yt-dlp from git pin to PyPI and add Dependabot (#100) by @guillevc
- Add github-actions ecosystem to Dependabot by @guillevc
- _(yubal)_ Pin yt-dlp to exact version for Dependabot tracking by @guillevc
- Group Dependabot github-actions updates into single PR by @guillevc
- Exclude extension directory from Docker build context by @guillevc
- Bump the actions group with 7 updates (#110) by @dependabot[bot]
- Bump jdx/mise-action from 3 to 4 in the actions group (#111) by @dependabot[bot]
- Bump yt-dlp from 2026.3.3 to 2026.3.13 in /packages/yubal (#112) by @dependabot[bot]
- Update mise version by @guillevc
- Bump version to 0.7.1 by @guillevc

## [0.7.0] - 2026-03-08

### 🚀 Features

- _(yubal)_ Show unmatched count in extraction summary and add OSM support (#95) by @guillevc

### 🐛 Bug Fixes

- _(yubal)_ Use track title as album fallback instead of "Unknown Album" by @guillevc
- _(yubal)_ Remove OLAK5uy_ prefix check and pin ytmusicapi to fix non-album playlist classification by @guillevc
- _(web)_ Enforce object-cover on job card thumbnails for UGC tracks by @guillevc
- _(yubal)_ Extract video ID from watch URLs even when list= parameter is present by @guillevc

### 📚 Documentation

- Revise README with new features and extension info by @guillevc
- Pdate README with unicode filename upgrade notes by @guillevc
- Improve browser extension download buttons by @guillevc

### ⚙️ Miscellaneous Tasks

- Improve justfiles version recipes by @guillevc
- Bump version to 0.7.0 by @guillevc

## [0.6.3] - 2026-03-07

### 🚀 Features

- _(web)_ Change max width by @guillevc
- Add /api/info endpoint and use it in extension by @guillevc

### 🐛 Bug Fixes

- _(api)_ Remove unused audio_format from CreateJobRequest by @guillevc
- _(api)_ Use album metadata for artist and thumbnail in /api/info by @guillevc
- Filter extension commits from changelog and add version range support by @guillevc

### 💼 Other

- _(ci)_ Add zip attestation by @guillevc

### 📚 Documentation

- Refactor by @guillevc
- Document supported URLs by @guillevc

### 🧪 Testing

- _(api)_ Reduce sleep in timeout test to avoid slow teardown by @guillevc

### ⚙️ Miscellaneous Tasks

- Ignore extension changes in ci and cd workflows by @guillevc
- Add release drafts, stable-only latest tag, and exclude extension from changelog by @guillevc
- Cancel in-progress CI runs on new pushes to same branch or PR by @guillevc
- Bump version to 0.7.0-alpha.1 by @guillevc
- _(web)_ Migrate eslint config to use defineConfig by @guillevc
- Update dependencies by @guillevc
- Create recipe for updating yt-dlp by @guillevc
- Bump version to 0.6.3 by @guillevc

## [0.6.2] - 2026-02-24

### 🐛 Bug Fixes

- _(web)_ Use TanStack Router Link for SPA navigation by @guillevc

### ⚙️ Miscellaneous Tasks

- Update dependencies by @guillevc
- Bump version to 0.6.2 by @guillevc

## [0.6.1] - 2026-02-18

### 🐛 Bug Fixes

- Upscale small thumbnail URLs and omit year from folder when unknown (#80) by @guillevc
- Allow null album ID in playlist tracks (#81) by @guillevc
- _(web)_ Add cookie upload option to mobile hamburger menu (#82) by @guillevc
- Accept mobile, short, and embed YouTube URL formats (#84) by @guillevc
- Log how to enable UGC downloads when tracks are skipped by @guillevc

### ⚙️ Miscellaneous Tasks

- Bump version to 0.6.1 by @guillevc

## [0.6.0] - 2026-02-15

### 🚀 Features

- Add SQLite-backed extraction cache for skipping already-processed tracks (#75 #76) by @guillevc
- _(api)_ Make job timeout configurable via YUBAL_JOB_TIMEOUT_SECONDS (#73) by @guillevc

### 🐛 Bug Fixes

- _(web)_ Raise max items limit on jobs page to match backend validation (#79) by @guillevc

### 📚 Documentation

- Revise README for clarity on upgrades and formats by @guillevc
- Update README with Unraid Docker template info (#71) by @guillevc

### ⚙️ Miscellaneous Tasks

- Ignore agent files by @guillevc
- Improve justfile version recipe by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.6.0 by @guillevc

## [0.5.0] - 2026-02-09

### 🚀 Features

- _(yubal)_ Add tags command for inspecting audio file metadata by @guillevc
- _(yubal)_ Add ReplayGain tagging via rsgain (#49) by @guillevc
- _(yubal)_ Route unmatched tracks to _Unmatched/ folder (#32) by @guillevc
- _(yubal)_ Add configurable ascii filename transliteration via unidecode (#58) by @guillevc
- _(yubal)_ Add cancellation token support to metadata extraction by @guillevc
- _(yubal)_ Add mid-download cancellation via yt-dlp progress hooks by @guillevc
- Add UGC track download support (#22) by @guillevc

### 🐛 Bug Fixes

- _(yubal)_ Improve ReplayGain robustness and album detection by @guillevc
- _(yubal)_ Copy cookies to temp file before yt-dlp download by @guillevc
- _(cli)_ Remove unsupported param by @guillevc

### 💼 Other

- _(docker)_ Improve dockerfile by @guillevc

### 🚜 Refactor

- _(yubal)_ Split cli.py into cli/ package with modular commands by @guillevc
- _(yubal)_ Migrate CLI from Click to Typer with version command by @guillevc
- _(yubal)_ Remove unused NO_ALBUM_MATCH skip reason by @guillevc
- Remove dead code by @guillevc
- Remove more dead code by @guillevc
- _(yubal)_ Make services stateless and injectable with protocols by @guillevc
- _(yubal)_ Replace raw tuple with ArtifactPaths named tuple by @guillevc
- Clean up test file organization and remove legacy Python imports by @guillevc
- _(yubal)_ Fix facade bypass, freeze TrackMetadata, extract bitrate I/O, and relocate cover utils by @guillevc
- _(yubal)_ Move domain modules from utils/ to lib/ and inline single-use helpers by @guillevc
- _(yubal-api)_ Extract SubscriptionService, add SubscriptionRepo protocol, and inject singletons via DI by @guillevc
- Rename YTMetaError to YubalError, APIError to UpstreamAPIError, and remove status_code from core exceptions by @guillevc
- _(api)_ Move job timeout from lazy store detection to executor-level asyncio.timeout by @guillevc
- _(yubal)_ Rename Playlists folder to _Playlists for top-sorted directory listing by @guillevc
- _(api)_ Normalize services naming, structure, and protocol usage by @guillevc
- _(api)_ Normalize db and domain naming, remove dead types by @guillevc
- _(yubal)_ Normalize services naming, remove utils/lib boundary leak by @guillevc
- _(api)_ Use str literals in schemas by @guillevc
- _(yubal,web)_ Unify extraction summary logging, add UGC skip reason by @guillevc

### 📚 Documentation

- _(cli)_ Add CLI README with install and usage docs (#45) by @guillevc
- Update test urls by @guillevc
- _(yubal)_ Update extractor docstrings for unmatched track flow by @guillevc
- Update readme by @guillevc

### 🧪 Testing

- Remove unnecessary tests by @guillevc

### ⚙️ Miscellaneous Tasks

- Update justfile by @guillevc
- _(web)_ Increment chunk size limit to silence warning by @guillevc
- _(api)_ Remove unused version definition by @guillevc
- Add git-cliff by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.5.0 by @guillevc

## [0.4.2] - 2026-02-08

### 🚀 Features

- _(api)_ Bumped job queue from 20 to 200 (#61) by @guillevc

### 🐛 Bug Fixes

- _(yubal)_ Normalized null artists to prevent crashing (#60) by @WarlockSyno

### ⚙️ Miscellaneous Tasks

- Bump version to 0.4.2 by @guillevc

## [0.4.1] - 2026-02-08

### 🐛 Bug Fixes

- _(web)_ Replace crypto.randomUUID with counter (#59) by @guillevc

### 📚 Documentation

- Fix readme by @guillevc
- Update project description in README.md by @guillevc
- Update gif by @guillevc
- Increase demo image width in README by @guillevc

### ⚙️ Miscellaneous Tasks

- Bump version to 0.4.1 by @guillevc

## [0.4.0] - 2026-02-05

### 🚀 Features

- _(api, web)_ Add playlist sync feature by @guillevc
- _(web)_ Add responsive navbar with mobile menu support by @guillevc
- _(web)_ Add page titles and refine header typography by @guillevc
- _(web)_ Change copy by @guillevc
- _(api)_ Add scheduler env var settings by @guillevc
- _(api)_ Add Subscription model, remove SyncedPlaylist/SyncConfig by @guillevc
- _(api)_ Add subscription schemas, remove sync schemas by @guillevc
- _(api)_ Add scheduler status schema by @guillevc
- _(api)_ Add subscriptions router, remove sync router by @guillevc
- _(api)_ Add scheduler router, update dependencies and app factory by @guillevc
- _(web)_ Update to subscriptions API, add repository tests by @guillevc
- _(api,web)_ Simplify subscription API and auto-fetch playlist names by @guillevc
- _(api)_ Add Alembic database migrations by @guillevc
- _(web)_ Change button size by @guillevc
- _(api,web)_ Add thumbnail_url to subscriptions by @guillevc
- _(web)_ Change spacing by @guillevc
- _(web)_ Add loading state to subscriptions table by @guillevc
- _(web)_ Cards by @guillevc
- _(web)_ Add SubscriptionCard compound component by @guillevc
- _(web)_ Ui by @guillevc
- _(api,web)_ Add job source tracking to distinguish manual vs scheduler jobs by @guillevc
- _(web)_ Add success toasts for sync actions and improve countdown display by @guillevc
- _(api,web)_ Replace sync interval with cron expression scheduling by @guillevc
- _(web)_ Add loading state to downloads panel and remove empty-state animations by @guillevc
- _(yubal)_ Preserve unicode in filenames and add comprehensive tests by @guillevc
- _(web)_ Add version update indicator to header by @guillevc
- _(api)_ Rename scheduler settings and add scheduled sync documentation by @guillevc
- _(web)_ Show scheduler disabled state in subscriptions page by @guillevc
- _(web)_ Add tooltip to Auto chip showing sync timestamp by @guillevc
- _(web)_ Add JobsProvider context and refresh scheduler on countdown complete by @guillevc
- _(web)_ Add live-updating relative time for Last Synced column by @guillevc
- _(web)_ Change bg by @guillevc
- _(web)_ Change bg by @guillevc
- _(web)_ Console -> logs by @guillevc

### 🐛 Bug Fixes

- _(downloader)_ Prioritize configured codec in yt-dlp format selection (#48) by @ergosteur
- Improve type safety and error handling across packages by @guillevc
- _(api)_ Add format uri to URL fields and sync SkipReasonType with enum by @guillevc
- _(api)_ Preserve app logging config during alembic migrations by @guillevc
- _(api)_ Serialize datetimes with UTC timezone offset by @guillevc
- _(yubal)_ Filter cookies to prevent HTTP 413 errors (#47, #30) by @guillevc
- _(yubal)_ Detect invalid cookies and improve auth error messages (#30) by @guillevc
- _(web)_ Do not use now in time remaining format by @guillevc
- _(web)_ Improve mobile responsiveness for job cards and subscriptions table by @guillevc
- _(api)_ Remove trailing slash from /logs endpoint by @guillevc
- _(web)_ Fix job card overflow and external link visibility by @guillevc
- _(api,web)_ Fix max items input reset and improve SSE performance by @guillevc
- _(api)_ Use SPAStaticFiles for proper client-side routing fallback by @guillevc
- _(api)_ Emit content_info early in SSE stream during extraction by @guillevc
- _(web)_ Reorder job card chips to show codec before track count by @guillevc

### 💼 Other

- Improve layout by @guillevc

### 🚜 Refactor

- _(web)_ Add TanStack Router with header navigation by @guillevc
- _(api)_ Rename database sync.db to yubal.db by @guillevc
- _(api)_ Replace SyncRepository with SubscriptionRepository by @guillevc
- _(api)_ Rename SyncScheduler to Scheduler, use env settings by @guillevc
- Use centralized deps, rename sync.ts to subscriptions.ts by @guillevc
- _(web)_ Rename sync to subscriptions throughout web package by @guillevc
- _(web)_ Reorganize into features/ structure with path aliases by @guillevc
- _(yubal)_ Split domain.py into focused modules and rename services by @guillevc
- _(api)_ Reorganize package structure with clearer naming by @guillevc
- _(web)_ Remove BlurFade animations and fix offline chip flash by @guillevc
- _(web)_ Extract shared hover utilities from card components by @guillevc
- _(api)_ Improve migrations and repository API by @guillevc
- _(web)_ Replace subscription cards with table layout by @guillevc
- _(web)_ Use Icon suffix for lucide-react imports by @guillevc
- _(web)_ Reduce header font and button sizes by @guillevc
- _(web)_ Update nav buttons and subscription table styling by @guillevc
- _(web)_ Increase background gradient opacity by @guillevc
- _(web)_ Rename theme classes from flexoki to dark/light by @guillevc
- _(web)_ Use HeroUI Card components in Panel by @guillevc
- _(web)_ Redesign JobCard with HeroUI Card and add JobChip by @guillevc
- _(web)_ Standardize component props to use types with short names by @guillevc
- _(web)_ Remove faded variant from input components by @guillevc
- _(api, web)_ Replace job polling with SSE for real-time updates by @guillevc
- _(api, web)_ Add timezone to scheduler, combine countdown hooks into useScheduleCountdown by @guillevc
- _(web)_ Rename downloads feature to jobs, update playlists route by @guillevc
- _(api)_ Simplify JobEventBus by removing redundant call_soon_threadsafe by @guillevc
- _(api)_ Rename /logs/history endpoint to /logs by @guillevc
- _(api,web)_ Use generated schema types for SSE events and logs by @guillevc
- _(web)_ Rename console feature to logs by @guillevc

### 📚 Documentation

- Add CONTRIBUTING.md by @guillevc
- Add subscriptions API design by @guillevc
- Add subscriptions implementation plan by @guillevc
- Update .env.example with fetch_lyrics and fix formatting by @guillevc
- Update README by @guillevc
- Update README by @guillevc
- Fix readme by @guillevc
- Update demo by @guillevc
- Set width for demo image in README by @guillevc
- Update upgrade note for version v0.3 by @guillevc
- Clarify cookie export instructions in README by @guillevc

### 🎨 Styling

- _(web)_ Adjust spacing and refine sync button UI by @guillevc
- _(web)_ Refine JobCard styling and layout adjustments by @guillevc

### 🧪 Testing

- Mock network calls and add pytest-socket to isolate unit tests by @guillevc
- Modernize test suites with parameterization and shared fixtures by @guillevc

### ⚙️ Miscellaneous Tasks

- Update CLAUDE.md by @guillevc
- Simplify gitignore by @guillevc
- _(yubal)_ Upgrade ytdlp version by @guillevc
- Remove old doc files by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.4.0 by @guillevc

## [0.3.1] - 2026-01-29

### 🚀 Features

- _(yubal)_ Improve ytdlp built in retry sleep functions by @guillevc

### 🐛 Bug Fixes

- _(yubal)_ Address CodeQL alert by @guillevc
- _(yubal)_ Handle missing artists/thumbnails in playlist tracks by @guillevc
- _(docker)_ Add git for yt-dlp installation from GitHub by @guillevc

### 📚 Documentation

- Update README by @guillevc

### ⚙️ Miscellaneous Tasks

- _(yubal)_ Pin yt-dlp to master branch commit by @guillevc
- _(yubal)_ Update yt-dlp to latest master commit (#29) by @guillevc
- Bump version to 0.3.1 by @guillevc

## [0.3.0] - 2026-01-26

### 🚀 Features

- _(docker)_ Run container as non-root user by default (#21) by @guillevc
- _(yubal)_ Add single track download support for YouTube Music URLs by @guillevc
- Improve single track display and skip M3U for tracks by @guillevc
- _(yubal)_ Add fuzzy artist matching in album search validation by @guillevc
- _(yubal)_ Add retry logic for transient download errors and matching tests by @guillevc
- _(api)_ Add graceful shutdown with job cancellation and cleanup by @guillevc
- _(api)_ Add validation for log_level and timezone settings by @guillevc
- _(yubal)_ Add playlist ID suffix to m3u and cover filenames to prevent collisions by @guillevc
- _(web)_ Add external link button to job card by @guillevc
- _(yubal)_ Add automatic lyrics fetching from lrclib.net by @guillevc

### 🐛 Bug Fixes

- _(web)_ Align URL validation with backend and show error feedback by @guillevc
- _(yubal)_ Validate album search results match track title and artist by @guillevc
- _(yubal)_ Normalize titles when matching album search results by @guillevc
- _(api)_ Remove logging calls from signal handler by @guillevc
- _(api)_ Remove custom signal handler, let uvicorn handle shutdown by @guillevc
- _(api)_ Emit content_info on phase transition for playlists with skipped tracks by @guillevc
- _(yubal)_ Pass cookies to yt-dlp for age-restricted content by @guillevc
- _(api)_ Remove auto-clear of active job slot on completion by @guillevc
- _(web)_ Show job card link while running by @guillevc
- _(yubal)_ Include extraction skips in playlist total and add SkipReason.label by @guillevc
- _(web)_ Add offset to scrollshadow by @guillevc
- Skip playlist artifacts for single tracks and support youtube.com URLs by @guillevc
- _(web)_ Change input validation error message by @guillevc
- _(web)_ Trim url whitespace by @guillevc

### 🚜 Refactor

- _(api)_ Use yubal's is_supported_url for URL validation by @guillevc
- Rename AlbumInfo to ContentInfo across API and web by @guillevc
- Simplify conditionals and reduce complexity in sync_service by @guillevc
- _(api,yubal)_ Improve error handling, thread safety, and validation by @guillevc
- _(yubal)_ Extract fuzzy matching logic to dedicated module by @guillevc
- _(api)_ Use APIRouter instead of mounted sub-app for DI compatibility by @guillevc
- _(yubal,api)_ Move cleanup_part_files to yubal package by @guillevc
- _(api)_ Improve JobStore with thread safety and comprehensive tests by @guillevc
- _(api)_ Modernize SyncService with cleaner architecture and generic naming by @guillevc
- Remove dead code by @guillevc

### 📚 Documentation

- _(api)_ Update comments for album → content terminology by @guillevc
- Update README by @guillevc
- Rewrite README by @guillevc
- Improve README copy and structure by @guillevc
- Add lrc to readme by @guillevc
- Update README by @guillevc

### ⚙️ Miscellaneous Tasks

- Add user UID:GID to compose files and format-root recipes (#21) by @guillevc
- Add CLAUDE.md by @guillevc
- Update CLAUDE.md by @guillevc
- Add dead code detection and remove unused code by @guillevc
- Remove old doc files by @guillevc
- Update dependencies by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.3.0 by @guillevc

## [0.2.3] - 2026-01-22

### 🚀 Features

- Add stats_type discriminator and aggregate_skip_reasons utility by @guillevc
- _(yubal)_ Show unavailable tracks with reasons and improve logging by @guillevc
- _(yubal)_ Add multi-value artist tags for Jellyfin/Navidrome/Gonic support by @guillevc

### 🚜 Refactor

- Simplify job-card with unified status config and CircleAlert icon by @guillevc

### 📚 Documentation

- Add tagging research by @guillevc
- Add integrations file by @guillevc
- Reorganize media servers section in README by @guillevc
- Clarify M3U playlist relative path support status by @guillevc
- Remove community section from README by @guillevc

### ⚙️ Miscellaneous Tasks

- Bump version to 0.2.3 by @guillevc

## [0.2.2] - 2026-01-20

### 📚 Documentation

- Add GitHub funding link by @guillevc
- Dd GitHub sponsor button to README by @guillevc

### ⚙️ Miscellaneous Tasks

- Bump version to 0.2.2 by @guillevc

## [0.2.1] - 2026-01-20

### 🚀 Features

- _(web)_ Add activity spinner and offline chip to console panel by @guillevc

### 🐛 Bug Fixes

- Add missing error logs for silent failures by @guillevc
- Use semicolon without space for artist separator (Jellyfin compatibility) (#12) by @guillevc

### 📚 Documentation

- Revise playlist recommendation and setup instructions by @guillevc
- Update README with playlist support announcement by @guillevc

### ⚙️ Miscellaneous Tasks

- _(gh)_ Use github-hosted runners by @guillevc
- Bump version to 0.2.1 by @guillevc

## [0.2.0] - 2026-01-18

### 🚀 Features

- _(web)_ Increment by @guillevc
- _(web)_ Download playlist button by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- Playlist increment by @guillevc
- _(yubal)_ Improve DI by @guillevc
- Create app by @guillevc
- Report non-music videos by @guillevc
- New backend by @guillevc
- _(api)_ Add yubal-api package with FastAPI backend by @guillevc
- _(web)_ Improve header by @guillevc
- _(web)_ Footer by @guillevc
- _(web)_ Background by @guillevc
- _(web)_ Improve footer by @guillevc
- Add ytmusicapi cookie auth and better error handling by @guillevc
- _(yubal)_ Add PlaylistDownloadService for unified playlist workflow by @guillevc
- _(yubal, api)_ Add cancellation support and refactor API as thin client by @guillevc
- Give playlist cover by @guillevc
- Add max_items limit for playlist downloads by @guillevc
- Add content kind to distinguish albums from playlists by @guillevc
- _(cli)_ Improve UI by @guillevc
- _(api)_ Add rich logging with formatted output by @guillevc
- _(yubal)_ Improve logging by @guillevc
- _(api, web)_ Stream logs via SSE with Rich HTML styling by @guillevc
- _(web)_ Use Image component by @guillevc
- _(web)_ Add version check by @guillevc
- _(web)_ Add pulsing dot indicator for version updates by @guillevc
- _(web)_ Ui improvement by @guillevc
- _(api,web)_ Replace ANSI logs with structured JSON logging by @guillevc
- Add prod/build tasks and fix static files path by @guillevc
- _(ci)_ Add test coverage with codecov integration by @guillevc
- _(yubal,api)_ Show channel name for playlists in downloads panel by @guillevc
- _(web)_ Replace ASCII icons with Lucide icons in console logs by @guillevc
- _(web)_ Add empty state component with improved UI for panels by @guillevc
- _(yubal)_ Add missing CLI options and clarify album support by @guillevc
- _(yubal)_ Improve album detection with flexible track matching by @guillevc
- Add warning colors to web console and docker compose recipe by @guillevc
- _(web)_ Add faded variant to max tracks input by @guillevc

### 🐛 Bug Fixes

- Explicitly disable cookies during fetch info by @guillevc
- Lint errors and format issues by @guillevc
- Improve UI styling for cards and panels by @guillevc
- _(web)_ Escaping issues by @guillevc
- Show download cancelled message in danger color by @guillevc
- _(docker)_ Use non-editable install and YUBAL_ROOT for static files by @guillevc
- _(docker)_ Add retry logic and file-based ffmpeg download by @guillevc
- _(api)_ Add Windows compatibility for MIME types and timezone data (#6) by @guillevc
- _(api)_ Exclude year from playlist responses by @guillevc

### 💼 Other

- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc

### 🚜 Refactor

- Move component by @guillevc
- Move components by @guillevc
- Restructure web by @guillevc
- _(web)_ Change file naming by @guillevc
- _(yubal)_ Modernize Python codebase with architecture improvements by @guillevc
- Remove yubal by @guillevc
- _(api)_ Use yubal library backend and migrate to src layout by @guillevc
- _(api)_ Make settings root-relative with YUBAL_ROOT env var by @guillevc
- _(api)_ Replace loguru/mutagen with stdlib logging and mediafile by @guillevc
- Simplify config paths to library and config directories by @guillevc
- Use AudioCodec from yubal as single source of truth by @guillevc
- _(api, web)_ Move log styling from backend to frontend by @guillevc
- _(web)_ Remove status indicator from console panel by @guillevc
- Improve code quality and error handling by @guillevc
- _(docker)_ Simplify Dockerfile and update config structure by @guillevc
- Improve code quality with extracted components and better error handling by @guillevc
- _(web)_ Simplify error boundary with semantic colors by @guillevc
- Rename data directory from library to data and update env var by @guillevc
- _(web)_ Rename Github icon component to GithubIcon by @guillevc

### 📚 Documentation

- Playlists poc by @guillevc
- Improve poc by @guillevc
- Improve poc by @guillevc
- Add plan by @guillevc
- Add plan by @guillevc
- Improve plan by @guillevc
- Update README to reflect current architecture and add codebase analysis by @guillevc
- Streamline README with library structure examples and cleaner formatting by @guillevc
- Clarify flat folder structure roadmap item by @guillevc
- Add Star History section to README by @guillevc
- Update README with upgrade instructions for v0.2.0 by @guillevc
- Update README with playlist server recommendation by @guillevc
- Update acknowledgments in README.md by @guillevc
- _(yubal)_ Add pdoc documentation generation and clean up public API by @guillevc
- Update branding from Album to Music Downloader by @guillevc
- Update demo image in README.md by @guillevc
- Update demo by @guillevc

### 🎨 Styling

- Linting by @guillevc
- _(yubal)_ Add linting rule by @guillevc
- _(web)_ Refine button and input border radius by @guillevc
- _(web)_ Add subtle gradient background with teal and purple accents by @guillevc
- _(web)_ Simplify background gradients and fix code formatting by @guillevc

### ⚙️ Miscellaneous Tasks

- Remove files by @guillevc
- Fix files by @guillevc
- Fix file by @guillevc
- Improve linting by @guillevc
- Remove files by @guillevc
- _(gh)_ Improve workflows by @guillevc
- Fix justfile by @guillevc
- Move dev files by @guillevc
- Remove files by @guillevc
- Fix lint/format by @guillevc
- Remove files by @guillevc
- Create justfile by @guillevc
- Update dependencies by @guillevc
- Add py.typed marker files for PEP 561 by @guillevc
- Add ANN rules to ruff and fix type annotations by @guillevc
- Improvements by @guillevc
- Improvements by @guillevc
- Improvements by @guillevc
- Improvements by @guillevc
- Update justfile by @guillevc
- Update justfile by @guillevc
- Add ignored files by @guillevc
- Merge version bump and add justfile sync/upgrade/version recipes by @guillevc
- Use dynamic versioning and add vite chunk splitting by @guillevc
- _(api)_ Remove unused code and dead imports by @guillevc
- Add codecov token by @guillevc
- _(web)_ Fix formatting by @guillevc
- _(web)_ Fix class ordering in error boundary by @guillevc
- Bump version to 0.2.0-beta.1 by @guillevc
- _(cd)_ Store attestations in GitHub storage instead of GHCR by @guillevc
- _(cd)_ Use GitHub Actions cache instead of registry cache by @guillevc
- Prevent codecov failures from blocking pipeline by @guillevc
- _(docker)_ Rename dev tag to master for clarity by @guillevc
- Update dependencies and docker config by @guillevc
- Bump version to 0.2.0 by @guillevc

## [0.1.4] - 2026-01-09

### 📚 Documentation

- Pdate README with new release link format by @guillevc

### ⚙️ Miscellaneous Tasks

- Update beets file meta version by @guillevc
- Bump version to 0.1.4 by @guillevc

## [0.1.3] - 2026-01-08

### 🐛 Bug Fixes

- _(tagger)_ Pass library directory via CLI instead of config (#5) by @guillevc

### 📚 Documentation

- Evise Spotify plugin status in README by @guillevc
- Revise README for Spotify plugin update by @guillevc

### ⚙️ Miscellaneous Tasks

- Update deps by @guillevc
- Bump version to 0.1.3 by @guillevc

## [0.1.2] - 2026-01-07

### 🚀 Features

- _(web)_ Add animations by @guillevc
- _(web)_ Add theme toggle animation by @guillevc
- Improve UI by @guillevc
- UI improvements by @guillevc
- UI improvements by @guillevc
- _(web)_ Improve downloads UI by @guillevc
- _(web)_ Improve job card by @guillevc
- _(web)_ Add star on github button by @guillevc
- _(web)_ UI improvements by @guillevc
- _(web)_ Improve UI by @guillevc
- Replace spotify with deezer by @guillevc
- _(docker)_ Beets config auto-update by @guillevc
- _(docker)_ Beets config auto-update by @guillevc

### 🐛 Bug Fixes

- _(web)_ Local storage crash by @guillevc

### 📚 Documentation

- Update README with caution on cookie usage by @guillevc
- Refine feature descriptions in README.md by @guillevc
- Update section header for Cookies in README by @guillevc
- Readme formatting by @guillevc
- Update README with Spotify plugin notice by @guillevc
- Pdate README with clarification on Spotify support by @guillevc
- Update README with Spotify removal instructions by @guillevc

### 🎨 Styling

- _(web)_ Format by @guillevc

### 🧪 Testing

- _(web)_ Add some tests by @guillevc

### ⚙️ Miscellaneous Tasks

- _(web)_ Remove unused dev dependencies by @guillevc
- Move files by @guillevc
- Bump version to 0.1.2 by @guillevc

## [0.1.1] - 2026-01-04

### 🚀 Features

- _(client)_ Improve footer by @guillevc
- Improve version display in webapp by @guillevc

### 🐛 Bug Fixes

- Version not working in docker image by @guillevc
- Version not working in docker image by @guillevc
- Pin numpy<2 for compatibility (#1) by @guillevc
- Explicitly disable cookies during fetch info (#3) by @guillevc

### 📚 Documentation

- Add browser extension to roadmap by @guillevc

### ⚙️ Miscellaneous Tasks

- Add context7 by @guillevc
- Remove project mcp definitions by @guillevc
- Potential fix for code scanning alert no. 1: Workflow does not contain permissions by @guillevc
- Update dependencies by @guillevc
- Bump version to 0.1.1 by @guillevc

## [0.1.0] - 2025-12-31

### 🚀 Features

- Initial commit by @guillevc
- Make it a CLI by @guillevc
- Improvements by @guillevc
- Add track by @guillevc
- Add release date by @guillevc
- Remove genre tag from yt-dlp output by @guillevc
- Remove genre tag from yt-dlp output by @guillevc
- Increment by @guillevc
- Improve tagging by @guillevc
- Improve tags by @guillevc
- Improve tags by @guillevc
- Increment by @guillevc
- Nuke command by @guillevc
- Add import by @guillevc
- Add fastapi by @guillevc
- Improve fastapi by @guillevc
- React app by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ UI improvements by @guillevc
- _(web)_ Add theme by @guillevc
- Change cancel button by @guillevc
- UI improvements by @guillevc
- _(web)_ Imprmove UI by @guillevc
- _(web)_ Improve UI by @guillevc
- Jobs by @guillevc
- Jobs by @guillevc
- Improve progress tracking by @guillevc
- _(client)_ Improve download panel by @guillevc
- _(web)_ Improve styles by @guillevc
- _(web)_ Improve UI by @guillevc
- _(web)_ Improve UI by @guillevc
- Add album thumbnail by @guillevc
- _(web)_ UI improvements by @guillevc
- Env vars by @guillevc
- _(client)_ Add light mode css by @guillevc
- _(client)_ Add dark/light theme switch by @guillevc
- _(web)_ Change icon by @guillevc
- Improvements by @guillevc
- Improve audio format and quality support by @guillevc
- Support cookies.txt by @guillevc
- _(web)_ Make downlaods and console a vertical stack by @guillevc
- _(web)_ Collapsible console by @guillevc
- _(web)_ Terminal status indicator by @guillevc
- _(web)_ Add cookie upload by @guillevc
- _(web)_ Allow removing cookie file by @guillevc
- _(beets)_ Allow overriding already imported albums by @guillevc
- _(client)_ Improve UI by @guillevc
- _(client)_ Add tooltip to cookie button by @guillevc
- _(client)_ Update icon by @guillevc
- _(client)_ Improve UI by @guillevc
- _(client)_ Dynamic version string in header by @guillevc
- _(client)_ Add version link by @guillevc
- _(client)_ Show commit hash by @guillevc
- _(client)_ Change icon by @guillevc

### 🐛 Bug Fixes

- Use year in folder names by @guillevc
- Relative paths by @guillevc
- Change path by @guillevc
- Missing yt fields by @guillevc
- Use evaluate template instead by @guillevc
- _(web)_ Remove console progress bar by @guillevc
- Multiple corrections by @guillevc
- Jobs queue by @guillevc
- Jobs queue by @guillevc
- Jobs queue by @guillevc
- _(server)_ Type errors by @guillevc
- _(server)_ Bitrate by @guillevc
- Spotify keys are not required by @guillevc

### 💼 Other

- Improve spotify metadata matching by @guillevc
- Update dependencies by @guillevc
- Include justfile and linting for webapp by @guillevc
- Add ty by @guillevc
- Improve justfile by @guillevc
- _(ci)_ Add woodpecker by @guillevc
- _(docker)_ Add Dockerfile by @guillevc
- _(web)_ Terminal status indicator by @guillevc
- Add --frozen-lockfile by @guillevc
- _(docker)_ Improve Dockerfile by @guillevc
- _(docker)_ Improve docker by @guillevc
- _(docker)_ Improve dockerfile by @guillevc
- Improve docker support by @guillevc
- _(docker)_ Fix Dockerfile by @guillevc
- _(docker)_ Simplify Dockerfile by @guillevc
- _(docker)_ Improve dockerfile and examples by @guillevc
- _(web)_ Fix deps by @guillevc

### 🚜 Refactor

- Folder structure by @guillevc
- Move files around by @guillevc
- Full refactor by @guillevc
- Change name by @guillevc
- Utils file by @guillevc
- Move files by @guillevc
- Rename to yubal by @guillevc
- _(web)_ Move file by @guillevc
- Unify job statu stype by @guillevc
- _(server)_ Code structure by @guillevc
- _(server)_ Unify models by @guillevc
- _(server)_ Simplify progress models by @guillevc
- Remove unused API response data by @guillevc
- Use deps by @guillevc
- Remove dead code by @guillevc
- Proper DI by @guillevc
- Code improvements by @guillevc
- Move docker deploy files by @guillevc

### 📚 Documentation

- Add CLAUDE.md by @guillevc
- Improve claude by @guillevc
- _(docker)_ Add tz to .env examples by @guillevc
- Add MIT License to the project by @guillevc
- Improve README by @guillevc
- Readme changes by @guillevc
- Update README with YouTube cookies and audio settings by @guillevc
- Enhance README content and formatting by @guillevc
- Revise README for clarity and formatting improvements by @guillevc
- Revise README for clarity and formatting consistency by @guillevc
- Update readme and demo by @guillevc
- Add GIF speed note to README by @guillevc
- Add roadmap by @guillevc
- Readme changes by @guillevc
- Fix readme by @guillevc
- Improve readme by @guillevc
- Simplify README by @guillevc
- Improve README by @guillevc
- Readme formatting by @guillevc

### ⚡ Performance

- Reduce information retrieval from get_info step by @guillevc

### 🎨 Styling

- _(web)_ Fix formatting by @guillevc
- Improve lint, formatting, add python dead code analyzer by @guillevc

### 🧪 Testing

- _(server)_ Add unit tests by @guillevc
- _(server)_ Job store tests by @guillevc

### ⚙️ Miscellaneous Tasks

- Improve gitignore by @guillevc
- Change gitignore by @guillevc
- Add ruff by @guillevc
- Enable ruff rules by @guillevc
- Remove CLI by @guillevc
- Update deps by @guillevc
- Remove dead code by @guillevc
- Add vscode by @guillevc
- Remove tsbuildinfo by @guillevc
- Improve vscode settings by @guillevc
- Improve editorconfig by @guillevc
- _(docker)_ Fix example file by @guillevc
- Improve local docker env example file by @guillevc
- Remove example file by @guillevc
- Add gh workflow by @guillevc
- Add cd workflow by @guillevc
- Remove woodpecker by @guillevc
- Add version bump recipe by @guillevc
- Add ko-fi by @guillevc
- Agents.md by @guillevc
