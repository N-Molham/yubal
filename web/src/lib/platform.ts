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
