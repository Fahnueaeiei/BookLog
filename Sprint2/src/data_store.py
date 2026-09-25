"""SQLite persistence (Data Access Layer) for BookLog (Sprint 2).

DataStore is the only place in the application that talks to SQLite.
All SQL lives here. Business logic (Library, ReadingTracker) calls
DataStore's methods and never writes SQL of its own.

Schema (see PLAN.md, section 6):
    books(book_id, title, authors, description, published_date,
          categories, cover_url, page_count)
    library_entries(book_id, status, pages_read, rating, notes, added_at)
"""

import os
import shutil
import sqlite3
from datetime import datetime, timezone

from src.exceptions import DatabaseError
from src.models import Book, LibraryEntry, ReadingStatus

_CREATE_BOOKS_TABLE = """
CREATE TABLE IF NOT EXISTS books (
    book_id        TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    authors        TEXT,
    description    TEXT,
    published_date TEXT,
    categories     TEXT,
    cover_url      TEXT,
    page_count     INTEGER
);
"""

_CREATE_LIBRARY_ENTRIES_TABLE = """
CREATE TABLE IF NOT EXISTS library_entries (
    book_id    TEXT PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE,
    status     TEXT NOT NULL CHECK (
        status IN ('want_to_read', 'reading', 'completed')
    ),
    pages_read INTEGER NOT NULL DEFAULT 0 CHECK (pages_read >= 0),
    rating     INTEGER CHECK (rating BETWEEN 1 AND 5),
    notes      TEXT,
    added_at   TEXT NOT NULL
);
"""


def _join(values):
    """Join a list of strings for storage, e.g. authors or categories."""
    return ",".join(values) if values else ""


def _split(text):
    """Reverse of _join: turn stored text back into a list of strings."""
    return [part for part in text.split(",") if part] if text else []


class DataStore:
    """Saves, loads, and deletes books and library entries in SQLite.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path):
        """Create the DataStore and make sure the database is ready.

        Args:
            db_path: Path to the SQLite database file. Created
                automatically if it does not exist yet. If it exists
                but is corrupted, it is backed up and replaced with a
                fresh, empty database.
        """
        self.db_path = db_path
        self.init_db()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def init_db(self):
        """Create the database file and tables if they don't exist.

        If a database file already exists at db_path but is corrupted
        (not a valid SQLite file, or fails an integrity check), it is
        renamed to a timestamped ``.corrupted`` backup and a fresh
        database is created in its place.
        """
        if os.path.exists(self.db_path) and not self._is_valid_database():
            self._backup_corrupted_database()

        with self._connect() as connection:
            connection.execute(_CREATE_BOOKS_TABLE)
            connection.execute(_CREATE_LIBRARY_ENTRIES_TABLE)

    def _is_valid_database(self):
        """Return True if db_path is a readable, non-corrupted database."""
        try:
            with sqlite3.connect(self.db_path) as connection:
                result = connection.execute("PRAGMA integrity_check;")
                return result.fetchone()[0] == "ok"
        except sqlite3.DatabaseError:
            return False

    def _backup_corrupted_database(self):
        """Rename a corrupted database file out of the way."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        backup_path = f"{self.db_path}.corrupted.{timestamp}"
        try:
            shutil.move(self.db_path, backup_path)
        except OSError as error:
            raise DatabaseError(
                f"Could not back up the corrupted database file "
                f"'{self.db_path}'.",
                cause=error,
            ) from error

    def _connect(self):
        """Open a connection with foreign keys enabled and row access."""
        connection = sqlite3.connect(self.db_path)
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.row_factory = sqlite3.Row
        return connection

    # ------------------------------------------------------------------
    # Books
    # ------------------------------------------------------------------
    def save_book(self, book):
        """Insert a book, or replace it if book_id already exists."""
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO books (
                        book_id, title, authors, description,
                        published_date, categories, cover_url, page_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(book_id) DO UPDATE SET
                        title=excluded.title,
                        authors=excluded.authors,
                        description=excluded.description,
                        published_date=excluded.published_date,
                        categories=excluded.categories,
                        cover_url=excluded.cover_url,
                        page_count=excluded.page_count;
                    """,
                    (
                        book.book_id,
                        book.title,
                        _join(book.authors),
                        book.description,
                        book.published_date,
                        _join(book.categories),
                        book.cover_url,
                        book.page_count,
                    ),
                )
        except sqlite3.Error as error:
            raise DatabaseError(
                f"Could not save book '{book.book_id}'.", cause=error
            ) from error

    # ------------------------------------------------------------------
    # Library entries
    # ------------------------------------------------------------------
    def save_entry(self, entry):
        """Save a library entry, and the book it refers to.

        The book is saved first (insert-or-replace) so the foreign key
        in library_entries is always satisfied, and so book details
        picked up from a fresh API call stay up to date.
        """
        self.save_book(entry.book)

        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO library_entries (
                        book_id, status, pages_read, rating, notes, added_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(book_id) DO UPDATE SET
                        status=excluded.status,
                        pages_read=excluded.pages_read,
                        rating=excluded.rating,
                        notes=excluded.notes,
                        added_at=excluded.added_at;
                    """,
                    (
                        entry.book.book_id,
                        entry.status.value,
                        entry.pages_read,
                        entry.rating,
                        entry.notes,
                        entry.added_at,
                    ),
                )
        except sqlite3.Error as error:
            raise DatabaseError(
                f"Could not save library entry '{entry.book.book_id}'.",
                cause=error,
            ) from error

    def delete_entry(self, book_id):
        """Delete a library entry. Return True if a row was deleted.

        The underlying book row in `books` is left in place, so the
        book's details are still available (e.g. if it is re-added
        later). Only the library_entries row is removed.
        """
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "DELETE FROM library_entries WHERE book_id = ?;",
                    (book_id,),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as error:
            raise DatabaseError(
                f"Could not delete library entry '{book_id}'.", cause=error
            ) from error

    def load_entries(self):
        """Load every library entry, joined with its book details.

        Returns:
            A list of LibraryEntry objects. Empty if the library has
            no entries yet.
        """
        query = """
            SELECT b.book_id, b.title, b.authors, b.description,
                   b.published_date, b.categories, b.cover_url,
                   b.page_count,
                   e.status, e.pages_read, e.rating, e.notes, e.added_at
            FROM library_entries e
            JOIN books b ON b.book_id = e.book_id;
        """
        try:
            with self._connect() as connection:
                rows = connection.execute(query).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError(
                "Could not load library entries.", cause=error
            ) from error

        return [self._row_to_entry(row) for row in rows]

    @staticmethod
    def _row_to_entry(row):
        """Turn one joined SQL row into a LibraryEntry with its Book."""
        book = Book(
            book_id=row["book_id"],
            title=row["title"],
            authors=_split(row["authors"]),
            description=row["description"],
            published_date=row["published_date"],
            categories=_split(row["categories"]),
            cover_url=row["cover_url"],
            page_count=row["page_count"],
        )
        return LibraryEntry(
            book=book,
            status=ReadingStatus(row["status"]),
            pages_read=row["pages_read"],
            rating=row["rating"],
            notes=row["notes"] or "",
            added_at=row["added_at"],
        )