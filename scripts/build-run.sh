#!/usr/bin/env bash
# Build the yubal Docker image locally and run it via docker compose.
# Everything stays on this machine — no GitHub Actions, no registry push.
# For publishing to ghcr.io instead, see scripts/build-deploy.sh.
#
# Usage:
#   scripts/build-run.sh              # build + start
#   scripts/build-run.sh --no-cache   # force a clean rebuild
#   scripts/build-run.sh --logs       # build + start + follow logs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker not found on PATH." >&2
  exit 1
fi

BUILD_ARGS=()
FOLLOW_LOGS=false
for arg in "$@"; do
  case "$arg" in
    --no-cache) BUILD_ARGS+=(--no-cache) ;;
    --logs) FOLLOW_LOGS=true ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: $0 [--no-cache] [--logs]" >&2
      exit 1
      ;;
  esac
done

echo "==> Building yubal:local"
docker compose build "${BUILD_ARGS[@]}"

echo "==> Starting container"
docker compose up -d

echo "==> Waiting for health check"
HEALTH_URL="http://localhost:8000/api/health"
for _ in $(seq 1 30); do
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    echo "==> Healthy: $HEALTH_URL"
    break
  fi
  sleep 1
done

if ! curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
  echo "Error: container did not become healthy in time. Recent logs:" >&2
  docker compose logs --tail=50
  exit 1
fi

echo "==> yubal running at http://localhost:8000"

if [ "$FOLLOW_LOGS" = true ]; then
  docker compose logs -f
fi
