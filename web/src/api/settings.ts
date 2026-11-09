import { api } from "./client";
import type { components } from "./schema";

export type LibrarySyncSettings =
  components["schemas"]["LibrarySyncSettingsResponse"];
export type LibrarySyncSettingsUpdate =
  components["schemas"]["LibrarySyncSettingsUpdate"];

export async function getLibrarySyncSettings(): Promise<LibrarySyncSettings | null> {
  const { data, error } = await api.GET("/settings");
  if (error) return null;
  return data;
}

export async function updateLibrarySyncSettings(
  update: LibrarySyncSettingsUpdate,
): Promise<LibrarySyncSettings | null> {
  const { data, error } = await api.PATCH("/settings", { body: update });
  if (error) return null;
  return data;
}
