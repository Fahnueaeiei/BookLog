"""
BookLog Sprint 3 - full test suite (no network, no API quota).

Covers what the course doc asks for in Sprint 3:
  * UI <-> SQL consistency (what the UI reads == what is stored)
  * Data persistence + two sessions seeing the same data
  * Edge cases: missing/corrupt/read-only DB, negative/extreme/wrong-type
    values, unknown ids, duplicates, empty search
  * Exception handling: custom exceptions instead of raw Python errors
  * Scale: many books in the library

Uses a temporary DB per test (your real booklog.db is never touched).
Requires the updated service.py (validated update_status / update_rating).

Put in:  Sprint3/frontend/test/test_sprint3_full.py
Run:     cd Sprint3/frontend && python3 -m pytest test/test_sprint3_full.py -v
"""
import inspect
import os
import sqlite3
import sys
import time
from pathlib import Path

import pytest

FRONTEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FRONTEND_DIR / "src"))

import service  # noqa: E402  (also puts Sprint2 on sys.path)
from src.exceptions import (  # noqa: E402
    BookNotFoundError,
    DatabaseError,
    DuplicateBookError,
    InvalidProgressError,
    InvalidRatingError,
)

BID = "TEST_BOOK_001"
PAGES = 200

# library_entries columns: book_id, status, current_page, rating, notes, added_at
COL_STATUS, COL_PAGES, COL_RATING, COL_NOTES = 1, 2, 3, 4


# ---------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------
def make_book(pages=PAGES, book_id=BID):
    cand = {
        "book_id": book_id, "title": f"Book {book_id}", "authors": ["Author"],
        "categories": ["Testing"], "published_year": 2020,
        "published_date": "2020", "page_count": pages, "cover_url": "",
        "description": "A book for tests.",
    }
    ok = inspect.signature(service.Book).parameters
    return service.Book(**{k: v for k, v in cand.items() if k in ok})


class StubFinder:
    """Fake Google Books: returns a Book for any id, never uses the network."""

    def __init__(self, pages=PAGES):
        self.pages = pages

    def get_details(self, book_id):
        return make_book(self.pages, book_id)


def install(db_path, monkeypatch):
    store = service.DataStore(str(db_path))
    lib = service.Library(store)
    monkeypatch.setattr(service, "data_store", store)
    monkeypatch.setattr(service, "library", lib)
    monkeypatch.setattr(service, "reading_tracker", service.ReadingTracker(lib))
    monkeypatch.setattr(service, "book_finder", StubFinder())
    monkeypatch.setattr(service, "DB_PATH", Path(db_path))
    if hasattr(service, "_get_book"):
        service._get_book.cache_clear()


