// Hosts the toolbar icon lights up for — a cheap, no-network heuristic only.
// NOT the real gate for the popup's download/subscribe flow (that defers to
// GET /api/info, backed by the backend's source provider registry — see
// agent/multi-source-downloader/tasks/0006-url-validator-consolidation).
const MEDIA_HOSTS = new Set([
  "youtube.com",
  "www.youtube.com",
  "m.youtube.com",
  "music.youtube.com",
  "youtube-nocookie.com",
  "www.youtube-nocookie.com",
  "soundcloud.com",
  "www.soundcloud.com",
  "m.soundcloud.com",
]);

/** Cheap "is this a real http(s) URL" check — real source validation is
 * server-side (GET /api/info). Used to gate the popup's main flow before
 * it bothers calling the backend at all.
 */
export function isSupportedUrlCandidate(url: string): boolean {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

/** Returns true if the URL points to a page with extractable media —
 * used only to color the toolbar icon, not to gate any real functionality.
 */
export function isYouTubeMediaUrl(url: string): boolean {
  try {
    const u = new URL(url);
    if (!MEDIA_HOSTS.has(u.hostname)) return false;
    if (u.hostname.endsWith("soundcloud.com")) {
      // SoundCloud has no /watch or /playlist path shape — any content
      // page under a user profile is a plausible candidate.
      return u.pathname.length > 1;
    }
    return (
      u.pathname.startsWith("/watch") || u.pathname.startsWith("/playlist")
    );
  } catch {
    return false;
  }
}
