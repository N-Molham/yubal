import type { components } from "@/api/schema";

export type Platform = components["schemas"]["Source"];

const PLATFORM_LABELS: Record<Platform, string> = {
  youtube_music: "YT Music",
  youtube: "YouTube",
  soundcloud: "SoundCloud",
};

export function platformLabel(
  platform: Platform | null | undefined,
): string | null {
  if (!platform) return null;
  return PLATFORM_LABELS[platform];
}

const MUSIC_YOUTUBE_HOSTS = new Set(["music.youtube.com"]);
const YOUTUBE_HOSTS = new Set([
  "youtube.com",
  "www.youtube.com",
  "m.youtube.com",
  "youtu.be",
  "youtube-nocookie.com",
  "www.youtube-nocookie.com",
]);
const SOUNDCLOUD_HOSTS = new Set([
  "soundcloud.com",
  "www.soundcloud.com",
  "m.soundcloud.com",
]);

/** Coarse, client-only guess of a URL's platform — for UI affordances only
 * (e.g. showing the podcast picker), never for accept/reject decisions.
 * Real classification is server-side (classify_source in yubal.providers);
 * this is a small, deliberate exception to "don't hand-sync validators"
 * (see task 0006) since it never gates anything, only shows/hides a hint.
 */
export function guessPlatformFromUrl(url: string): Platform | null {
  try {
    const host = new URL(url).hostname.toLowerCase();
    if (MUSIC_YOUTUBE_HOSTS.has(host)) return "youtube_music";
    if (YOUTUBE_HOSTS.has(host)) return "youtube";
    if (SOUNDCLOUD_HOSTS.has(host)) return "soundcloud";
    return null;
  } catch {
    return null;
  }
}
