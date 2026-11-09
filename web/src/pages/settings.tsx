import { getSettings, updateSettings, type Settings } from "@/api/settings";
import { showErrorToast, showSuccessToast } from "@/lib/toast";
import {
  Button,
  InputGroup,
  NumberField,
  Spinner,
  Switch,
  TextField,
} from "@heroui/react";
import { useEffect, useState } from "react";
import type { ReactNode } from "react";

function Section({
  title,
  description,
  children,
}: {
  title: string;
  description?: string;
  children: ReactNode;
}) {
  return (
    <section className="flex flex-col gap-4">
      <div>
        <h2 className="text-foreground text-lg font-semibold">{title}</h2>
        {description && <p className="text-muted text-sm">{description}</p>}
      </div>
      {children}
    </section>
  );
}

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

function NumberRow({
  title,
  description,
  value,
  min,
  max,
  onChange,
  unlimitedAtZero = false,
}: {
  title: string;
  description: string;
  value: number;
  min: number;
  max: number;
  onChange: (value: number) => void;
  unlimitedAtZero?: boolean;
}) {
  return (
    <div className="flex flex-col gap-2">
      <div>
        <p className="text-foreground text-sm font-medium">{title}</p>
        <p className="text-muted text-xs">{description}</p>
      </div>
      <NumberField
        value={value}
        onChange={(next) => {
          if (!Number.isNaN(next) && next >= min) onChange(next);
        }}
        minValue={min}
        maxValue={max}
        aria-label={title}
      >
        <InputGroup>
          <InputGroup.Input className="w-full min-w-0 font-mono" />
        </InputGroup>
      </NumberField>
      {unlimitedAtZero && value === 0 && (
        <p className="text-muted text-xs">0 = unlimited</p>
      )}
    </div>
  );
}

function EnvironmentRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="border-separator flex items-start justify-between gap-4 border-b py-2 last:border-0">
      <span className="text-muted text-sm">{label}</span>
      <span className="text-foreground max-w-[60%] truncate text-right font-mono text-xs">
        {value}
      </span>
    </div>
  );
}

