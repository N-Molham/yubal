"""Subscription business logic service."""

import logging
from datetime import UTC, datetime
from uuid import UUID

from yubal import (
    AuthenticationRequiredError,
    PlaylistNotFoundError,
    PlaylistParseError,
    Source,
    UnsupportedPlaylistError,
    UpstreamAPIError,
    classify_source,
)

from yubal_api.api.exceptions import (
    MetadataFetchError,
    SubscriptionConflictError,
    SubscriptionNotFoundError,
)
from yubal_api.db.subscription import (
    Subscription,
    SubscriptionFields,
    SubscriptionOrigin,
    SubscriptionType,
)
from yubal_api.services.playlist_info_service import PlaylistInfoService
from yubal_api.services.protocols import SubscriptionRepository

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Use-case layer for subscription operations.

    Encapsulates business logic for subscription CRUD, keeping route handlers
    thin (HTTP concerns only). PlaylistInfoService is injected as a concrete
    type (single implementation) — extract to a protocol if a second
    implementation is ever needed.
    """

    def __init__(
        self,
        repository: SubscriptionRepository,
        playlist_info: PlaylistInfoService,
    ) -> None:
        self._repository = repository
        self._playlist_info = playlist_info

    def list(
        self,
        *,
        enabled: bool | None = None,
        type: SubscriptionType | None = None,
        origin: SubscriptionOrigin | None = None,
    ) -> list[Subscription]:
        return self._repository.list(enabled=enabled, type=type, origin=origin)

    def get(self, subscription_id: UUID) -> Subscription:
        sub = self._repository.get(subscription_id)
        if sub is None:
            raise SubscriptionNotFoundError(subscription_id)
        return sub

    def create(
        self,
        url: str,
        max_items: int | None = None,
        is_podcast: bool = False,
    ) -> Subscription:
        existing = self._repository.get_by_url(url)
        if existing is not None:
            raise SubscriptionConflictError(
                f"Subscription with URL already exists: {existing.id}",
                subscription_id=existing.id,
            )

        try:
            metadata = self._playlist_info.get_playlist_metadata(url)
        except (
            PlaylistNotFoundError,
            AuthenticationRequiredError,
            PlaylistParseError,
            UnsupportedPlaylistError,
            UpstreamAPIError,
        ):
            raise  # Known exceptions — propagate to exception handlers
        except Exception as e:
            logger.warning("Unexpected error fetching metadata for %s: %s", url, e)
            raise MetadataFetchError(str(e), upstream_error=type(e).__name__) from e

        subscription = Subscription(
            type=SubscriptionType.PLAYLIST,
            url=url,
            name=metadata.title,
            thumbnail_url=metadata.thumbnail_url,
            platform=classify_source(url) or Source.YOUTUBE_MUSIC,
            is_podcast=is_podcast,
            enabled=True,
            max_items=max_items,
            created_at=datetime.now(UTC),
        )
        return self._repository.create(subscription)

    def create_auto(
        self,
        url: str,
        name: str,
        origin: SubscriptionOrigin,
        *,
        thumbnail_url: str | None = None,
        max_items: int | None = None,
    ) -> Subscription:
        """Create a subscription discovered from the user's library.

        Unlike :meth:`create`, this does not fetch metadata (discovery already
        has title/thumbnail) and is only called for rows confirmed missing.
        """
        subscription = Subscription(
            type=SubscriptionType.PLAYLIST,
            url=url,
            name=name[:200],
            thumbnail_url=thumbnail_url,
            platform=classify_source(url) or Source.YOUTUBE_MUSIC,
            origin=origin,
            is_podcast=False,
            enabled=True,
            max_items=max_items,
            created_at=datetime.now(UTC),
        )
        return self._repository.create(subscription)

    def update(self, subscription_id: UUID, fields: SubscriptionFields) -> Subscription:
        if not fields:
            return self.get(subscription_id)
        sub = self._repository.update(subscription_id, fields)
        if sub is None:
            raise SubscriptionNotFoundError(subscription_id)
        return sub

    def count(
        self,
        *,
        enabled: bool | None = None,
        type: SubscriptionType | None = None,
        origin: SubscriptionOrigin | None = None,
    ) -> int:
        return self._repository.count(enabled=enabled, type=type, origin=origin)

    def delete(self, subscription_id: UUID) -> None:
        if not self._repository.delete(subscription_id):
            raise SubscriptionNotFoundError(subscription_id)
