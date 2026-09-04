#!/usr/bin/env bash
# Build the yubal Docker image and push it to ghcr.io — a manual,
# local equivalent of what .github/workflows/cd.yaml does in CI.
# Self-contained: bootstraps buildx if needed, logs into ghcr.io if not
# already logged in (via `gh auth token` when possible), and sets the
# ghcr.io package to private after the first push. For a purely local
# build+run with no registry involved, use scripts/build-run.sh instead.
#
# Usage:
#   scripts/build-deploy.sh                     # build + push :latest for this host's arch
#   scripts/build-deploy.sh --tag v0.1.0        # push a specific tag instead of :latest
#   scripts/build-deploy.sh --multi-arch        # build+push linux/amd64,linux/arm64 (buildx, no local image)
#   scripts/build-deploy.sh --public            # set package visibility to public instead of private
#   scripts/build-deploy.sh --dry-run           # print what would run, do nothing
#   scripts/build-deploy.sh --check-only        # run prerequisite checks (buildx, ghcr login) and stop
#   scripts/build-deploy.sh --image ghcr.io/other/repo   # override the target image

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker not found on PATH." >&2
  exit 1
fi

# Derive ghcr.io/<owner>/<repo> from the origin remote, same as
# cd.yaml's IMAGE_NAME: ${{ github.repository }}.
derive_image() {
  local url owner_repo
  url="$(git remote get-url origin 2>/dev/null || true)"
  if [ -z "$url" ]; then
    echo "" && return
  fi
  # git@github.com:owner/repo.git  or  https://github.com/owner/repo.git
  # Docker/OCI image paths must be lowercase even though the GitHub
  # username/repo casing (e.g. "N-Molham") is preserved everywhere else.
  owner_repo="$(echo "$url" | sed -E 's#^git@github\.com:##; s#^https://github\.com/##; s#\.git$##' | tr '[:upper:]' '[:lower:]')"
  echo "ghcr.io/${owner_repo}"
}

TAG="latest"
IMAGE="$(derive_image)"
MULTI_ARCH=false
DRY_RUN=false
CHECK_ONLY=false
ALSO_LATEST=false
VISIBILITY="private"

while [ $# -gt 0 ]; do
  case "$1" in
    --tag)
      TAG="$2"
      shift 2
      ;;
    --image)
      IMAGE="$2"
      shift 2
      ;;
    --multi-arch)
      MULTI_ARCH=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --check-only)
      CHECK_ONLY=true
      shift
      ;;
    --also-latest)
      ALSO_LATEST=true
      shift
      ;;
    --public)
      VISIBILITY="public"
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 [--tag TAG] [--image ghcr.io/owner/repo] [--multi-arch] [--also-latest] [--public] [--dry-run] [--check-only]" >&2
      exit 1
      ;;
  esac
done

if [ -z "$IMAGE" ]; then
  echo "Error: could not derive image name from 'git remote origin', pass --image explicitly." >&2
  exit 1
fi

# ghcr.io/<owner>/<repo> -> owner, repo (package name = repo, by GitHub convention)
OWNER_REPO="${IMAGE#ghcr.io/}"
OWNER="${OWNER_REPO%%/*}"
PACKAGE_NAME="${OWNER_REPO#*/}"

# ---------------------------------------------------------------------------
# Prerequisite checks — these mutate nothing remote, safe to run always.
# ---------------------------------------------------------------------------

ensure_buildx() {
  if ! docker buildx version >/dev/null 2>&1; then
    echo "Error: docker buildx not available. Update Docker or install the buildx plugin." >&2
    exit 1
  fi
  if [ "$MULTI_ARCH" = true ]; then
    echo "==> Ensuring buildx builder supports linux/amd64,linux/arm64"
    if ! docker buildx inspect --bootstrap >/tmp/yubal-buildx-inspect.log 2>&1; then
      echo "==> Creating a dedicated buildx builder (yubal-multiarch)"
      docker buildx create --name yubal-multiarch --driver docker-container --use >/dev/null
      docker buildx inspect --bootstrap >/dev/null
    elif ! grep -q "linux/arm64" /tmp/yubal-buildx-inspect.log || ! grep -q "linux/amd64" /tmp/yubal-buildx-inspect.log; then
      echo "==> Active builder is missing a platform; creating yubal-multiarch"
      docker buildx create --name yubal-multiarch --driver docker-container --use >/dev/null
      docker buildx inspect --bootstrap >/dev/null
    fi
  fi
}

# Returns 0 if we appear to be authenticated to ghcr.io for this image, else 1.
# Probes a tag that almost certainly doesn't exist. This only proves *some*
# valid identity was presented, not that it can push — GHCR can return
# "manifest unknown" for an unrecognized tag even to a token with no
# packages scope at all. Use gh_has_packages_scope() to check push-worthiness
# specifically when the credential came from gh CLI.
ghcr_authenticated() {
  local probe_log="/tmp/yubal-ghcr-probe.log"
  if docker buildx imagetools inspect "${IMAGE}:__yubal_auth_probe__" >"$probe_log" 2>&1; then
    return 0
  fi
  if grep -qiE "unauthorized|authentication required|denied|403|forbidden" "$probe_log"; then
    return 1
  fi
  # Any other failure (e.g. "manifest unknown") means auth itself is fine.
  return 0
}

# Direct, reliable scope check via the X-OAuth-Scopes response header —
# unlike ghcr_authenticated(), this can't be fooled by GHCR's ambiguous
# error semantics for a nonexistent tag.
gh_has_packages_scope() {
  local scopes
  scopes="$(gh api -i /user 2>/dev/null | tr -d '\r' | grep -i '^x-oauth-scopes:' || true)"
  [[ "$scopes" == *"write:packages"* ]]
}

