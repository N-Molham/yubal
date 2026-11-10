# Build frontend
#
# Pinned to $BUILDPLATFORM (the build host's arch), not the target platform:
# bun's JIT crashes under QEMU emulation ("MemoryExhaustion" abort) on a
# foreign-arch multi-platform build. Not a real cross-compile though — the
# output is architecture-independent static JS/CSS/HTML, so building it once
# natively and reusing it for every target platform is correct, not a hack.
FROM --platform=$BUILDPLATFORM oven/bun:1-alpine AS web-builder

ARG VERSION=dev
ARG COMMIT_SHA=dev
ARG IS_RELEASE=false

WORKDIR /app/web
COPY web/package.json web/bun.lock ./
RUN bun install --frozen-lockfile

COPY web/ ./
RUN VITE_VERSION=$VERSION \
    VITE_COMMIT_SHA=$COMMIT_SHA \
    VITE_IS_RELEASE=$IS_RELEASE \
    bun run build

# Bun runtime for yt-dlp's YouTube JS challenge solver. Baked into the final
# image (not fetched at boot): every download may need it, and a silent
# first-boot fetch failure would break format resolution. Musl build; the
# final image installs libstdc++ (bun links it dynamically).
FROM oven/bun:1.4.2-alpine AS bun-bin

# Install Python dependencies
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS python-builder

RUN apk add --no-cache git

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY packages/ ./packages/
RUN uv sync --package yubal-api --no-dev --frozen --no-cache --no-editable

# Final runtime image
FROM python:3.12-alpine

WORKDIR /app

# Install runtime dependencies, then create the non-root user.
#
# ffmpeg and rsgain are NOT baked in here — entrypoint.sh installs them
# under /app/config/ (a persistent volume mount) on first boot instead.
# That trades a slower first start for a much smaller image:
#   - ffmpeg is an 80MB+ static binary, bigger than everything else in
#     this image combined.
#   - rsgain ships only a glibc-dynamically-linked Linux release (its
#     "static" build still links glibc), which cannot run on this image's
#     musl libc, and its Alpine package transitively pulls in a full shared
#     ffmpeg (~90MB). entrypoint.sh installs rsgain via apk into a
#     persistent root under /app/config — musl-native, x86_64 and arm64.
# bun (yt-dlp's JS challenge runtime) IS baked in: every download may need
# it, and a failed first-boot fetch would silently break format resolution.
# libstdc++ is a runtime dependency of bun's musl build.
# curl/tar/xz/unzip stay installed (not removed after) because
# entrypoint.sh needs them at runtime to do these fetches.
RUN set -eux \
    # bash: entrypoint.sh's shebang. su-exec: gosu-equivalent, Alpine-native.
    && apk add --no-cache curl tar xz unzip ca-certificates bash su-exec libstdc++ \
    #
    # --- Non-root user (Alpine's busybox addgroup/adduser, not groupadd/useradd) ---
    && addgroup -g 1000 yubal \
    && adduser -D -H -u 1000 -G yubal -h /app -s /sbin/nologin yubal

# Copy built artifacts
COPY --from=python-builder --chown=yubal:yubal /app/.venv /app/.venv
COPY --from=web-builder --chown=yubal:yubal /app/web/dist ./web/dist
COPY --from=bun-bin /usr/local/bin/bun /usr/local/bin/bun
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/app/.venv/bin:/app/config/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    YUBAL_ROOT=/app \
    YUBAL_HOST=0.0.0.0 \
    YUBAL_PORT=8000

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "yubal_api"]
