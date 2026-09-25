"""Domain models for BookLog (Sprint 2 - Business Logic Layer).

This module holds plain data classes only: Book, ReadingStatus, and
LibraryEntry. No printing, no input, no SQL, and no validation rules
live here. Validation belongs to ReadingTracker; persistence belongs
to DataStore; display belongs to the CLI / web app.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# Matches "YYYY", "YYYY-MM", or "YYYY-MM-DD" and captures the year.
_YEAR_PATTERN = re.compile(r"^(\d{4})")


class ReadingStatus(Enum):
    """Reading status of a book in the library.

    Each member carries a human-readable label so the CLI and the web
    app can both display it without keeping a separate lookup table.
    """

    WANT_TO_READ = ("want_to_read", "Want to Read")
    READING = ("reading", "Reading")
    COMPLETED = ("completed", "Completed")

    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        """Return the human-readable label."""
        return self.label


@dataclass
class Book:
    """Information about one book, as returned by BookFinder.

    Attributes:
        book_id: Google Books volume ID. Used as the book's identity.
        title: Book title.
        authors: List of author names. Empty if unknown.
        description: Short description, or None if missing.
        published_date: Raw published date as given by the API, in the
            form "YYYY", "YYYY-MM", or "YYYY-MM-DD". None if missing.
        categories: List of category/genre names. Empty if unknown.
        cover_url: URL of the cover image, or None if missing.
        page_count: Total number of pages, or None if unknown.
    """

    book_id: str
    title: str = field(compare=False)
    authors: list = field(default_factory=list, compare=False)
    description: Optional[str] = field(default=None, compare=False)
    published_date: Optional[str] = field(default=None, compare=False)
    categories: list = field(default_factory=list, compare=False)
    cover_url: Optional[str] = field(default=None, compare=False)
    page_count: Optional[int] = field(default=None, compare=False)

    @property
    def published_year(self):
        """Return the publication year as an int, or None if unknown.

        Handles all three date formats used in the mock data and
        expected from the Google Books API: "YYYY", "YYYY-MM", and
        "YYYY-MM-DD".
        """
        if not self.published_date:
            return None

        match = _YEAR_PATTERN.match(self.published_date)
        return int(match.group(1)) if match else None


@dataclass
class LibraryEntry:
    """A book in the user's personal library, plus their reading data.

    Attributes:
        book: The Book this entry is about.
        status: Current ReadingStatus.
        pages_read: Pages read so far. 0 by default.
        rating: Personal rating from 1 to 5, or None if not rated.
        notes: Free-text notes. Empty string if none.
        added_at: ISO timestamp of when the book was added.
    """

    book: Book
    status: ReadingStatus
    pages_read: int = 0
    rating: Optional[int] = None
    notes: str = ""
    added_at: str = ""

    @property
    def progress_percent(self):
        """Return reading progress as a percentage (0-100), or None.

        Returns None when the book's page count is unknown, since a
        percentage cannot be calculated without it.
        """
        page_count = self.book.page_count
        if not page_count:
            return None
        return round(100 * self.pages_read / page_count)