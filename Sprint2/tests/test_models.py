"""Tests for the plain data models in src/models.py."""

import pytest

from src.models import Book, LibraryEntry, ReadingStatus


class TestBookPublishedYear:
    @pytest.mark.parametrize(
        "published_date, expected_year",
        [
            ("1999", 1999),
            ("1999-10", 1999),
            ("1999-10-20", 1999),
            (None, None),
            ("", None),
        ],
    )
    def test_published_year_formats(self, published_date, expected_year):
        book = Book(book_id="b1", title="T", published_date=published_date)
        assert book.published_year == expected_year

    def test_published_year_unparseable_string_returns_none(self):
        book = Book(book_id="b1", title="T", published_date="unknown")
        assert book.published_year is None


class TestBookEquality:
    """Book equality is book_id-only (every other field is compare=False)."""

    def test_equal_by_book_id_only(self):
        a = Book(book_id="same", title="Title A")
        b = Book(book_id="same", title="Title B")
        assert a == b

    def test_not_equal_different_book_id(self):
        a = Book(book_id="a", title="Same Title")
        b = Book(book_id="b", title="Same Title")
        assert a != b


class TestReadingStatusLabels:
    def test_str_returns_human_readable_label(self):
        assert str(ReadingStatus.WANT_TO_READ) == "Want to Read"
        assert str(ReadingStatus.READING) == "Reading"
        assert str(ReadingStatus.COMPLETED) == "Completed"

    def test_value_is_the_snake_case_string(self):
        assert ReadingStatus.WANT_TO_READ.value == "want_to_read"
        assert ReadingStatus("reading") == ReadingStatus.READING


class TestLibraryEntryProgress:
    def test_progress_percent_normal(self, sample_book):
        entry = LibraryEntry(
            book=sample_book, status=ReadingStatus.READING, pages_read=176
        )
        assert entry.progress_percent == 50

    def test_progress_percent_no_page_count(self):
        book = Book(book_id="b1", title="T", page_count=None)
        entry = LibraryEntry(
            book=book, status=ReadingStatus.READING, pages_read=10
        )
        assert entry.progress_percent is None

    def test_progress_percent_zero_pages_read(self, sample_book):
        entry = LibraryEntry(
            book=sample_book, status=ReadingStatus.WANT_TO_READ, pages_read=0
        )
        assert entry.progress_percent == 0

    def test_progress_percent_rounds_to_nearest_int(self):
        book = Book(book_id="b1", title="T", page_count=3)
        entry = LibraryEntry(book=book, status=ReadingStatus.READING, pages_read=1)
        assert entry.progress_percent == 33