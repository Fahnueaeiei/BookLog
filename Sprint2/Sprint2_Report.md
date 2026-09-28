# Sprint 2 Report - Back-End Development

| Item | Detail |
|---|---|
| Project | BookLog |
| Course | CP352301 Script Programming - Semester 1/2569 |
| Sprint | Sprint 2 - Back-End Development |
| Team | Phattharawadee Songsrirod, Sujeephon Poobanchuen |
| Roles | Both members: Coder and Debugger |
| Repository | https://github.com/Fahnueaeiei/BookLog |
| Pull Request | Pending - `sprint-2` will be opened against `main` after documentation review |

---

## 1. Sprint Goal

Build the BookLog business logic and data access layers independently
from the user interface. The result persists a personal library,
supports Google Books lookups, and implements local search, filter,
and sort algorithms for reuse by the Sprint 3 Streamlit application.

## 2. Sprint Progress Summary

- [x] Created domain models, custom exceptions, and the business-logic
  services.
- [x] Implemented SQLite persistence with automatic database creation
  and corrupted-file recovery.
- [x] Implemented Google Books search and details lookup with API error
  handling and safe defaults for missing fields.
- [x] Implemented local search, filter, and sort algorithms.
- [x] Implemented reading status, progress, rating, and notes rules.
- [x] Added seed data and measured algorithm performance with 1,000
  library entries.
- [x] Added automated pytest coverage for core logic and `DataStore`.
- [x] Ran `ruff` with no findings.
- [x] Wrote this report and `CHANGELOG.md` version 0.2.0.
- [ ] Open the Sprint 2 Pull Request after committing the documentation.

## 3. Work Completed

### Domain models and business logic

- Added `Book`, `LibraryEntry`, and `ReadingStatus` domain models.
- Added custom exceptions for missing books, duplicate books, invalid
  ratings, invalid reading progress, API failures, and database errors.
- Implemented `Library` to add, remove, load, search, filter, and sort
  personal-library entries.
- Implemented `ReadingTracker` to update status, pages read, rating,
  and notes. Marking a book as Completed sets pages read to its full
  page count when known.

### Data access and persistence

- Implemented `DataStore` using SQLite.
- The database and tables are created automatically when absent.
- Books and entries are saved, loaded, updated, and deleted through
  the data-access layer only.
- A corrupted database is kept as a timestamped `.corrupted` backup
  before a fresh database is created.

### Google Books integration

- Implemented `BookFinder` as the only module that calls Google Books.
- Supports title, author, and genre search plus details lookup by ID.
- Converts timeout, network, HTTP, invalid JSON, and unusable-response
  cases into `APIError`.
- Handles missing API fields safely with placeholders or empty lists.

### Validation and algorithms

- Search is case-insensitive across title, author, and category.
- Filters combine reading status, category, and minimum rating.
- Sort supports rating, published year, title, and date added; missing
  rating or published-year values remain last in either direction.
- Added validation for empty Google Books queries and IDs, invalid
  result limits, and non-integer reading progress.

## 4. Automated Test Report

Automated tests were run with pytest using a temporary SQLite database.
The tests do not modify the user's real library and do not require an
internet connection.

