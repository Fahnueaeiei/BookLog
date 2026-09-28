import sys
from pathlib import Path

# =========================================================
# Sprint 2 Path
# =========================================================
REPO_ROOT = Path(__file__).resolve().parents[3]
SPRINT2_PATH = REPO_ROOT / "Sprint2"

if str(SPRINT2_PATH) not in sys.path:
    sys.path.insert(0, str(SPRINT2_PATH))

from dotenv import load_dotenv

load_dotenv(SPRINT2_PATH / ".env")

DB_PATH = SPRINT2_PATH / "data" / "booklog.db"


# =========================================================
# Import Sprint 2
# =========================================================
from src.book_finder import BookFinder
from src.data_store import DataStore
from src.library import Library
from src.reading_tracker import ReadingTracker
from src.models import Book, ReadingStatus


# =========================================================
# Backend Services
# =========================================================
book_finder = BookFinder()
data_store = DataStore(str(DB_PATH))
library = Library(data_store)
reading_tracker = ReadingTracker(library)


# =========================================================
# Book Adapter
# =========================================================
def book_to_dict(book):
    """Convert Sprint 2 Book model to frontend format."""
    return {
        "id": book.book_id,
        "title": book.title,
        "author": ", ".join(book.authors) if book.authors else "Unknown Author",
        "category": ", ".join(book.categories) if book.categories else "Uncategorized",
        "year": book.published_year or "Unknown",
        "pages": book.page_count or 0,
        "cover": book.cover_url or "",
        "description": book.description or "No description available.",
    }


# =========================================================
# Search
# =========================================================
def search_books(keyword):
    """Search books using Google Books API."""
    books = book_finder.search("title", keyword)

    unique_books = {}

    for book in books:
        unique_books[book.book_id] = book

    return [
        book_to_dict(book)
        for book in unique_books.values()
    ]

def get_home_books():
    """Get books to display on Home page."""
    books = book_finder.search(
        "genre",
        "fiction",
        max_results=10,
    )

    return [
        book_to_dict(book)
        for book in books
    ]



# =========================================================
# Book Details
# =========================================================
def get_book_details(book_id):
    """Get detailed book information."""
    book = book_finder.get_details(book_id)
    return book_to_dict(book)


# =========================================================
# Library
# =========================================================
def get_library_books():
    """Return books currently in user's library."""
    entries = library.get_entries()

    return [
        {
            **book_to_dict(entry.book),
            "status": str(entry.status),
            "progress": entry.progress_percent or 0,
            "rating": entry.rating or 0,
            "note": entry.notes,
        }
        for entry in entries
    ]


def add_to_library(book_dict):
    """Add a book to the library."""
    book = book_finder.get_details(book_dict["id"])
    library.add_book(book)


def remove_from_library(book_id):
    """Remove a book from the library."""
    library.remove_book(book_id)


# =========================================================
# Reading Tracker
# =========================================================
def update_status(book_id, status):
    """Update reading status."""
    status_map = {
        "Want to Read": ReadingStatus.WANT_TO_READ,
        "Reading": ReadingStatus.READING,
        "Completed": ReadingStatus.COMPLETED,
    }

    reading_tracker.set_status(
        book_id,
        status_map[status],
    )


def update_progress(book_id, pages_read):
    """Update reading progress by pages."""
    reading_tracker.update_progress(
        book_id,
        pages_read,
    )


def update_rating(book_id, rating):
    """Update personal rating."""
    reading_tracker.set_rating(
        book_id,
        rating if rating > 0 else None,
    )


def update_note(book_id, note):
    """Update personal note."""
    reading_tracker.set_notes(
        book_id,
        note,
    )

def browse_books(genre, max_results=20):
    """Browse books by genre using Google Books API."""

    books = book_finder.search(
        "genre",
        genre,
        max_results=max_results
    )

    unique_books = {}

    for book in books:
        unique_books[book.book_id] = book

    return [
        book_to_dict(book)
        for book in unique_books.values()
    ]