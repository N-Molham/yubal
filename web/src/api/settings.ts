import { api } from "./client";
import type { components } from "./schema";

export type Settings = components["schemas"]["SettingsResponse"];
export type SettingsUpdate = components["schemas"]["SettingsUpdate"];
export type EnvironmentSettings = components["schemas"]["EnvironmentSettings"];

export async function getSettings(): Promise<Settings | null> {
  const { data, error } = await api.GET("/settings");
  if (error) return null;
  return data;
}

export async function updateSettings(
  update: SettingsUpdate,
): Promise<Settings | null> {
  const { data, error } = await api.PATCH("/settings", { body: update });
  if (error) return null;
  return data;
}
