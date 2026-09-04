"""Job API schemas."""

from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, WithJsonSchema, model_validator
from yubal import Source, classify_source, is_supported_url

from yubal_api.domain.job import Job


def validate_youtube_music_url(url: str) -> str:
    """Validate that the URL is supported by yubal.

    Uses yubal's is_supported_url() as the source of truth to ensure
    the API accepts exactly what yubal can process.
    """
    url = url.strip()
    if not is_supported_url(url):
        raise ValueError(
            "Invalid URL. Expected a YouTube or YouTube Music URL "
            "(e.g., https://youtube.com/watch?v=... or "
            "https://music.youtube.com/playlist?list=...)"
        )
    return url


YouTubeMusicUrl = Annotated[
    str,
    AfterValidator(validate_youtube_music_url),
    WithJsonSchema({"type": "string", "format": "uri"}),
]


class CreateJobRequest(BaseModel):
    """Request to create a new sync job."""

    url: YouTubeMusicUrl = Field(
        description="YouTube or YouTube Music playlist, album, or single track URL",
        examples=[
            "https://music.youtube.com/playlist?list=OLAK5uy_...",
            "https://www.youtube.com/watch?v=VIDEO_ID",
        ],
    )
    max_items: int | None = Field(
        default=None,
        ge=1,
        le=10000,
        description="Maximum number of tracks to download",
    )
    download_ugc: bool | None = Field(
        default=None,
        description="Include non-music/UGC videos for this job. "
        "Defaults to the instance-wide YUBAL_DOWNLOAD_UGC setting when omitted.",
    )
    is_podcast: bool = Field(
        default=False,
        description="Treat this as a podcast episode, not music. Only valid "
        "for plain YouTube URLs (not YouTube Music or SoundCloud) — never "
        "auto-detected, always an explicit user choice.",
    )

    @model_validator(mode="after")
    def _podcast_requires_youtube_source(self) -> "CreateJobRequest":
        if self.is_podcast and classify_source(self.url) != Source.YOUTUBE:
            raise ValueError(
                "is_podcast is only valid for plain YouTube URLs, not "
                "YouTube Music or SoundCloud"
            )
        return self


class JobsResponse(BaseModel):
    """Response for listing jobs."""

    jobs: list[Job]


class JobCreatedResponse(BaseModel):
    """Response when a job is created."""

    id: str
    message: Literal["Job created"] = "Job created"


class ClearJobsResponse(BaseModel):
    """Response when jobs are cleared."""

    cleared: int


class CancelJobResponse(BaseModel):
    """Response when a job is cancelled."""

    message: Literal["Job cancelled"] = "Job cancelled"


# SSE Event schemas


class SnapshotEvent(BaseModel):
    """Initial snapshot of all jobs sent on SSE connection."""

    type: Literal["snapshot"] = "snapshot"
    jobs: list[Job]


class CreatedEvent(BaseModel):
    """Emitted when a new job is created."""

    type: Literal["created"] = "created"
    job: Job


class UpdatedEvent(BaseModel):
    """Emitted when a job's status or progress changes."""

    type: Literal["updated"] = "updated"
    job: Job


class DeletedEvent(BaseModel):
    """Emitted when a job is deleted."""

    type: Literal["deleted"] = "deleted"
    jobId: str


class ClearedEvent(BaseModel):
    """Emitted when finished jobs are cleared."""

    type: Literal["cleared"] = "cleared"
    count: int
