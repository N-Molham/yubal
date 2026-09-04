import type { Job, JobStatus } from "@/api/jobs";
import { formatDateTime } from "@/lib/format";
import { isActive, isFinished, isRunning } from "@/lib/job-status";
import { platformLabel } from "@/lib/platform";
import {
  Button,
  buttonVariants,
  Card,
  Chip,
  cn,
  ProgressBar,
  Tooltip,
} from "@heroui/react";
import {
  CheckCircleIcon,
  CircleAlertIcon,
  ClockIcon,
  ExternalLinkIcon,
  Loader2,
  Loader2Icon,
  Trash2Icon,
  XCircleIcon,
  XIcon,
  ZapIcon,
} from "lucide-react";
import { JobChip } from "./job-chip";

type Props = {
  job: Job;
  onCancel?: (jobId: string) => void;
  onDelete?: (jobId: string) => void;
};

type ProgressColor = "default" | "accent" | "success" | "warning" | "danger";

const STATUS_CONFIG: Record<
  JobStatus,
  {
    icon: typeof ClockIcon;
    color: string;
    progressColor: ProgressColor;
    spin?: boolean;
  }
> = {
  pending: {
    icon: ClockIcon,
    color: "text-muted",
    progressColor: "default",
  },
  fetching_info: {
    icon: Loader2Icon,
    color: "text-muted",
    progressColor: "default",
    spin: true,
  },
  downloading: {
    icon: Loader2Icon,
    color: "text-accent",
    progressColor: "accent",
    spin: true,
  },
  importing: {
    icon: Loader2,
    color: "text-secondary",
    progressColor: "default",
    spin: true,
  },
  completed: {
    icon: CheckCircleIcon,
    color: "text-success",
    progressColor: "success",
  },
  failed: { icon: XCircleIcon, color: "text-danger", progressColor: "danger" },
  cancelled: { icon: XIcon, color: "text-warning", progressColor: "warning" },
};

function StatusIcon({
  status,
  hasPartialFailures,
}: {
  status: JobStatus;
  hasPartialFailures?: boolean;
}) {
  const sizeClass = "h-4 w-4";

  if (status === "completed" && hasPartialFailures) {
    return <CircleAlertIcon className={`${sizeClass} text-warning`} />;
  }

  const { icon: Icon, color, spin } = STATUS_CONFIG[status];
  return (
    <Icon className={`${sizeClass} ${color} ${spin ? "animate-spin" : ""}`} />
  );
}

function Thumbnail({
  url,
  status,
  hasPartialFailures,
}: {
  url: string | null;
  status: JobStatus;
  hasPartialFailures?: boolean;
}) {
  const statusIcon = (
    <StatusIcon status={status} hasPartialFailures={hasPartialFailures} />
  );

  return (
    <div className="relative h-18 w-18 shrink-0">
      {url ? (
        <img
          src={url}
          alt=""
          className="h-full w-full rounded-sm object-cover"
        />
      ) : (
        <div className="bg-surface-tertiary flex h-full w-full shrink-0 items-center justify-center rounded-sm"></div>
      )}
      <div className="bg-surface-secondary/80 absolute right-0.5 bottom-0.5 z-10 grid h-6 w-6 place-items-center rounded-full">
        {statusIcon}
      </div>
    </div>
  );
}

