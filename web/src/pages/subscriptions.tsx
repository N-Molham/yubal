import { UrlInput } from "@/components/common/url-input";
import { SubscriptionCard } from "@/features/subscriptions/subscription-card";
import { SubscriptionsTable } from "@/features/subscriptions/subscriptions-table";
import { useSubscriptions } from "@/features/subscriptions/use-subscriptions";
import { useScheduleCountdown } from "@/hooks/use-schedule-countdown";
import { guessPlatformFromUrl } from "@/lib/platform";
import { isValidUrl } from "@/lib/url";
import {
  Alert,
  Button,
  Card,
  Checkbox,
  InputGroup,
  NumberField,
  Spinner,
} from "@heroui/react";
import {
  CircleQuestionMarkIcon,
  ClockIcon,
  HashIcon,
  ListMusicIcon,
  RefreshCw,
  ZapIcon,
  ZapOffIcon,
} from "lucide-react";
import { useState } from "react";

const DEFAULT_MAX_ITEMS = 100;

export function SubscriptionsPage() {
  const [url, setUrl] = useState("");
  const [maxItems, setMaxItems] = useState(DEFAULT_MAX_ITEMS);
  const [isPodcast, setIsPodcast] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const {
    subscriptions,
    schedulerStatus,
    isLoading,
    addSubscription,
    updateSubscription,
    deleteSubscription,
    syncSubscription,
    syncAll,
  } = useSubscriptions();
  const [isSyncing, setIsSyncing] = useState(false);

  const canAdd = isValidUrl(url);
  const isEmpty = subscriptions.length == 0;
  const canSyncAll = !isEmpty && !isSyncing && !isLoading;
  // Coarse client-only guess, just to show/hide this picker — the backend
  // is the real authority (rejects is_podcast for non-YouTube URLs).
  const showPodcastPicker = guessPlatformFromUrl(url) === "youtube";

  const handleAdd = async () => {
    if (!canAdd) return;
    setIsAdding(true);
    const success = await addSubscription(
      url.trim(),
      maxItems,
      showPodcastPicker && isPodcast,
    );
    if (success) {
      setUrl("");
    }
    setIsAdding(false);
  };

  const handleToggleEnabled = async (id: string, enabled: boolean) => {
    await updateSubscription(id, { enabled });
  };

  const handleSyncAll = async () => {
    setIsSyncing(true);
    await syncAll();
    setIsSyncing(false);
  };

  const countdown = useScheduleCountdown(
    schedulerStatus?.cron_expression,
    schedulerStatus?.timezone,
  );
  const enabledCount = subscriptions.filter((s) => s.enabled).length;
  const totalCount = subscriptions.length;

  return (
    <>
      {/* Page Title */}
      <h1 className="text-foreground mb-6 text-2xl font-bold">My playlists</h1>

      {/* URL Input Section */}
      <section className="mb-8 flex flex-col gap-2">
        <div className="flex gap-2">
          <div className="min-w-0 flex-1">
            <UrlInput
              value={url}
              onChange={setUrl}
              disabled={isAdding}
              placeholder="Playlist URL to sync automatically"
            />
          </div>
          <NumberField
            className="w-24"
            aria-label="Max tracks to sync per run"
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
            onPress={handleAdd}
            isDisabled={!canAdd}
            isPending={isAdding}
          >
            {({ isPending }) => (
              <>
                {isPending ? (
                  <Spinner color="current" size="sm" />
                ) : (
                  <ZapIcon className="h-4 w-4" />
                )}
                Subscribe
              </>
            )}
          </Button>
        </div>
        {showPodcastPicker && (
          <Checkbox isSelected={isPodcast} onChange={setIsPodcast}>
            <Checkbox.Content>
              <Checkbox.Control>
                <Checkbox.Indicator />
              </Checkbox.Control>
              Treat synced episodes as podcasts (files go to _Podcasts/, no
              lyrics or album gain)
            </Checkbox.Content>
          </Checkbox>
        )}
      </section>

      {/* Stats Cards */}
      <div className="mb-6 grid w-full grid-cols-1 gap-4 md:grid-cols-3">
        {/* Active playlists */}
        <SubscriptionCard isDisabled={!schedulerStatus?.enabled}>
          <SubscriptionCard.Header title="Active">
            <SubscriptionCard.Value suffix={`of ${totalCount}`}>
              <span className="font-mono">{enabledCount}</span>
            </SubscriptionCard.Value>
          </SubscriptionCard.Header>
          <SubscriptionCard.Icon className="text-success bg-success/10">
            <ListMusicIcon />
          </SubscriptionCard.Icon>
        </SubscriptionCard>
        {/* Next sync */}
        <SubscriptionCard isDisabled={!schedulerStatus?.enabled}>
          <SubscriptionCard.Header title="Next sync">
            <SubscriptionCard.Value suffix="remaining">
              <span className="font-mono">{countdown}</span>
            </SubscriptionCard.Value>
          </SubscriptionCard.Header>
          <SubscriptionCard.Icon>
            <ClockIcon />
          </SubscriptionCard.Icon>
        </SubscriptionCard>
        {/* Sync all button */}
        {/* The card's padding lives on the button so the whole card is the
            hit target and the hover highlight covers it edge to edge. */}
        <Card className={`p-0 ${canSyncAll ? "" : "opacity-50"}`}>
          <button
            type="button"
            disabled={!canSyncAll}
            onClick={handleSyncAll}
            className="group enabled:hover:bg-surface-hover flex flex-1 cursor-pointer flex-col items-center justify-center gap-2 rounded-[inherit] p-4 transition-colors disabled:cursor-not-allowed"
          >
            <RefreshCw
              size={24}
              className={`mb-1 ${isSyncing ? "text-success animate-spin" : "transition-transform duration-500 group-hover:rotate-180"}`}
            />
            <span className="text-sm font-medium">
              {isSyncing ? "Synchronizing..." : "Sync all now"}
            </span>
          </button>
        </Card>
      </div>
      {/* Scheduler disabled alert */}
      {schedulerStatus?.enabled === false && (
        <div className="mb-6 flex w-full items-center justify-center">
          <Alert status="warning">
            <Alert.Indicator>
              <ZapOffIcon size={18} />
            </Alert.Indicator>
            <Alert.Content>
              <Alert.Title>Scheduler is disabled.</Alert.Title>
              <Alert.Description>
                You can still add playlists and sync them manually.
              </Alert.Description>
            </Alert.Content>
            <a
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Configuration docs"
              href="https://github.com/guillevc/yubal?tab=readme-ov-file#%EF%B8%8F-configuration"
            >
              <CircleQuestionMarkIcon size={20} className="mr-2" />
            </a>
          </Alert>
        </div>
      )}
      {/* Subscriptions Table */}
      <SubscriptionsTable
        subscriptions={subscriptions}
        isLoading={isLoading}
        isSchedulerEnabled={schedulerStatus?.enabled}
        onToggleEnabled={handleToggleEnabled}
        onSync={syncSubscription}
        onDelete={deleteSubscription}
      />
    </>
  );
}
