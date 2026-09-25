"""Tests for src/reading_tracker.py (Business Logic Layer)."""

import pytest

from src.exceptions import (
    BookNotFoundError,
    InvalidProgressError,
    InvalidRatingError,
)
from src.models import ReadingStatus
from src.reading_tracker import ReadingTracker


@pytest.fixture
def tracker(library):
    return ReadingTracker(library)


class TestSetStatus:
    def test_completed_sets_pages_read_to_full_count(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=300))
        entry = tracker.set_status("b1", ReadingStatus.COMPLETED)
        assert entry.pages_read == 300

    def test_completed_with_unknown_page_count_leaves_pages_read(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=None))
        entry = tracker.set_status("b1", ReadingStatus.COMPLETED)
        assert entry.pages_read == 0

    def test_set_status_missing_book_raises(self, tracker):
        with pytest.raises(BookNotFoundError):
            tracker.set_status("missing", ReadingStatus.READING)

    def test_status_change_is_persisted(self, library, tracker, sample_book_factory):
        library.add_book(sample_book_factory("b1"))
        tracker.set_status("b1", ReadingStatus.READING)
        assert library.get_entry("b1").status == ReadingStatus.READING


class TestUpdateProgress:
    def test_valid_progress_is_saved(self, library, tracker, sample_book_factory):
        library.add_book(sample_book_factory("b1", page_count=300))
        entry = tracker.update_progress("b1", 150)
        assert entry.pages_read == 150

    def test_negative_progress_raises(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=300))
        with pytest.raises(InvalidProgressError):
            tracker.update_progress("b1", -1)

    def test_progress_beyond_page_count_raises(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=300))
        with pytest.raises(InvalidProgressError):
            tracker.update_progress("b1", 301)

    def test_progress_at_exact_page_count_is_allowed(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=300))
        entry = tracker.update_progress("b1", 300)
        assert entry.pages_read == 300

    def test_progress_allowed_when_page_count_unknown(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1", page_count=None))
        entry = tracker.update_progress("b1", 99999)
        assert entry.pages_read == 99999

    def test_update_progress_missing_book_raises(self, tracker):
        with pytest.raises(BookNotFoundError):
            tracker.update_progress("missing", 10)


class TestSetRating:
    @pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
    def test_valid_ratings_accepted(
        self, library, tracker, sample_book_factory, rating
    ):
        library.add_book(sample_book_factory("b1"))
        entry = tracker.set_rating("b1", rating)
        assert entry.rating == rating

    def test_rating_none_clears_it(self, library, tracker, sample_book_factory):
        library.add_book(sample_book_factory("b1"))
        tracker.set_rating("b1", 5)
        entry = tracker.set_rating("b1", None)
        assert entry.rating is None

    @pytest.mark.parametrize("rating", [0, 6, -1, 100])
    def test_out_of_range_rating_raises(
        self, library, tracker, sample_book_factory, rating
    ):
        library.add_book(sample_book_factory("b1"))
        with pytest.raises(InvalidRatingError):
            tracker.set_rating("b1", rating)

    def test_non_integer_rating_raises(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1"))
        with pytest.raises(InvalidRatingError):
            tracker.set_rating("b1", 4.5)

    def test_boolean_rating_raises(self, library, tracker, sample_book_factory):
        """bool is technically an int subclass in Python — True/False
        must be rejected rather than silently treated as 1/0.
        """
        library.add_book(sample_book_factory("b1"))
        with pytest.raises(InvalidRatingError):
            tracker.set_rating("b1", True)


class TestSetNotes:
    def test_notes_are_saved(self, library, tracker, sample_book_factory):
        library.add_book(sample_book_factory("b1"))
        entry = tracker.set_notes("b1", "Really enjoyed this one.")
        assert entry.notes == "Really enjoyed this one."

    def test_none_notes_become_empty_string(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1"))
        entry = tracker.set_notes("b1", None)
        assert entry.notes == ""

    def test_empty_string_notes_are_kept_as_is(
        self, library, tracker, sample_book_factory
    ):
        library.add_book(sample_book_factory("b1"))
        tracker.set_notes("b1", "Some notes")
        entry = tracker.set_notes("b1", "")
        assert entry.notes == ""