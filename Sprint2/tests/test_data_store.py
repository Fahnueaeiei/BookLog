"""Tests for src/data_store.py (Data Access Layer).

Every test gets its own throwaway SQLite file via the data_store /
db_path fixtures in conftest.py, so tests never interfere with each
other or with a real database.
"""

from src.data_store import DataStore
from src.models import LibraryEntry, ReadingStatus


class TestSaveAndLoadEntries:
    def test_save_and_load_entry_round_trip(self, data_store, sample_book):
        entry = LibraryEntry(
            book=sample_book,
            status=ReadingStatus.READING,
            pages_read=50,
            rating=4,
            notes="Great so far.",
            added_at="2026-01-01T00:00:00+00:00",
        )

        data_store.save_entry(entry)
        loaded = data_store.load_entries()

        assert len(loaded) == 1
        loaded_entry = loaded[0]
        assert loaded_entry.book.book_id == sample_book.book_id
        assert loaded_entry.book.title == sample_book.title
        assert loaded_entry.book.authors == sample_book.authors
        assert loaded_entry.status == ReadingStatus.READING
        assert loaded_entry.pages_read == 50
        assert loaded_entry.rating == 4
        assert loaded_entry.notes == "Great so far."

    def test_load_entries_empty_when_nothing_saved(self, data_store):
        assert data_store.load_entries() == []

    def test_save_entry_upserts_on_same_book_id(self, data_store, sample_book):
        entry = LibraryEntry(
            book=sample_book,
            status=ReadingStatus.WANT_TO_READ,
            added_at="2026-01-01T00:00:00+00:00",
        )
        data_store.save_entry(entry)

        entry.status = ReadingStatus.COMPLETED
        entry.rating = 5
        data_store.save_entry(entry)

        loaded = data_store.load_entries()
        assert len(loaded) == 1
        assert loaded[0].status == ReadingStatus.COMPLETED
        assert loaded[0].rating == 5

    def test_authors_and_categories_round_trip_as_lists(
        self, data_store, sample_book_factory
    ):
        book = sample_book_factory(
            "multi-001",
            authors=["Author One", "Author Two"],
            categories=["Fiction", "Adventure"],
        )
        entry = LibraryEntry(
            book=book, status=ReadingStatus.WANT_TO_READ, added_at="now"
        )
        data_store.save_entry(entry)

        loaded = data_store.load_entries()[0]
        assert loaded.book.authors == ["Author One", "Author Two"]
        assert loaded.book.categories == ["Fiction", "Adventure"]

    def test_missing_optional_fields_round_trip_as_none(
        self, data_store, sample_book_factory
    ):
        book = sample_book_factory(
            "sparse-001",
            description=None,
            cover_url=None,
            page_count=None,
            authors=[],
            categories=[],
        )
        entry = LibraryEntry(
            book=book, status=ReadingStatus.WANT_TO_READ, added_at="now"
        )
        data_store.save_entry(entry)

        loaded = data_store.load_entries()[0]
        assert loaded.book.description is None
        assert loaded.book.cover_url is None
        assert loaded.book.page_count is None
        assert loaded.book.authors == []
        assert loaded.book.categories == []


class TestDeleteEntry:
    def test_delete_entry_removes_entry_but_keeps_book(
        self, data_store, sample_book
    ):
        entry = LibraryEntry(
            book=sample_book,
            status=ReadingStatus.WANT_TO_READ,
            added_at="2026-01-01T00:00:00+00:00",
        )
        data_store.save_entry(entry)

        deleted = data_store.delete_entry(sample_book.book_id)
        assert deleted is True
        assert data_store.load_entries() == []

        # The book row itself should still be there, so re-adding the
        # same book_id later does not lose its details.
        with data_store._connect() as connection:
            row = connection.execute(
                "SELECT * FROM books WHERE book_id = ?;",
                (sample_book.book_id,),
            ).fetchone()
        assert row is not None
        assert row["title"] == sample_book.title

    def test_delete_entry_returns_false_when_not_found(self, data_store):
        assert data_store.delete_entry("does-not-exist") is False


class TestCorruptedDatabase:
    def test_corrupted_database_is_backed_up_and_replaced(self, tmp_path):
        db_path = tmp_path / "corrupted.db"
        db_path.write_bytes(b"not a real sqlite file")

        store = DataStore(str(db_path))

        # A fresh, working database should now be usable...
        assert store.load_entries() == []

        # ...and the original bad file should be preserved as a backup
        # rather than silently discarded.
        backups = list(tmp_path.glob("corrupted.db.corrupted.*"))
        assert len(backups) == 1
        assert backups[0].read_bytes() == b"not a real sqlite file"

    def test_missing_database_file_is_created_automatically(self, tmp_path):
        db_path = tmp_path / "does_not_exist_yet.db"
        assert not db_path.exists()

        DataStore(str(db_path))

        assert db_path.exists()