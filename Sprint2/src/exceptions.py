"""Custom exceptions for BookLog (Sprint 2 - Business Logic Layer).

All BookLog-specific errors inherit from BookLibraryError, so callers
(CLI, web app) can catch that one base class if they just want to show
a generic "something went wrong" message, or catch a specific subclass
for a more precise one.
"""


class BookLibraryError(Exception):
    """Base class for every BookLog-specific error."""


class BookNotFoundError(BookLibraryError):
    """Raised when a book_id is not found in the library.

    Raised by operations that update or remove an existing library
    entry (e.g. ReadingTracker, Library.remove_book).
    """

    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"No library entry found for book_id '{book_id}'.")


class DuplicateBookError(BookLibraryError):
    """Raised when adding a book that is already in the library."""

    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"Book '{book_id}' is already in the library.")


class InvalidRatingError(BookLibraryError):
    """Raised when a rating is not a whole number from 1 to 5."""

    def __init__(self, rating):
        self.rating = rating
        super().__init__(
            f"Rating must be a whole number from 1 to 5, got {rating!r}."
        )


class InvalidProgressError(BookLibraryError):
    """Raised when pages_read is negative or above the page count."""

    def __init__(self, pages_read, page_count):
        self.pages_read = pages_read
        self.page_count = page_count
        if page_count is None:
            message = f"Pages read ({pages_read}) cannot be negative."
        else:
            message = (
                f"Pages read ({pages_read}) must be between 0 and "
                f"{page_count}."
            )
        super().__init__(message)


class APIError(BookLibraryError):
    """Raised when the Google Books API cannot be reached or returns
    an unusable response (timeout, no network, bad status code, or a
    response that cannot be parsed).
    """

    def __init__(self, message, cause=None):
        self.cause = cause
        super().__init__(message)


class DatabaseError(BookLibraryError):
    """Raised when the SQLite database file is missing data it should
    have, or cannot be read (e.g. it is corrupted).
    """

    def __init__(self, message, cause=None):
        self.cause = cause
        super().__init__(message)