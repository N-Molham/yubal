"""Source-provider abstraction.

Each supported source (YouTube Music today; YouTube and SoundCloud later)
implements ``SourceProvider``. The registry dispatches a URL to the first
provider that claims it.
"""

from yubal.providers.base import SourceProvider, UrlMatch
from yubal.providers.registry import classify_source, get_provider, is_supported_url

__all__ = [
    "SourceProvider",
    "UrlMatch",
    "classify_source",
    "get_provider",
    "is_supported_url",
]
