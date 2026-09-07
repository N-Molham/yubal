#!/bin/bash
set -e

PUID=${PUID:-1000}
PGID=${PGID:-1000}

BIN_DIR=/app/config/bin
APK_ROOT=/app/config/apk

warn_chown() {
    path=$1
    echo "Warning: could not change ownership of '$path' to $PUID:$PGID; continuing because the mount may not support chown." >&2
}

ensure_writable() {
    path=$1

    if ! su-exec "$PUID:$PGID" test -w "$path"; then
        echo "Error: '$path' is not writable by $PUID:$PGID. Set PUID/PGID to an account with write access to this mount." >&2
        exit 1
    fi
}

# ffmpeg/deno are fetched here instead of baked into the image (see
# Dockerfile) — both are 80MB+ static binaries, bigger than everything else
# in the image combined. Cached in /app/config/bin/, a persistent volume
# mount, so this only costs time on the very first boot; every boot after
# that just finds the binary already there and skips straight through.
fetch_ffmpeg_if_missing() {
    if [ -x "$BIN_DIR/ffmpeg" ] && [ -x "$BIN_DIR/ffprobe" ]; then
        return 0
    fi

    local arch
    case "$(uname -m)" in
        x86_64) arch=amd64 ;;
        aarch64 | arm64) arch=arm64 ;;
        *)
            echo "Error: unsupported architecture '$(uname -m)' for ffmpeg fetch." >&2
            return 1
            ;;
    esac

    echo "Fetching ffmpeg (first boot only, cached in $BIN_DIR)..."
    local tmp=/tmp/ffmpeg.tar.xz
    if ! curl -fsSL --retry 3 --retry-delay 5 -o "$tmp" \
        "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${arch}-static.tar.xz"; then
        echo "Error: failed to download ffmpeg. ReplayGain/transcoding will not work" >&2
        echo "until this succeeds on a later boot." >&2
        return 1
    fi
    tar -xJf "$tmp" --strip-components=1 -C "$BIN_DIR" --wildcards '*/ffmpeg' '*/ffprobe'
    rm -f "$tmp"
    chmod +x "$BIN_DIR/ffmpeg" "$BIN_DIR/ffprobe"
    echo "ffmpeg fetched."
}

# Only used by yt-dlp to solve YouTube's JS anti-bot challenges — downloads
# are not otherwise affected if this fetch fails (best-effort, non-fatal).
fetch_deno_if_missing() {
    if [ -x "$BIN_DIR/deno" ]; then
        return 0
    fi

    local arch
    case "$(uname -m)" in
        x86_64) arch=x86_64 ;;
        aarch64 | arm64) arch=aarch64 ;;
        *)
            echo "Warning: unsupported architecture '$(uname -m)' for deno fetch, skipping." >&2
            return 0
            ;;
    esac

    echo "Fetching deno (first boot only, cached in $BIN_DIR)..."
    local tmp=/tmp/deno.zip
    if ! curl -fsSL --retry 3 --retry-delay 5 -o "$tmp" \
        "https://github.com/denoland/deno/releases/latest/download/deno-${arch}-unknown-linux-gnu.zip"; then
        echo "Warning: failed to download deno. YouTube JS-challenge solving will be" >&2
        echo "unavailable until this succeeds on a later boot; regular downloads are unaffected." >&2
        return 0
    fi
    unzip -oq "$tmp" -d "$BIN_DIR"
    rm -f "$tmp"
    chmod +x "$BIN_DIR/deno"
    echo "deno fetched."
}

# Only used for ReplayGain tagging — downloads are not otherwise affected if
# this fails (best-effort, non-fatal). rsgain ships only a glibc-dynamically-
# linked Linux release, which cannot run on this image's musl libc, so Alpine's
# own musl-native rsgain package is installed via apk into a persistent root
# under /app/config (apk installs to /usr otherwise, which does not survive
# container recreation). A thin wrapper in $BIN_DIR sets LD_LIBRARY_PATH so only
# rsgain sees the apk-root libraries. Works on x86_64 and arm64 alike.
install_rsgain_if_missing() {
    if [ -x "$APK_ROOT/usr/bin/rsgain" ]; then
        return 0
    fi

    echo "Installing rsgain (first boot only, cached in $APK_ROOT)..."
    mkdir -p "$APK_ROOT/etc/apk" "$BIN_DIR"
    cp -r /etc/apk/keys "$APK_ROOT/etc/apk/" 2>/dev/null || true
    cp /etc/apk/repositories "$APK_ROOT/etc/apk/repositories" 2>/dev/null || true
    if ! apk --root "$APK_ROOT" --initdb --no-cache add rsgain; then
        echo "Warning: failed to install rsgain. ReplayGain tagging will be unavailable" >&2
        echo "until this succeeds on a later boot; downloads themselves are unaffected." >&2
        return 0
    fi

    cat > "$BIN_DIR/rsgain" <<'EOF'
#!/bin/sh
LD_LIBRARY_PATH="/app/config/apk/usr/lib:/app/config/apk/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" exec /app/config/apk/usr/bin/rsgain "$@"
EOF
    chmod +x "$BIN_DIR/rsgain"
    echo "rsgain installed."
}

case "$PUID" in
    "" | *[!0-9]*)
        echo "PUID must be a numeric user id, got '$PUID'" >&2
        exit 1
        ;;
esac

case "$PGID" in
    "" | *[!0-9]*)
        echo "PGID must be a numeric group id, got '$PGID'" >&2
        exit 1
        ;;
esac

if [ "$(id -u)" = "0" ]; then
    # Create required directories
    mkdir -p /app/config/yubal /app/config/ytdlp "$BIN_DIR" /app/data

    # Non-fatal: a network hiccup on first boot shouldn't crash-loop the
    # container. Downloads needing the missing binary will just fail with a
    # clear error until it fetches successfully on a later boot.
    fetch_ffmpeg_if_missing || true
    fetch_deno_if_missing || true
    install_rsgain_if_missing || true

    # Fix ownership (non-recursive on /app/data to avoid slow startup with large libraries)
    chown "$PUID:$PGID" /app/data || warn_chown /app/data
    chown -R "$PUID:$PGID" /app/config
    ensure_writable /app/data

    exec su-exec "$PUID:$PGID" "$@"
fi

# Non-root: still create dirs if possible, then exec
mkdir -p /app/config/yubal /app/config/ytdlp "$BIN_DIR" /app/data 2>/dev/null || true
fetch_ffmpeg_if_missing || true
fetch_deno_if_missing || true
install_rsgain_if_missing || true
exec "$@"
