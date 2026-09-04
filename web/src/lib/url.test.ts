import { describe, expect, test } from "bun:test";
import { isValidUrl } from "./url";

// isValidUrl is deliberately source-agnostic — it only checks "is this an
// http(s) URL", not "is this a supported source". Real source validation
// happens server-side (GET /api/info), backed by the provider registry.
// This keeps the client from needing a 4th hand-synced copy of the
// YouTube/YouTube-Music/SoundCloud host allowlist every time a source is
// added — see task 0006 in agent/multi-source-downloader/tasks/.
const VALID_URLS = [
  "https://music.youtube.com/playlist?list=OLAK5uy_abc123",
  "http://music.youtube.com/watch?v=dQw4w9WgXcQ",
  "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "https://youtu.be/dQw4w9WgXcQ",
  "https://soundcloud.com/artist-name/track-slug",
  "https://soundcloud.com/artist-name/sets/album-slug",
  "https://soundcloud.com/some-user/likes",
  // Not necessarily a supported source — the backend decides that. This
  // check only gates "is it a URL at all".
  "https://example.com/whatever",
];

const INVALID_URLS = [
  ["empty string", ""],
  ["plain text", "not a url"],
  ["missing protocol", "youtube.com/watch?v=abc"],
  ["ftp protocol", "ftp://example.com/file"],
] as const;

describe("isValidUrl", () => {
  describe("valid http(s) URLs", () => {
    test.each(VALID_URLS)("accepts %s", (url) => {
      expect(isValidUrl(url)).toBe(true);
    });
  });

  describe("invalid input", () => {
    test.each(INVALID_URLS)("rejects %s", (_description, url) => {
      expect(isValidUrl(url)).toBe(false);
    });
  });
});
