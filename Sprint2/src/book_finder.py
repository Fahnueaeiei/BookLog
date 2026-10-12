"""Google Books API client (Data Access Layer) for BookLog (Sprint 2).

BookFinder is the only place in the application that talks to the
Google Books API. It converts API responses into Book objects and
translates network/API problems into APIError exceptions.
"""

import os
import time

import requests
from dotenv import load_dotenv

from src.exceptions import APIError
from src.models import Book


# Load environment variables from a .env file if available.
load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Map BookLog search fields to Google Books query prefixes.
FIELD_PREFIXES = {
    "title": "intitle",
    "author": "inauthor",
    "genre": "subject",
}

RETRYABLE_STATUS_CODES = {500, 502, 503, 504}
MAX_ATTEMPTS = 4


class BookFinder:
    """Search Google Books and convert results into Book objects."""

    def __init__(self, api_key=None, timeout=10):
        """Initialize the API client.

        Args:
            api_key: Optional Google Books API key. If omitted, the
                GOOGLE_BOOKS_API_KEY environment variable is used.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_BOOKS_API_KEY")
        self.timeout = timeout

    def search(self, field, keyword, max_results=20):
        """Search books by title, author, or genre.

        Returns:
            A list of Book objects. Returns an empty list if no
            results are found.

        Raises:
            ValueError: If the search arguments are invalid.
            APIError: If the API request or response fails.
        """
        if field not in FIELD_PREFIXES:
            raise ValueError(f"Unknown search field: {field}")

        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")

        if (
            not isinstance(max_results, int)
            or isinstance(max_results, bool)
            or not 1 <= max_results <= 40
        ):
            raise ValueError(
                "max_results must be a whole number from 1 to 40."
            )

        keyword = keyword.strip()
        query = f"{FIELD_PREFIXES[field]}:{keyword}"

        data = self._get(
            BASE_URL,
            {"q": query, "maxResults": max_results},
        )

        if not isinstance(data, dict):
            raise APIError("Google Books API returned an unusable response.")

        items = data.get("items") or []

        # Retry the search with a plain keyword if the filtered search
        # returns no results.
        if not items:
            data = self._get(
                BASE_URL,
                {"q": keyword, "maxResults": max_results},
            )

            if not isinstance(data, dict):
                raise APIError(
                    "Google Books API returned an unusable response."
                )

            items = data.get("items") or []

        return [self._parse_volume(item) for item in items]

    def get_details(self, book_id):
        """Fetch details for a book by its Google Books volume ID."""
        if not isinstance(book_id, str) or not book_id.strip():
            raise ValueError("book_id cannot be empty.")

        url = f"{BASE_URL}/{book_id.strip()}"
        item = self._get(url)

        if not isinstance(item, dict):
            raise APIError("Google Books API returned an unusable response.")

        return self._parse_volume(item)

    def _get(self, url, params=None):
        """Send a GET request and return the parsed JSON response.

        Retries up to three times after the initial request when a
        timeout or temporary server error occurs. Delays are 1, 2,
        and 4 seconds.

        Raises:
            APIError: If the request fails or the response is invalid.
        """
        request_params = dict(params or {})

        if self.api_key:
            request_params["key"] = self.api_key

        # Cloud servers often have IPs Google cannot geolocate (HTTP 403
        # "unknownLocation"). Passing a country code avoids that.
        request_params.setdefault("country", "US")

        response = None

        for attempt in range(MAX_ATTEMPTS):
            try:
                response = requests.get(
                    url,
                    params=request_params,
                    timeout=self.timeout,
                )

                if (
                    response.status_code in RETRYABLE_STATUS_CODES
                    and attempt < MAX_ATTEMPTS - 1
                ):
                    time.sleep(2 ** attempt)
                    continue

                response.raise_for_status()
                break

            except requests.Timeout as error:
                if attempt < MAX_ATTEMPTS - 1:
                    time.sleep(2 ** attempt)
                    continue

                raise APIError(
                    "Google Books API did not respond in time.",
                    cause=error,
                ) from error

            except requests.ConnectionError as error:
                raise APIError(
                    "Could not connect to Google Books API. Check your "
                    "network connection.",
                    cause=error,
                ) from error

            except requests.HTTPError as error:
                status_code = error.response.status_code
                error_message = ""
                error_reason = ""

                try:
                    error_body = error.response.json()
                    api_error = error_body.get("error", {})
                    error_message = api_error.get("message", "")

                    errors = api_error.get("errors") or []
                    if errors and isinstance(errors[0], dict):
                        error_reason = errors[0].get("reason", "")

                except (ValueError, AttributeError, IndexError):
                    pass

                details = f"HTTP {status_code}"

                if error_reason:
                    details += f" ({error_reason})"

                if error_message:
                    details += f": {error_message}"

                raise APIError(
                    f"Google Books API returned an error: {details}",
                    cause=error,
                ) from error

            except requests.RequestException as error:
                raise APIError(
                    f"Google Books API request failed: {error}",
                    cause=error,
                ) from error

        try:
            return response.json()
        except (ValueError, AttributeError) as error:
            raise APIError(
                "Google Books API returned a response that could not "
                "be read.",
                cause=error,
            ) from error

    @staticmethod
    def _parse_volume(item):
        """Convert a Google Books API volume item into a Book object."""
        info = item.get("volumeInfo", {}) or {}
        image_links = info.get("imageLinks") or {}

        return Book(
            book_id=item.get("id", ""),
            title=info.get("title") or "Untitled",
            authors=info.get("authors") or [],
            description=info.get("description"),
            published_date=info.get("publishedDate"),
            categories=info.get("categories") or [],
            cover_url=image_links.get("thumbnail"),
            page_count=info.get("pageCount"),
        )