@pytest.fixture
def env(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    install(db_path, monkeypatch)
    return db_path


def add_book(book_id=BID):
    service.add_to_library({"id": book_id})


def db_row(db_path, book_id=BID):
    con = sqlite3.connect(str(db_path))
    try:
        return con.execute(
            "select * from library_entries where book_id=?", (book_id,)
        ).fetchone()
    finally:
        con.close()


def ui_row(book_id=BID):
    return next(
        (b for b in service.get_library_books() if b["id"] == book_id), None
    )


def norm(status):
    return str(status).split(".")[-1].replace("_", "").replace(" ", "").lower()


def is_custom(exc):
    return type(exc).__module__.split(".")[-1] == "exceptions"


# =========================================================
# 1. CRUD + UI <-> SQL consistency
# =========================================================
def test_add_creates_row_in_db_and_ui(env):
    add_book()
    assert db_row(env) is not None
    assert ui_row()["title"] == f"Book {BID}"


@pytest.mark.parametrize("label", ["Want to Read", "Reading", "Completed"])
def test_status_matches_ui_and_db(env, label):
    add_book()
    service.update_status(BID, label)
    assert ui_row()["status"] == label
    assert norm(db_row(env)[COL_STATUS]) == norm(label)


def test_progress_db_pages_vs_ui_percent(env):
    add_book()
    service.update_status(BID, "Reading")
    service.update_progress(BID, PAGES // 2)
    assert db_row(env)[COL_PAGES] == PAGES // 2          # DB stores pages
    assert ui_row()["progress"] == 50                    # UI shows percent


def test_completed_is_100_percent(env):
    add_book()
    service.update_status(BID, "Completed")
    assert ui_row()["progress"] == 100
    assert db_row(env)[COL_PAGES] == PAGES


def test_rating_set_and_clear(env):
    add_book()
    service.update_rating(BID, 4)
    assert ui_row()["rating"] == db_row(env)[COL_RATING] == 4
    service.update_rating(BID, 0)
    assert ui_row()["rating"] == 0
    assert db_row(env)[COL_RATING] in (None, 0)


def test_note_roundtrip(env):
    add_book()
    service.update_note(BID, "hello")
    assert ui_row()["note"] == db_row(env)[COL_NOTES] == "hello"


def test_remove_deletes_from_db_and_ui(env):
    add_book()
    service.remove_from_library(BID)
    assert db_row(env) is None and ui_row() is None


# =========================================================
# 2. Persistence and two sessions
# =========================================================
def test_data_survives_restart(env):
    add_book()
    service.update_status(BID, "Reading")
    service.update_rating(BID, 5)
    service.update_note(BID, "persisted")

    lib2 = service.Library(service.DataStore(str(env)))
    entry = next(e for e in lib2.get_entries() if e.book.book_id == BID)
    assert entry.rating == 5
    assert entry.notes == "persisted"
    assert norm(entry.status) == "reading"


def test_two_sessions_see_the_same_data(env):
    """Like two browser sessions/processes on the same DB file."""
    add_book()
    other_lib = service.Library(service.DataStore(str(env)))
    other_tracker = service.ReadingTracker(other_lib)

    service.update_rating(BID, 4)                       # session A writes
    seen_by_b = next(e for e in other_lib.get_entries() if e.book.book_id == BID)
    assert seen_by_b.rating == 4, "session B has stale data (RAM != file)"

    other_tracker.set_rating(BID, 2)                    # session B writes
    assert ui_row()["rating"] == 2, "session A has stale data (RAM != file)"


# =========================================================
# 3. Edge cases: values (progress / rating / note / status)
# =========================================================
@pytest.mark.parametrize("pages_read", [-1, 201, 10**9, "abc", None, 100.5])
def test_invalid_progress_rejected(env, pages_read):
    add_book()
    with pytest.raises(InvalidProgressError):
        service.update_progress(BID, pages_read)
    assert ui_row()["progress"] == 0            # nothing was stored


def test_progress_on_book_without_page_count(env):
    service.book_finder.pages = 0
    service.add_to_library({"id": "NO_PAGES"})
    with pytest.raises(InvalidProgressError):
        service.update_progress("NO_PAGES", 10)
    assert ui_row("NO_PAGES")["progress"] == 0


@pytest.mark.parametrize("pages_read, percent", [(0, 0), (100, 50), (200, 100)])
def test_progress_boundaries(env, pages_read, percent):
    add_book()
    service.update_status(BID, "Reading")
    service.update_progress(BID, pages_read)
    assert ui_row()["progress"] == percent


@pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
def test_valid_ratings(env, rating):
    add_book()
    service.update_rating(BID, rating)
    assert ui_row()["rating"] == rating


@pytest.mark.parametrize("rating", [-1, 6, 4.5, "3", None])
def test_invalid_rating_rejected(env, rating):
    add_book()
    with pytest.raises((InvalidRatingError, ValueError)):
        service.update_rating(BID, rating)
    assert ui_row()["rating"] == 0


@pytest.mark.parametrize(
    "note",
    ["", "x" * 5000, "สวัสดี 📚", "<script>alert(1)</script>", "line1\nline2"],
)
def test_notes_roundtrip_exactly(env, note):
    add_book()
    service.update_note(BID, note)
    stored = ui_row()["note"]
    assert (stored or "") == note


@pytest.mark.parametrize("status", ["Bogus", None, "reading", "", 3])
def test_invalid_status_rejected(env, status):
    add_book()
    with pytest.raises(ValueError):
        service.update_status(BID, status)
    assert ui_row()["status"] == "Want to Read"      # unchanged default


# =========================================================
# 4. Edge cases: library operations
# =========================================================
def test_adding_same_book_twice_rejected(env):
    add_book()
    with pytest.raises(DuplicateBookError):
        add_book()
    assert len(service.get_library_books()) == 1


def test_remove_missing_book(env):
    with pytest.raises(BookNotFoundError):
        service.remove_from_library("NOT_THERE")


@pytest.mark.parametrize(
    "action",
    [
        lambda: service.update_status("NOT_THERE", "Reading"),
        lambda: service.update_progress("NOT_THERE", 5),
        lambda: service.update_rating("NOT_THERE", 3),
        lambda: service.update_note("NOT_THERE", "x"),
    ],
    ids=["status", "progress", "rating", "note"],
)
def test_update_unknown_book(env, action):
    with pytest.raises(BookNotFoundError):
        action()


def test_empty_library(env):
    assert service.get_library_books() == []


# =========================================================
# 5. Edge cases: search input (validated before any network call)
# =========================================================
@pytest.mark.parametrize("keyword", ["", "   ", None, 123])
def test_invalid_search_rejected(keyword):
    with pytest.raises(ValueError):
        service.search_books(keyword)


# =========================================================
# 6. Edge cases: database file problems
# =========================================================
def _flow(path, monkeypatch):
    install(path, monkeypatch)
    add_book()
    service.update_status(BID, "Reading")
    return service.get_library_books()


def test_db_file_missing_is_created(tmp_path, monkeypatch):
    books = _flow(tmp_path / "new.db", monkeypatch)
    assert len(books) == 1


def test_db_file_empty_is_usable(tmp_path, monkeypatch):
    path = tmp_path / "empty.db"
    path.write_bytes(b"")
    assert len(_flow(path, monkeypatch)) == 1


@pytest.mark.xfail(
    reason="DataStore does not create missing parent folders "
           "(service.py does it for the default path)",
    strict=False,
)
def test_db_folder_missing_is_created(tmp_path, monkeypatch):
    assert len(_flow(tmp_path / "nodir" / "t.db", monkeypatch)) == 1


def test_corrupt_db_file_is_handled_not_raw(tmp_path, monkeypatch):
    path = tmp_path / "corrupt.db"
    path.write_bytes(b"not a database" * 200)
    try:
        books = _flow(path, monkeypatch)
    except Exception as e:  # noqa: BLE001
        assert is_custom(e), f"raw error leaked to UI: {type(e).__name__}: {e}"
    else:
        assert len(books) == 1


def test_read_only_db_raises_database_error(tmp_path, monkeypatch):
    path = tmp_path / "ro.db"
    install(path, monkeypatch)
    add_book()
    os.chmod(path, 0o444)
    try:
        with pytest.raises(DatabaseError):
            service.update_note(BID, "x")
    finally:
        os.chmod(path, 0o644)


def test_table_dropped_is_handled_not_raw(env):
    add_book()
    con = sqlite3.connect(str(env))
    con.execute("drop table library_entries")
    con.commit()
    con.close()
    try:
        service.get_library_books()
    except Exception as e:  # noqa: BLE001
        assert is_custom(e), f"raw error leaked to UI: {type(e).__name__}: {e}"


def test_db_deleted_while_running_is_handled_not_raw(env):
    add_book()
    os.remove(env)
    try:
        service.get_library_books()
    except Exception as e:  # noqa: BLE001
        assert is_custom(e), f"raw error leaked to UI: {type(e).__name__}: {e}"


# =========================================================
# 7. Scale
# =========================================================
def test_many_books(env):
    n = 200
    for i in range(n):
        service.add_to_library({"id": f"BULK_{i:04d}"})
    start = time.perf_counter()
    books = service.get_library_books()
    elapsed = time.perf_counter() - start

    assert len(books) == n
    assert len({b["id"] for b in books}) == n
    assert elapsed < 1.0, f"reading {n} books took {elapsed:.2f}s"


def test_status_filter_counts_add_up(env):
    labels = ["Want to Read", "Reading", "Completed"]
    for i in range(9):
        bid = f"F_{i}"
        service.add_to_library({"id": bid})
        service.update_status(bid, labels[i % 3])

    books = service.get_library_books()
    counts = {lbl: sum(b["status"] == lbl for b in books) for lbl in labels}
    assert counts == {lbl: 3 for lbl in labels}
    assert sum(counts.values()) == len(books)