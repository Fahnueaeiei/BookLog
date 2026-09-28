from datetime import datetime, timezone

from src.exceptions import BookNotFoundError, DuplicateBookError
from src.models import LibraryEntry, ReadingStatus


SORT_KEYS = ("rating", "published_year", "title", "added_at")


class Library:
    """The user's personal library: add, remove, view, search, filter, sort.

    Attributes:
        data_store: The DataStore used to persist changes.
    """

    def __init__(self, data_store):
        """Load the existing library from data_store into memory.

        Args:
            data_store: A DataStore instance.
        """
        self.data_store = data_store
        self._entries = {
            entry.book.book_id: entry
            for entry in self.data_store.load_entries()
        }

    # ------------------------------------------------------------------
    # Refresh
    # ------------------------------------------------------------------

    def _refresh_entries(self):
        """Refresh in-memory entries from the database."""
        entries = self.data_store.load_entries()

        self._entries = {
            entry.book.book_id: entry
            for entry in entries
        }

    # ------------------------------------------------------------------
    # Add / remove / view
    # ------------------------------------------------------------------

    def add_book(self, book):
        """Add a book to the library as 'Want to Read'.

        Args:
            book: The Book to add.

        Returns:
            The new LibraryEntry.

        Raises:
            DuplicateBookError: If a book with the same book_id is
                already in the library.
        """
        if book.book_id in self._entries:
            raise DuplicateBookError(book.book_id)

        entry = LibraryEntry(
            book=book,
            status=ReadingStatus.WANT_TO_READ,
            pages_read=0,
            rating=None,
            notes="",
            added_at=datetime.now(timezone.utc).isoformat(),
        )

        self.data_store.save_entry(entry)
        self._entries[book.book_id] = entry

        return entry

    def remove_book(self, book_id):
        """Remove a book from the library.

        Args:
            book_id: The book_id of the entry to remove.

        Raises:
            BookNotFoundError: If book_id is not in the library.
        """
        if book_id not in self._entries:
            raise BookNotFoundError(book_id)

        self.data_store.delete_entry(book_id)
        del self._entries[book_id]

    def get_entries(self):
        """Return every entry in the library, in no particular order."""
        self._refresh_entries()
        return list(self._entries.values())

    def get_entry(self, book_id):
        """Return one entry by book_id.

        Raises:
            BookNotFoundError: If book_id is not in the library.
        """
        self._refresh_entries()

        try:
            return self._entries[book_id]
        except KeyError:
            raise BookNotFoundError(book_id) from None

    def update_entry(self, entry):
        """Update an existing library entry."""
        if entry.book.book_id not in self._entries:
            raise BookNotFoundError(entry.book.book_id)

        self.data_store.save_entry(entry)
        self._entries[entry.book.book_id] = entry

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, keyword):
        keyword = keyword.strip().lower()

        if not keyword:
            return []

        results = []

        for entry in self._entries.values():
            book = entry.book

            texts = [
                book.title,
                *book.authors,
                *book.categories,
            ]

            if any(
                keyword in text.lower()
                for text in texts
                if text
            ):
                results.append(entry)

        return results

    # ------------------------------------------------------------------
    # Filter
    # ------------------------------------------------------------------

    def filter_entries(
        self,
        status=None,
        category=None,
        min_rating=None,
    ):
        results = list(self._entries.values())

        if status is not None:
            results = [
                entry
                for entry in results
                if entry.status == status
            ]

        if category is not None:
            category = category.strip().lower()

            results = [
                entry
                for entry in results
                if any(
                    category == book_category.lower()
                    for book_category in entry.book.categories
                )
            ]

        if min_rating is not None:
            results = [
                entry
                for entry in results
                if entry.rating is not None
                and entry.rating >= min_rating
            ]

        return results

    # ------------------------------------------------------------------
    # Sort
    # ------------------------------------------------------------------

    def sort_entries(self, entries, key, reverse=False):
        if key not in SORT_KEYS:
            raise ValueError(f"Unknown sort key: {key}")

        def sort_value(entry):
            if key == "rating":
                return entry.rating

            if key == "published_year":
                return entry.book.published_year

            if key == "title":
                return (
                    entry.book.title.lower()
                    if entry.book.title
                    else None
                )

            return entry.added_at or None

        with_value = [
            entry
            for entry in entries
            if sort_value(entry) is not None
        ]

        missing_value = [
            entry
            for entry in entries
            if sort_value(entry) is None
        ]

        with_value.sort(
            key=sort_value,
            reverse=reverse,
        )

        return with_value + missing_value