function ContentInfo({
  title,
  artist,
  year,
  trackCount,
  audioCodec,
  audioBitrate,
  showBitrate,
  kind,
  platform,
  source,
  createdAt,
}: {
  title: string;
  artist: string | null;
  year: number | null;
  trackCount: number | null;
  audioCodec: string | null;
  audioBitrate: number | null;
  showBitrate: boolean;
  kind: "playlist" | "album" | "track" | null;
  platform: "youtube_music" | "youtube" | "soundcloud" | null;
  source: "manual" | "scheduler";
  createdAt: string | undefined;
}) {
  const platformText = platformLabel(platform);
  return (
    <div className="min-w-0">
      <div className="flex flex-col gap-1">
        <div className="flex min-w-0 items-baseline gap-2 font-mono text-sm">
          <span className="text-foreground truncate">{title}</span>
          {year && <span className="text-muted shrink-0">({year})</span>}
        </div>
        <p className="text-muted mb-1 min-w-0 truncate text-sm">{artist}</p>
      </div>
      <div className="flex items-center gap-2">
        {source === "scheduler" && (
          <Tooltip delay={0} closeDelay={0}>
            <Tooltip.Trigger>
              <Chip
                size="md"
                variant="soft"
                className="bg-sky-500/15 font-mono text-sky-600 dark:bg-sky-500/20 dark:text-sky-300"
              >
                <ZapIcon size={14} />
                <Chip.Label>Auto</Chip.Label>
              </Chip>
            </Tooltip.Trigger>
            <Tooltip.Content>
              {createdAt
                ? `Synced @ ${formatDateTime(createdAt)}`
                : "Synced by the scheduler"}
            </Tooltip.Content>
          </Tooltip>
        )}
        {kind && (
          <JobChip variant={kind}>
            <span className="capitalize">{kind}</span>
          </JobChip>
        )}
        {platformText && (
          <JobChip variant="flat" className="max-md:hidden">
            {platformText}
          </JobChip>
        )}
        {audioCodec && (
          <JobChip variant="flat" className="max-md:hidden">
            {`${audioCodec} ${showBitrate && audioBitrate ? `@ ${audioBitrate}kbps` : ""}`}
          </JobChip>
        )}
        {trackCount && kind !== "track" && (
          <JobChip variant="flat" className="max-md:hidden">
            {trackCount} {trackCount === 1 ? "track" : "tracks"}
          </JobChip>
        )}
      </div>
    </div>
  );
}

export function JobCard({ job, onCancel, onDelete }: Props) {
  const isJobActive = isActive(job.status);
  const isJobRunning = isRunning(job.status);
  const isJobFinished = isFinished(job.status);
  const { content_info, download_stats } = job;
  const hasPartialFailures =
    job.status === "completed" && (download_stats?.failed ?? 0) > 0;
  const opacity = job.status === "cancelled" ? "opacity-50" : "";

  return (
    <Card variant="secondary" className={`group ${opacity}`}>
      <Card.Content className="flex-row items-center gap-3">
        <Thumbnail
          url={content_info?.thumbnail_url ?? null}
          status={job.status}
          hasPartialFailures={hasPartialFailures}
        />

        <div className="min-w-0 flex-1">
          {content_info?.title ? (
            <ContentInfo
              title={content_info.title}
              artist={content_info.artist ?? null}
              year={content_info.year ?? null}
              trackCount={content_info.track_count ?? null}
              audioCodec={content_info.audio_codec ?? null}
              audioBitrate={content_info.audio_bitrate ?? null}
              showBitrate={isJobFinished}
              kind={content_info.kind ?? null}
              platform={content_info.platform ?? null}
              source={job.source}
              createdAt={job.created_at}
            />
          ) : (
            <p className="text-muted truncate font-mono text-xs">{job.url}</p>
          )}
        </div>

        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Open source"
          className={cn(
            buttonVariants({
              size: "sm",
              variant: "ghost",
              isIconOnly: true,
            }),
            "icon-action shrink-0 md:not-group-hover:hidden",
          )}
        >
          <ExternalLinkIcon className="h-4 w-4" />
        </a>

        {isJobActive && onCancel && (
          <Button
            variant="ghost"
            aria-label="Cancel job"
            size="sm"
            isIconOnly
            className="icon-action shrink-0 md:not-group-hover:hidden"
            onPress={() => onCancel(job.id)}
          >
            <XIcon className="h-4 w-4" />
          </Button>
        )}

        {isJobFinished && onDelete && (
          <Button
            variant="ghost"
            aria-label="Delete job"
            size="sm"
            isIconOnly
            className="icon-action hover:text-danger shrink-0 not-group-hover:hidden max-md:hidden"
            onPress={() => onDelete(job.id)}
          >
            <Trash2Icon className="h-4 w-4" />
          </Button>
        )}
      </Card.Content>

      {isJobRunning && (
        <Card.Footer className="gap-2">
          <ProgressBar
            value={job.progress}
            size="md"
            color={STATUS_CONFIG[job.status].progressColor}
            className="flex-1"
            aria-label="Job progress"
          >
            <ProgressBar.Track>
              <ProgressBar.Fill className="transition-all duration-500 ease-out" />
            </ProgressBar.Track>
          </ProgressBar>
          <span className="text-muted w-8 text-right font-mono text-sm">
            {Math.round(job.progress)}%
          </span>
        </Card.Footer>
      )}
    </Card>
  );
}