export function SettingsPage() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    let mounted = true;
    getSettings().then((data) => {
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

  const updateField = <K extends keyof Settings>(
    key: K,
    value: Settings[K],
  ) => {
    setSettings((current) =>
      current ? { ...current, [key]: value } : current,
    );
  };

  const handleSave = async () => {
    setIsSaving(true);
    const updated = await updateSettings({
      audio_format: settings.audio_format,
      audio_quality: settings.audio_quality,
      fetch_lyrics: settings.fetch_lyrics,
      ytmusic_lyrics_fallback: settings.ytmusic_lyrics_fallback,
      ascii_filenames: settings.ascii_filenames,
      download_ugc: settings.download_ugc,
      replaygain: settings.replaygain,
      scheduler_enabled: settings.scheduler_enabled,
      scheduler_cron: settings.scheduler_cron,
      job_timeout_seconds: settings.job_timeout_seconds,
      auto_sync_liked: settings.auto_sync_liked,
      auto_sync_saved_playlists: settings.auto_sync_saved_playlists,
      max_jobs_per_run: settings.max_jobs_per_run,
      liked_max_items: settings.liked_max_items,
    });
    setIsSaving(false);
    if (!updated) {
      showErrorToast("Save failed", "Could not update settings");
      return;
    }
    setSettings(updated);
    showSuccessToast("Settings saved", "Runtime settings updated");
  };

  const environment = settings.environment;

  return (
    <section className="flex max-w-2xl flex-col gap-10">
      <div>
        <h1 className="text-foreground mb-1 text-2xl font-bold">Settings</h1>
        <p className="text-muted text-sm">
          Environment variables provide defaults; values saved here override
          them.
        </p>
      </div>

      <Section
        title="Downloads and metadata"
        description="Applied to the next job."
      >
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-foreground text-sm font-medium">Audio format</p>
            <p className="text-muted text-xs">opus, mp3, or m4a</p>
          </div>
          <select
            value={settings.audio_format}
            onChange={(event) =>
              updateField(
                "audio_format",
                event.target.value as Settings["audio_format"],
              )
            }
            aria-label="Audio format"
            className="border-separator bg-surface-tertiary text-foreground rounded-lg border px-3 py-2 text-sm"
          >
            <option value="opus">opus</option>
            <option value="mp3">mp3</option>
            <option value="m4a">m4a</option>
          </select>
        </div>

        <NumberRow
          title="Audio quality"
          description="0 = best, 10 = worst"
          value={settings.audio_quality}
          min={0}
          max={10}
          onChange={(value) => updateField("audio_quality", value)}
        />

        <ToggleRow
          title="Fetch lyrics"
          description="Look up synced .lrc lyrics on lrclib.net."
          isSelected={settings.fetch_lyrics}
          onChange={(value) => updateField("fetch_lyrics", value)}
        />
        <ToggleRow
          title="YouTube Music lyrics fallback"
          description="Use YouTube Music lyrics when lrclib has no match."
          isSelected={settings.ytmusic_lyrics_fallback}
          onChange={(value) => updateField("ytmusic_lyrics_fallback", value)}
        />
        <ToggleRow
          title="ASCII filenames"
          description="Transliterate unicode characters in filenames."
          isSelected={settings.ascii_filenames}
          onChange={(value) => updateField("ascii_filenames", value)}
        />
        <ToggleRow
          title="Download UGC"
          description="Save user-generated content under _Unofficial."
          isSelected={settings.download_ugc}
          onChange={(value) => updateField("download_ugc", value)}
        />
        <ToggleRow
          title="ReplayGain"
          description="Apply loudness tags; album gain for complete albums."
          isSelected={settings.replaygain}
          onChange={(value) => updateField("replaygain", value)}
        />
      </Section>

      <Section title="Scheduler" description="Applied immediately.">
        <ToggleRow
          title="Scheduled sync"
          description="Run the scheduler on the cron below."
          isSelected={settings.scheduler_enabled}
          onChange={(value) => updateField("scheduler_enabled", value)}
        />

        <div className="flex flex-col gap-2">
          <div>
            <p className="text-foreground text-sm font-medium">Cron schedule</p>
            <p className="text-muted text-xs">
              Standard five-field cron in the configured timezone.
            </p>
          </div>
          <TextField
            value={settings.scheduler_cron}
            onChange={(value) => updateField("scheduler_cron", value)}
            aria-label="Cron schedule"
          >
            <InputGroup>
              <InputGroup.Input className="w-full min-w-0 font-mono" />
            </InputGroup>
          </TextField>
        </div>

        <NumberRow
          title="Job timeout"
          description="Seconds before a running job is aborted."
          value={settings.job_timeout_seconds}
          min={60}
          max={86400}
          onChange={(value) => updateField("job_timeout_seconds", value)}
        />
      </Section>

      <Section
        title="Library sync"
        description="Requires uploaded YouTube Music cookies."
      >
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
        <NumberRow
          title="Max subscriptions per run"
          description="Oldest-synced first; large libraries rotate over runs."
          value={settings.max_jobs_per_run}
          min={1}
          max={200}
          onChange={(value) => updateField("max_jobs_per_run", value)}
        />
        <NumberRow
          title="Liked Music track limit"
          description="0 means unlimited."
          value={settings.liked_max_items ?? 0}
          min={0}
          max={10000}
          unlimitedAtZero
          onChange={(value) =>
            updateField("liked_max_items", value === 0 ? null : value)
          }
        />
      </Section>

      <Section
        title="Environment"
        description="Set via YUBAL_* environment variables. Changes require a restart."
      >
        <div className="flex flex-col">
          <EnvironmentRow label="YUBAL_ROOT" value={environment.root} />
          <EnvironmentRow label="YUBAL_DATA" value={environment.data} />
          <EnvironmentRow label="YUBAL_CONFIG" value={environment.config} />
          <EnvironmentRow label="YUBAL_TEMP" value={environment.temp} />
          <EnvironmentRow
            label="YUBAL_BASE_PATH"
            value={environment.base_path || "(none)"}
          />
          <EnvironmentRow
            label="YUBAL_HOST"
            value={`${environment.host}:${environment.port}`}
          />
          <EnvironmentRow
            label="YUBAL_LOG_LEVEL"
            value={environment.log_level}
          />
          <EnvironmentRow label="YUBAL_TZ" value={environment.tz} />
          <EnvironmentRow
            label="YUBAL_CORS_ORIGINS"
            value={environment.cors_origins.join(", ")}
          />
          <EnvironmentRow
            label="YUBAL_DEBUG"
            value={String(environment.debug)}
          />
          <EnvironmentRow
            label="YUBAL_RELOAD"
            value={String(environment.reload)}
          />
        </div>
      </Section>

      <div>
        <Button variant="primary" onPress={handleSave} isDisabled={isSaving}>
          {isSaving ? "Saving..." : "Save settings"}
        </Button>
      </div>
    </section>
  );
}
