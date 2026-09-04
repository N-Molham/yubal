// Real validation lives server-side (GET /api/info), backed by the source
// provider registry in packages/yubal/src/yubal/providers — that's the only
// place that actually knows which sources (YouTube Music, YouTube, SoundCloud)
// are supported. This is just a cheap "looks like a URL" gate so obviously
// invalid input doesn't reach the network.
export function isValidUrl(url: string): boolean {
  if (!url) return false;
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}
