import { UrlInput } from "@/components/common/url-input";
import { LogsPanel } from "@/features/logs/logs-panel";
import { JobsPanel } from "@/features/jobs/jobs-panel";
import { useJobs } from "@/features/jobs/jobs-context";
import { guessPlatformFromUrl } from "@/lib/platform";
import { isValidUrl } from "@/lib/url";
import { Button, Checkbox, InputGroup, NumberField } from "@heroui/react";
import { DownloadIcon, HashIcon } from "lucide-react";
import { memo, useState } from "react";

const DEFAULT_MAX_ITEMS = 100;

interface DownloadFormProps {
  onDownload: (
    url: string,
    maxItems: number,
    downloadUgc: boolean,
    isPodcast: boolean,
  ) => Promise<void>;
}

const DownloadForm = memo(function DownloadForm({
  onDownload,
}: DownloadFormProps) {
  const [url, setUrl] = useState("");
  const [maxItems, setMaxItems] = useState(DEFAULT_MAX_ITEMS);
  const [downloadUgc, setDownloadUgc] = useState(false);
  const [isPodcast, setIsPodcast] = useState(false);

  const canDownload = isValidUrl(url);
  // Coarse client-only guess, just to show/hide this picker — the backend
  // is the real authority (rejects is_podcast for non-YouTube URLs).
  const showPodcastPicker = guessPlatformFromUrl(url) === "youtube";

  const handleDownload = async () => {
    if (canDownload) {
      await onDownload(
        url,
        maxItems,
        downloadUgc,
        showPodcastPicker && isPodcast,
      );
      setUrl("");
    }
  };

  return (
    <section className="mb-8 flex flex-col gap-2">
      <div className="flex gap-2">
        <div className="min-w-0 flex-1">
          <UrlInput value={url} onChange={setUrl} />
        </div>
        <NumberField
          className="w-24"
          aria-label="Max number of tracks to download"
          value={maxItems}
          onChange={(value) => {
            if (!Number.isNaN(value) && value >= 1) setMaxItems(value);
          }}
          minValue={1}
          maxValue={10000}
        >
          <InputGroup>
            <InputGroup.Prefix>
              <HashIcon className="text-muted h-4 w-4" />
            </InputGroup.Prefix>
            <InputGroup.Input
              placeholder="Max"
              className="w-full min-w-0 font-mono"
            />
          </InputGroup>
        </NumberField>
        <Button
          variant="primary"
          className="shrink-0"
          onPress={handleDownload}
          isDisabled={!canDownload}
        >
          <DownloadIcon className="h-4 w-4" />
          Download
        </Button>
      </div>
      <Checkbox isSelected={downloadUgc} onChange={setDownloadUgc}>
        <Checkbox.Content>
          <Checkbox.Control>
            <Checkbox.Indicator />
          </Checkbox.Control>
          Include non-music content (UGC videos, no album match)
        </Checkbox.Content>
      </Checkbox>
      {showPodcastPicker && (
        <Checkbox isSelected={isPodcast} onChange={setIsPodcast}>
          <Checkbox.Content>
            <Checkbox.Control>
              <Checkbox.Indicator />
            </Checkbox.Control>
            Treat as podcast (files go to _Podcasts/, no lyrics or album gain)
          </Checkbox.Content>
        </Checkbox>
      )}
    </section>
  );
});

export function JobsPage() {
  const { jobs, isLoading, startJob, cancelJob, deleteJob } = useJobs();

  const handleDeleteJob = async (jobId: string) => {
    await deleteJob(jobId);
  };

  return (
    <>
      {/* Page Title */}
      <h1 className="text-foreground mb-6 text-2xl font-bold">Downloads</h1>

      {/* URL Input Section */}
      <DownloadForm onDownload={startJob} />

      {/* Downloads Panels */}
      <section className="flex flex-col gap-6">
        <JobsPanel
          jobs={jobs}
          isLoading={isLoading}
          onCancel={cancelJob}
          onDelete={handleDeleteJob}
        />
        <LogsPanel jobs={jobs} />
      </section>
    </>
  );
}
