"""Tests for src/library.py (Business Logic Layer)."""

import time

import pytest

from src.exceptions import BookNotFoundError, DuplicateBookError
from src.library import Library
from src.models import ReadingStatus


class TestAddRemoveGet:
    def test_add_book_creates_want_to_read_entry(self, library, sample_book):
        entry = library.add_book(sample_book)
        assert entry.status == ReadingStatus.WANT_TO_READ
        assert entry.pages_read == 0
        assert entry.rating is None
        assert entry.added_at  # a timestamp was set

    def test_add_duplicate_book_raises(self, library, sample_book):
        library.add_book(sample_book)
        with pytest.raises(DuplicateBookError):
            library.add_book(sample_book)

    def test_remove_book_removes_it(self, library, sample_book):
        library.add_book(sample_book)
        library.remove_book(sample_book.book_id)
        assert library.get_entries() == []

    def test_remove_nonexistent_book_raises(self, library):
        with pytest.raises(BookNotFoundError):
            library.remove_book("does-not-exist")

    def test_get_entry_raises_when_missing(self, library):
        with pytest.raises(BookNotFoundError):
            library.get_entry("does-not-exist")

    def test_added_book_persists_across_new_library_instance(
        self, data_store, library, sample_book
    ):
        library.add_book(sample_book)

        reloaded_library = Library(data_store)
        assert reloaded_library.get_entry(sample_book.book_id) is not None


class TestSearch:
    def test_search_matches_title_case_insensitive(
        self, library, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", title="Python Crash Course"))
        library.add_book(sample_book_factory("b2", title="Learning Rust"))

        results = library.search("python")
        assert len(results) == 1
        assert results[0].book.book_id == "b1"

    def test_search_matches_author(self, library, sample_book_factory):
        library.add_book(
            sample_book_factory("b1", authors=["Jane Doe"], title="X")
        )
        assert len(library.search("jane")) == 1

    def test_search_matches_category(self, library, sample_book_factory):
        library.add_book(
            sample_book_factory("b1", categories=["Science Fiction"], title="X")
        )
        assert len(library.search("science")) == 1

    def test_search_empty_keyword_returns_empty(
        self, library, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", title="Anything"))
        assert library.search("   ") == []

    def test_search_no_match_returns_empty(self, library, sample_book_factory):
        library.add_book(sample_book_factory("b1", title="Anything"))
        assert library.search("zzz-no-match") == []


class TestFilter:
    def test_filter_by_status(self, library, sample_book_factory):
        entry1 = library.add_book(sample_book_factory("b1"))
        library.add_book(sample_book_factory("b2"))
        entry1.status = ReadingStatus.READING
        library.update_entry(entry1)

        results = library.filter_entries(status=ReadingStatus.READING)
        assert [e.book.book_id for e in results] == ["b1"]

    def test_filter_by_category_case_insensitive(
        self, library, sample_book_factory
    ):
        library.add_book(
            sample_book_factory("b1", categories=["Science Fiction"])
        )
        library.add_book(sample_book_factory("b2", categories=["Romance"]))

        results = library.filter_entries(category="SCIENCE FICTION")
        assert [e.book.book_id for e in results] == ["b1"]

    def test_filter_by_min_rating_excludes_unrated(
        self, library, sample_book_factory
    ):
        entry1 = library.add_book(sample_book_factory("b1"))
        entry1.rating = 5
        library.update_entry(entry1)
        library.add_book(sample_book_factory("b2"))  # never rated

        results = library.filter_entries(min_rating=3)
        assert [e.book.book_id for e in results] == ["b1"]

    def test_filter_combines_all_three_criteria(
        self, library, sample_book_factory
    ):
        entry1 = library.add_book(
            sample_book_factory("b1", categories=["Fiction"])
        )
        entry1.status = ReadingStatus.COMPLETED
        entry1.rating = 4
        library.update_entry(entry1)

        entry2 = library.add_book(
            sample_book_factory("b2", categories=["Fiction"])
        )
        entry2.status = ReadingStatus.COMPLETED
        entry2.rating = 2
        library.update_entry(entry2)

        results = library.filter_entries(
            status=ReadingStatus.COMPLETED, category="Fiction", min_rating=3
        )
        assert [e.book.book_id for e in results] == ["b1"]


class TestSort:
    def test_sort_by_rating_puts_unrated_last(
        self, library, sample_book_factory
    ):
        e1 = library.add_book(sample_book_factory("b1"))
        e2 = library.add_book(sample_book_factory("b2"))
        e3 = library.add_book(sample_book_factory("b3"))
        e1.rating, e2.rating, e3.rating = 3, None, 5
        for entry in (e1, e2, e3):
            library.update_entry(entry)

        sorted_entries = library.sort_entries(
            library.get_entries(), key="rating", reverse=True
        )
        assert [e.book.book_id for e in sorted_entries] == ["b3", "b1", "b2"]

    def test_sort_by_title_ascending(self, library, sample_book_factory):
        library.add_book(sample_book_factory("b1", title="Zebra"))
        library.add_book(sample_book_factory("b2", title="Apple"))

        sorted_entries = library.sort_entries(library.get_entries(), key="title")
        assert [e.book.title for e in sorted_entries] == ["Apple", "Zebra"]

    def test_sort_by_published_year_missing_last(
        self, library, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", published_date="2010"))
        library.add_book(sample_book_factory("b2", published_date=None))
        library.add_book(sample_book_factory("b3", published_date="2000"))

        sorted_entries = library.sort_entries(
            library.get_entries(), key="published_year"
        )
        assert [e.book.book_id for e in sorted_entries] == ["b3", "b1", "b2"]

    def test_sort_does_not_mutate_input_list(self, library, sample_book_factory):
        library.add_book(sample_book_factory("b1", title="B"))
        library.add_book(sample_book_factory("b2", title="A"))

        original = library.get_entries()
        original_order = [e.book.book_id for e in original]
        library.sort_entries(original, key="title")

        assert [e.book.book_id for e in original] == original_order

    def test_sort_unknown_key_raises(self, library):
        with pytest.raises(ValueError):
            library.sort_entries(library.get_entries(), key="not_a_real_key")


class TestSortPerformance:
    def test_sort_1000_entries_under_50ms(self, library, seed_books):
        """Mirrors TC-03 from the Sprint 2-3 test plan: sorting 1,000
        entries by published_year must finish in under 50ms.

        seed_books.json currently has 300 books (BOOK_COUNT in
        generate_seed_data.py) — bump it to 1000 to match the rubric
        exactly. Until then, this test cycles through the available
        books to still build a library of 1,000 entries, so it keeps
        exercising the target scale.
        """
        entries = []
        for i in range(1000):
            template = seed_books[i % len(seed_books)]
            book = type(template)(
                book_id=f"perf-{i:04d}",
                title=template.title,
                authors=template.authors,
                description=template.description,
                published_date=template.published_date,
                categories=template.categories,
                cover_url=template.cover_url,
                page_count=template.page_count,
            )
            entries.append(library.add_book(book))

        start = time.perf_counter()
        library.sort_entries(entries, key="published_year")
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 50, (
            f"sort_entries took {elapsed_ms:.2f}ms for 1000 entries "
            f"(limit: 50ms, per TC-03)"
        )