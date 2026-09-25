"""Reading rules (Business Logic Layer) for BookLog (Sprint 2).

ReadingTracker enforces the reading rules from PLAN.md sections 3.4
and 3.5: status changes, reading progress, ratings, and notes. It
depends only on Library (never on DataStore directly), and asks
Library to persist every change it makes.
"""

from src.exceptions import InvalidProgressError, InvalidRatingError
from src.models import ReadingStatus

MIN_RATING = 1
MAX_RATING = 5


class ReadingTracker:
    """Changes status, progress, rating, and notes for library entries.

    Attributes:
        library: The Library this tracker updates entries in.
    """

    def __init__(self, library):
        """Create a ReadingTracker.

        Args:
            library: A Library instance. Entries are looked up and
                persisted through it.
        """
        self.library = library

    def set_status(self, book_id, status):
        """Set the reading status of a library entry.

        Marking a book Completed sets its progress to the full page
        count, when the page count is known.

        Args:
            book_id: The book_id of the entry to update.
            status: A ReadingStatus.

        Returns:
            The updated LibraryEntry.

        Raises:
            BookNotFoundError: If book_id is not in the library.
        """
        entry = self.library.get_entry(book_id)
        entry.status = status

        page_count = entry.book.page_count
        if status == ReadingStatus.COMPLETED and page_count:
            entry.pages_read = page_count

        self.library.update_entry(entry)
        return entry

    def update_progress(self, book_id, pages_read):
        """Set how many pages have been read.

        Args:
            book_id: The book_id of the entry to update.
            pages_read: New page count. Must be at least 0, and no
                more than the book's page count when that is known.

        Returns:
            The updated LibraryEntry.

        Raises:
            BookNotFoundError: If book_id is not in the library.
            InvalidProgressError: If pages_read is negative, or
                greater than the book's page count.
        """
        entry = self.library.get_entry(book_id)
        page_count = entry.book.page_count

        too_small = pages_read < 0
        too_big = page_count is not None and pages_read > page_count
        if too_small or too_big:
            raise InvalidProgressError(pages_read, page_count)

        entry.pages_read = pages_read
        self.library.update_entry(entry)
        return entry

    def set_rating(self, book_id, rating):
        """Set or clear the personal rating.

        Args:
            book_id: The book_id of the entry to update.
            rating: A whole number from 1 to 5, or None to clear the
                rating.

        Returns:
            The updated LibraryEntry.

        Raises:
            BookNotFoundError: If book_id is not in the library.
            InvalidRatingError: If rating is not None and is not a
                whole number from 1 to 5.
        """
        entry = self.library.get_entry(book_id)

        if rating is not None:
            is_whole_number = isinstance(rating, int) and not isinstance(
                rating, bool
            )
            if not is_whole_number or not MIN_RATING <= rating <= MAX_RATING:
                raise InvalidRatingError(rating)

        entry.rating = rating
        self.library.update_entry(entry)
        return entry

    def set_notes(self, book_id, notes):
        """Replace the notes for a library entry.

        Args:
            book_id: The book_id of the entry to update.
            notes: New notes text. Pass an empty string to clear the
                notes.

        Returns:
            The updated LibraryEntry.

        Raises:
            BookNotFoundError: If book_id is not in the library.
        """
        entry = self.library.get_entry(book_id)
        entry.notes = notes or ""
        self.library.update_entry(entry)
        return entry