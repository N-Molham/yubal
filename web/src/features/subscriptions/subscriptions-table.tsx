import type { Subscription } from "@/api/subscriptions";
import { useTimeAgo } from "@/hooks/use-time-ago";
import { platformLabel } from "@/lib/platform";
import { Button, EmptyState, Spinner, Switch, Table } from "@heroui/react";
import {
  InboxIcon,
  ListMusicIcon,
  RefreshCwIcon,
  Trash2Icon,
} from "lucide-react";
import { useCallback } from "react";

type ColumnKey = "name" | "lastSynced" | "limit" | "enabled" | "actions";

function TimeAgo({ dateString }: { dateString: string | null | undefined }) {
  return useTimeAgo(dateString);
}

const columns: { name: string; id: ColumnKey }[] = [
  { name: "Playlist", id: "name" },
  { name: "Last synced", id: "lastSynced" },
  { name: "Limit", id: "limit" },
  { name: "Enabled", id: "enabled" },
  { name: "Actions", id: "actions" },
];

type SubscriptionsTableProps = {
  subscriptions: Subscription[];
  isLoading?: boolean;
  isSchedulerEnabled?: boolean;
  onToggleEnabled: (id: string, enabled: boolean) => void;
  onSync: (id: string) => void;
  onDelete: (id: string) => void;
};

export function SubscriptionsTable({
  subscriptions,
  isLoading,
  isSchedulerEnabled,
  onToggleEnabled,
  onSync,
  onDelete,
}: SubscriptionsTableProps) {
  const renderCell = useCallback(
    (
      subscription: Subscription,
      isSchedulerEnabled: boolean,
      columnKey: ColumnKey,
    ) => {
      switch (columnKey) {
        case "name":
          return (
            <div className="flex items-center gap-3">
              {subscription.thumbnail_url ? (
                <img
                  alt=""
                  src={subscription.thumbnail_url}
                  className="size-10 shrink-0 rounded-md object-cover max-md:hidden"
                />
              ) : (
                <div className="bg-surface-tertiary flex size-10 shrink-0 items-center justify-center rounded-md max-md:hidden">
                  <ListMusicIcon className="text-muted size-5" />
                </div>
              )}
              <div className="flex flex-col">
                <span>{subscription.name}</span>
                <span className="text-muted text-xs font-normal">
                  {platformLabel(subscription.platform)}
                  {subscription.is_podcast ? " · Podcast" : ""}
                </span>
              </div>
            </div>
          );
        case "lastSynced":
          return <TimeAgo dateString={subscription.last_synced_at} />;
        case "limit":
          return subscription.max_items ?? "∞";
        case "enabled":
          return (
            <Switch
              size="sm"
              isDisabled={!isSchedulerEnabled}
              isSelected={subscription.enabled}
              onChange={(enabled) => onToggleEnabled(subscription.id, enabled)}
              aria-label="Toggle auto-sync"
            >
              <Switch.Content>
                <Switch.Control>
                  <Switch.Thumb />
                </Switch.Control>
              </Switch.Content>
            </Switch>
          );
        case "actions":
          return (
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="sm"
                isIconOnly
                aria-label="Sync now"
                className="icon-action"
                onPress={() => onSync(subscription.id)}
              >
                <RefreshCwIcon className="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                isIconOnly
                aria-label="Delete playlist"
                className="icon-action hover:text-danger"
                onPress={() => onDelete(subscription.id)}
              >
                <Trash2Icon className="size-4" />
              </Button>
            </div>
          );
      }
    },
    [onToggleEnabled, onSync, onDelete],
  );

  return (
    <Table>
      <Table.ScrollContainer>
        <Table.Content aria-label="Subscribed playlists">
          <Table.Header columns={columns}>
            {(column) => (
              <Table.Column id={column.id} isRowHeader={column.id === "name"}>
                {column.name}
              </Table.Column>
            )}
          </Table.Header>
          <Table.Body
            items={isLoading ? [] : subscriptions}
            renderEmptyState={() =>
              isLoading ? (
                <EmptyState className="flex min-h-[160px] w-full flex-col items-center justify-center gap-4 text-center">
                  <Spinner size="sm" />
                  <span className="text-muted text-sm">Loading...</span>
                </EmptyState>
              ) : (
                <EmptyState className="flex min-h-[160px] w-full flex-col items-center justify-center gap-4 text-center">
                  <InboxIcon className="text-muted size-6" />
                  <span className="text-muted text-sm">
                    No playlists registered
                  </span>
                </EmptyState>
              )
            }
          >
            {(subscription) => (
              <Table.Row id={subscription.id}>
                {columns.map((column) => (
                  <Table.Cell key={column.id}>
                    {renderCell(subscription, !!isSchedulerEnabled, column.id)}
                  </Table.Cell>
                ))}
              </Table.Row>
            )}
          </Table.Body>
        </Table.Content>
      </Table.ScrollContainer>
    </Table>
  );
}
