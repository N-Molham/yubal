import {
  getLibrarySyncSettings,
  updateLibrarySyncSettings,
  type LibrarySyncSettings,
} from "@/api/settings";
import { showErrorToast, showSuccessToast } from "@/lib/toast";
import {
  Button,
  InputGroup,
  NumberField,
  Spinner,
  Switch,
} from "@heroui/react";
import { useEffect, useState } from "react";

function ToggleRow({
  title,
  description,
  isSelected,
  onChange,
}: {
  title: string;
  description: string;
  isSelected: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <div>
        <p className="text-foreground text-sm font-medium">{title}</p>
        <p className="text-muted text-xs">{description}</p>
      </div>
      <Switch isSelected={isSelected} onChange={onChange} aria-label={title}>
        <Switch.Content>
          <Switch.Control>
            <Switch.Thumb />
          </Switch.Control>
        </Switch.Content>
      </Switch>
    </div>
  );
}

export function SettingsPage() {
  const [settings, setSettings] = useState<LibrarySyncSettings | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    let mounted = true;
    getLibrarySyncSettings().then((data) => {
      if (mounted) setSettings(data);
    });
    return () => {
      mounted = false;
    };
  }, []);

  if (!settings) {
    return (
      <div className="flex justify-center py-16">
        <Spinner />
      </div>
    );
  }

  const updateField = <K extends keyof LibrarySyncSettings>(
    key: K,
    value: LibrarySyncSettings[K],
  ) => {
    setSettings((current) =>
      current ? { ...current, [key]: value } : current,
    );
  };

  const handleSave = async () => {
    setIsSaving(true);
    const updated = await updateLibrarySyncSettings({
      auto_sync_liked: settings.auto_sync_liked,
      auto_sync_saved_playlists: settings.auto_sync_saved_playlists,
      max_jobs_per_run: settings.max_jobs_per_run,
      liked_max_items: settings.liked_max_items,
    });
    setIsSaving(false);
    if (!updated) {
      showErrorToast("Save failed", "Could not update library sync settings");
      return;
    }
    setSettings(updated);
    showSuccessToast("Settings saved", "Library sync preferences updated");
  };

  return (
    <section className="flex max-w-2xl flex-col gap-8">
      <div>
        <h1 className="text-foreground mb-1 text-2xl font-bold">Settings</h1>
        <p className="text-muted text-sm">
          Automatically pull content from your YouTube Music library. Requires
          uploaded cookies.
        </p>
      </div>

      <div className="flex flex-col gap-4">
        <ToggleRow
          title="Sync Liked Music"
          description="Keep your Liked Music playlist in sync automatically."
          isSelected={settings.auto_sync_liked}
          onChange={(value) => updateField("auto_sync_liked", value)}
        />
        <ToggleRow
          title="Sync saved playlists"
          description="Discover playlists saved in your library and keep them in sync."
          isSelected={settings.auto_sync_saved_playlists}
          onChange={(value) => updateField("auto_sync_saved_playlists", value)}
        />
      </div>

      <div className="flex flex-col gap-4">
        <div>
          <p className="text-foreground text-sm font-medium">
            Max subscriptions per run
          </p>
          <p className="text-muted text-xs">
            Oldest-synced subscriptions are picked first so large libraries
            rotate over consecutive runs.
          </p>
        </div>
        <NumberField
          value={settings.max_jobs_per_run}
          onChange={(value) => {
            if (!Number.isNaN(value) && value >= 1) {
              updateField("max_jobs_per_run", value);
            }
          }}
          minValue={1}
          maxValue={200}
          aria-label="Maximum subscriptions per scheduler run"
        >
          <InputGroup>
            <InputGroup.Input className="w-full min-w-0 font-mono" />
          </InputGroup>
        </NumberField>

        <div>
          <p className="text-foreground text-sm font-medium">
            Liked Music track limit
          </p>
          <p className="text-muted text-xs">
            0 means unlimited. Large libraries may need several runs to
            converge.
          </p>
        </div>
        <NumberField
          value={settings.liked_max_items ?? 0}
          onChange={(value) => {
            if (!Number.isNaN(value) && value >= 0) {
              updateField("liked_max_items", value === 0 ? null : value);
            }
          }}
          minValue={0}
          maxValue={10000}
          aria-label="Liked Music track limit"
        >
          <InputGroup>
            <InputGroup.Input className="w-full min-w-0 font-mono" />
          </InputGroup>
        </NumberField>
      </div>

      <div>
        <Button variant="primary" onPress={handleSave} isDisabled={isSaving}>
          {isSaving ? "Saving..." : "Save settings"}
        </Button>
      </div>
    </section>
  );
}
