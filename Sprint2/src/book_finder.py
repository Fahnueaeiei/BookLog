"""Google Books API client (Data Access Layer) for BookLog (Sprint 2).

BookFinder is the only place in the application that talks to the
Google Books API. It turns API responses into Book objects and turns
network/API problems into a single APIError, so the business logic
and the UI never have to deal with requests or raw JSON.
"""

import os

import requests
from dotenv import load_dotenv

from src.exceptions import APIError
from src.models import Book

# Loads variables from a .env file in the project root (if one exists)
# into the environment, so GOOGLE_BOOKS_API_KEY does not need to be
# exported manually every time a new terminal session is opened. Has
# no effect, and raises no error, if no .env file is present.
load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Maps BookLog's search fields to the Google Books query prefixes.
# Same field names as Sprint 1's mock search (title, author, genre),
# so the CLI does not need to change when it switches to BookFinder.
FIELD_PREFIXES = {
    "title": "intitle",
    "author": "inauthor",
    "genre": "subject",
}


class BookFinder:
    """Searches Google Books and builds Book objects from the results.

    Attributes:
        api_key: Google Books API key, or None to call the API without
            one (works, but with a lower rate limit).
        timeout: Seconds to wait for a response before giving up.
    """

    def __init__(self, api_key=None, timeout=10):
        """Create a BookFinder.

        Args:
            api_key: API key to use. If None, falls back to the
                GOOGLE_BOOKS_API_KEY environment variable, and if that
                is not set either, requests are sent without a key.
            timeout: Seconds to wait for a response before raising
                APIError.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_BOOKS_API_KEY")
        self.timeout = timeout

    def search(self, field, keyword, max_results=20):
        """Search Google Books by title, author, or genre.

        Args:
            field: One of "title", "author", or "genre".
            keyword: Text to search for.
            max_results: Maximum number of results to return (1-40,
                per the Google Books API's own limit).

        Returns:
            A list of Book objects. Empty if nothing matches.

        Raises:
            ValueError: If field is not "title", "author", or "genre".
            APIError: If the API cannot be reached or returns a
                response that cannot be used.
        """
        if field not in FIELD_PREFIXES:
            raise ValueError(f"Unknown search field: {field}")

        query = f"{FIELD_PREFIXES[field]}:{keyword}"
        data = self._get(BASE_URL, {"q": query, "maxResults": max_results})

        items = data.get("items") or []
        return [self._parse_volume(item) for item in items]

    def get_details(self, book_id):
        """Fetch the full details of one book by its Google Books ID.

        Args:
            book_id: Google Books volume ID.

        Returns:
            A Book object.

        Raises:
            APIError: If the API cannot be reached, the book is not
                found, or the response cannot be used.
        """
        item = self._get(f"{BASE_URL}/{book_id}")
        return self._parse_volume(item)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get(self, url, params=None):
        """Make a GET request and return the parsed JSON body.

        Raises:
            APIError: For a timeout, a connection problem, an HTTP
                error status, or a response body that is not valid
                JSON.
        """
        params = dict(params or {})
        if self.api_key:
            params["key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.Timeout as error:
            raise APIError(
                "Google Books API did not respond in time.", cause=error
            ) from error
        except requests.ConnectionError as error:
            raise APIError(
                "Could not connect to Google Books API. Check your "
                "network connection.",
                cause=error,
            ) from error
        except requests.HTTPError as error:
            raise APIError(
                f"Google Books API returned an error: {error}",
                cause=error,
            ) from error
        except requests.RequestException as error:
            raise APIError(
                f"Google Books API request failed: {error}", cause=error
            ) from error

        try:
            return response.json()
        except ValueError as error:
            raise APIError(
                "Google Books API returned a response that could not "
                "be read.",
                cause=error,
            ) from error

    @staticmethod
    def _parse_volume(item):
        """Turn one Google Books API "volume" item into a Book.

        Missing fields become None (or an empty list for authors and
        categories) rather than raising an error, so a book with
        incomplete data still displays with the CLI's placeholders.
        """
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