Command used:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q
```

Latest result:

```text
96 passed in 1.32s
```

`ruff check --no-cache .` also completed with no findings.

| Test module | Test count | Coverage in this module | Status |
|---|---:|---|---|
| `tests/test_book_finder.py` | 23 | Search fields and prefixes, details, missing fields, API key, invalid arguments, timeout/network/HTTP/JSON failures | Passed |
| `tests/test_data_store.py` | 9 | Save/load/update/delete, optional fields, missing database, corrupted-database recovery | Passed |
| `tests/test_library.py` | 22 | Add/remove/get, duplicates, local search, combined filters, all sort behavior, 1,000-entry sort performance | Passed |
| `tests/test_models.py` | 14 | Publication-year parsing, model equality, status labels, progress percentage | Passed |
| `tests/test_reading_tracker.py` | 28 | Status, valid/invalid progress, ratings, notes, persistence through `Library` | Passed |
| **Total** | **96** | **All Sprint 2 automated tests** | **Passed** |

Each pytest test has its own executable identifier, for example:

```text
tests/test_reading_tracker.py::TestSetRating::test_boolean_rating_raises
```

Running `pytest -v` displays all 96 identifiers and their individual
`PASSED` results.

## 5. Algorithm Performance

The benchmark used 1,000 unique `Book` objects created from the
300-record seed dataset. The library was prepared before timing. Each
operation ran seven times; the table reports the fastest and average
run in milliseconds.

| Operation | Records | Result count | Fastest (ms) | Average (ms) |
|---|---:|---:|---:|---:|
| Search keyword `silent` | 1,000 | 59 | 0.529 | 0.547 |
| Filter status `Reading` | 1,000 | 334 | 0.025 | 0.028 |
| Sort by published year | 1,000 | 1,000 | 0.729 | 0.743 |

The sort result is well below the target of 50 ms for 1,000 entries.
Timing values can vary by computer, so operation and dataset size
should be presented together.

## 6. Architecture and Refactoring

```text
Presentation (Sprint 3 web UI)
        -> Business Logic: BookFinder, Library, ReadingTracker, models
        -> Data Access: DataStore (SQLite), Google Books API
```

`Library` and `ReadingTracker` receive dependencies through their
constructors. This keeps SQL out of business logic and lets tests use
a temporary database. Testing also revealed validation gaps: invalid
progress types and invalid BookFinder arguments could produce raw
Python errors. These paths were refactored to use controlled errors.

## 7. Retrospective

### Wow!

- The layered design makes core rules testable without a CLI, browser,
  real database, or live API connection.
- SQLite persistence, corrupted-file recovery, and 96 automated tests
  provide a reliable base for the Sprint 3 web UI.
- Search, filter, and sort run quickly on a 1,000-entry library.

### Whoops!

- Early validation checked numeric bounds but did not reject every
  invalid type, including boolean, float, and text progress values.
- BookFinder did not reject blank search text or invalid result limits
  before calling the API.

### Fixes and next steps

- Added validation and automated tests for those edge cases.
- Sprint 3 connects the Streamlit UI to these existing back-end classes
  and turns custom exceptions into friendly user messages.

## 8. Definition of Done - Sprint 2

Taken from `PLAN.md`, section 10.3.

- [x] Books and library entries are saved to SQLite and remain present
  after a new `Library` instance is created.
- [x] A missing database file is created automatically; a corrupted
  file is backed up and replaced without a crash.
- [x] Duplicate additions and missing entries raise the planned custom
  exceptions.
- [x] Ratings outside 1-5 and invalid progress values are rejected.
- [x] Marking a known-page-count book Completed sets progress to the
  page count.
- [x] Case-insensitive library search handles title, author, category,
  and empty keywords.
- [x] Status, category, and minimum-rating filters work alone and in
  combination.
- [x] Rating, published-year, title, and date-added sorting works in
  both directions, keeping missing values last.
- [x] Google Books errors are converted into `APIError`; the Sprint 3
  UI will show those errors as friendly messages.
- [x] Search, filter, and sort timing for 1,000 entries is recorded in
  this report.
- [x] Core-logic and `DataStore` pytest tests pass.
- [x] `PLAN.md` has finalized UML and SQLite schema headings.
- [x] This report includes QA information and retrospective; the
  changelog has version 0.2.0.
- [ ] Documentation has not yet been delivered through a Sprint 2 Pull
  Request.

**Overall status:** The Sprint 2 back-end is complete. Commit the
documentation and open the Pull Request to complete the handoff.

## 9. Sprint 2 Handoff

Sprint 2 delivers the reusable back-end and automated test suite.
Sprint 3 integrates this code with the Streamlit web interface; the UI
must call existing business-logic methods and contain no SQL or
duplicated business rules.
