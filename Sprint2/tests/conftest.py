"""Shared pytest fixtures for BookLog Sprint 2 tests.

Run from the Sprint2 project root with:

    python -m pytest

so `src` resolves as a package without any extra sys.path setup.
"""

import json
from pathlib import Path

import pytest

from src.data_store import DataStore
from src.library import Library
from src.models import Book

SEED_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "seed_books.json"


@pytest.fixture
def db_path(tmp_path):
    """Path to a fresh, temporary SQLite file for one test."""
    return str(tmp_path / "test_booklog.db")


@pytest.fixture
def data_store(db_path):
    """A DataStore backed by a temporary database file.

    A new temp file is created per test (via tmp_path), so tests never
    see each other's data and never touch the real database.
    """
    return DataStore(db_path)


@pytest.fixture
def library(data_store):
    """A Library backed by the temporary DataStore."""
    return Library(data_store)


@pytest.fixture
def sample_book():
    """One Book with every field filled in, for straightforward tests."""
    return Book(
        book_id="test-001",
        title="The Pragmatic Programmer",
        authors=["David Thomas", "Andrew Hunt"],
        description="A classic book about software craftsmanship.",
        published_date="1999-10-20",
        categories=["Programming", "Non-Fiction"],
        cover_url="https://example.com/covers/test-001.jpg",
        page_count=352,
    )


@pytest.fixture
def sample_book_factory():
    """Factory for building distinct Book objects on demand.

    Usage: sample_book_factory("b1", title="Something", page_count=200)
    Any Book field can be overridden; unset fields get sane defaults.
    """

    def _make(book_id, **overrides):
        defaults = dict(
            title=f"Book {book_id}",
            authors=["Some Author"],
            description="A book.",
            published_date="2020",
            categories=["Fiction"],
            cover_url=None,
            page_count=200,
        )
        defaults.update(overrides)
        return Book(book_id=book_id, **defaults)

    return _make


def _load_seed_books():
    """Load data/seed_books.json as a list of Book objects.

    Returns an empty list if the seed file has not been generated yet
    (generate_seed_data.py has not been run). Tests that need seed
    data should skip in that case, not fail the whole suite.
    """
    if not SEED_DATA_PATH.exists():
        return []

    with open(SEED_DATA_PATH, encoding="utf-8") as file:
        raw_books = json.load(file)

    return [
        Book(
            book_id=raw["book_id"],
            title=raw["title"],
            authors=raw["authors"],
            description=raw["description"],
            published_date=raw["published_date"],
            categories=raw["categories"],
            cover_url=raw["cover_url"],
            page_count=raw["page_count"],
        )
        for raw in raw_books
    ]


@pytest.fixture
def seed_books():
    """The generated seed_books.json, as Book objects.

    Skips the test (rather than failing) if the seed file has not
    been generated yet, since it is produced by a separate script.
    """
    books = _load_seed_books()
    if not books:
        pytest.skip(
            "data/seed_books.json not found — run "
            "python data/generate_seed_data.py first."
        )
    return books