ensure_ghcr_login() {
  echo "==> Checking ghcr.io authentication"

  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if ! gh_has_packages_scope; then
      echo "==> gh CLI token lacks write:packages — refreshing scope now"
      echo "    (a browser window will open — approve the additional scopes there)"
      if ! gh auth refresh -s write:packages,read:packages; then
        echo "Error: 'gh auth refresh' failed or was declined." >&2
        exit 1
      fi
    fi

    if gh_has_packages_scope; then
      echo "==> gh CLI token has write:packages — logging in"
      if gh auth token | docker login ghcr.io -u "$OWNER" --password-stdin >/tmp/yubal-docker-login.log 2>&1; then
        echo "==> Logged in via gh CLI token"
        return 0
      fi
      echo "==> 'docker login' failed despite a properly scoped token:" >&2
      cat /tmp/yubal-docker-login.log >&2
      exit 1
    fi

    # Refresh above didn't grant the scope (e.g. declined in the browser) —
    # fall back to whatever docker credentials already exist, if any.
    if ghcr_authenticated; then
      echo "==> Proceeding with existing docker credentials (gh CLI still lacks write:packages)"
      return 0
    fi

    echo "Error: gh CLI is authenticated as $OWNER but still lacks 'write:packages' after" >&2
    echo "attempting a refresh, and there's no other valid ghcr.io login." >&2
    echo "Run manually: gh auth refresh -s write:packages,read:packages" >&2
    echo "Or:           docker login ghcr.io -u $OWNER   (classic PAT with write:packages)" >&2
    exit 1
  fi

  if ghcr_authenticated; then
    echo "==> Already authenticated to ghcr.io"
    return 0
  fi

  echo
  echo "Error: not authenticated to ghcr.io as $OWNER, and gh CLI isn't available/authenticated." >&2
  echo "Run: docker login ghcr.io -u $OWNER   (with a classic PAT scoped write:packages)" >&2
  echo "Then re-run this script." >&2
  exit 1
}

set_package_visibility() {
  if ! command -v gh >/dev/null 2>&1 || ! gh auth status >/dev/null 2>&1; then
    echo "==> Skipping visibility check (gh CLI not available/authenticated)."
    echo "    Set it manually: https://github.com/${OWNER}/${PACKAGE_NAME}/pkgs/container/${PACKAGE_NAME} -> Package settings"
    return 0
  fi
  echo "==> Setting ghcr.io package visibility to $VISIBILITY (best effort)"
  if gh api --method PATCH "/user/packages/container/${PACKAGE_NAME}" -f "visibility=$VISIBILITY" >/dev/null 2>&1; then
    echo "==> Package visibility set to $VISIBILITY"
  else
    echo "==> Could not set visibility automatically (API call failed, possibly missing"
    echo "    scope or org-owned package). Set it manually:"
    echo "    https://github.com/${OWNER}/${PACKAGE_NAME}/pkgs/container/${PACKAGE_NAME} -> Package settings"
  fi
}

VERSION="$(git describe --tags --always 2>/dev/null || echo dev)"
COMMIT_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
if git describe --tags --exact-match HEAD >/dev/null 2>&1; then
  IS_RELEASE=true
else
  IS_RELEASE=false
fi

FULL_TAG="${IMAGE}:${TAG}"

echo "Image:      $FULL_TAG"
echo "Version:    $VERSION"
echo "Commit:     $COMMIT_SHA"
echo "Is release: $IS_RELEASE"
echo "Multi-arch: $MULTI_ARCH"
echo "Visibility: $VISIBILITY (applied after push)"
echo

if [ "$MULTI_ARCH" = true ]; then
  # shellcheck disable=SC2054  # intentional single value, not array elements
  CMD=(docker buildx build --platform linux/amd64,linux/arm64
    --build-arg "VERSION=$VERSION" --build-arg "COMMIT_SHA=$COMMIT_SHA" --build-arg "IS_RELEASE=$IS_RELEASE"
    -t "$FULL_TAG")
  [ "$ALSO_LATEST" = true ] && CMD+=(-t "${IMAGE}:latest")
  CMD+=(--push .)
else
  CMD=(docker build
    --build-arg "VERSION=$VERSION" --build-arg "COMMIT_SHA=$COMMIT_SHA" --build-arg "IS_RELEASE=$IS_RELEASE"
    -t "$FULL_TAG" .)
fi

echo "==> ${CMD[*]}"
if [ "$MULTI_ARCH" = true ]; then
  PUSH_CMD=()
else
  PUSH_CMD=(docker push "$FULL_TAG")
  [ "$ALSO_LATEST" = true ] && echo "==> also: docker tag $FULL_TAG ${IMAGE}:latest && docker push ${IMAGE}:latest"
  echo "==> ${PUSH_CMD[*]}"
fi

if [ "$DRY_RUN" = true ]; then
  echo
  echo "Dry run — nothing checked, built, or pushed."
  exit 0
fi

ensure_buildx
ensure_ghcr_login

if [ "$CHECK_ONLY" = true ]; then
  echo
  echo "==> Checks passed. Not building or pushing (--check-only)."
  exit 0
fi

"${CMD[@]}"

if [ "$MULTI_ARCH" = false ]; then
  "${PUSH_CMD[@]}"
  if [ "$ALSO_LATEST" = true ]; then
    docker tag "$FULL_TAG" "${IMAGE}:latest"
    docker push "${IMAGE}:latest"
  fi
fi

echo
echo "==> Pushed $FULL_TAG"

set_package_visibility
