# Changelog

All notable changes to the BookLog Sprint 2 back-end are documented in
this file.

## [0.2.0] - 2026-09-28

### Added

- Domain models: `Book`, `LibraryEntry`, and `ReadingStatus`.
- Custom BookLog exceptions for missing entries, duplicates, invalid
  rating/progress, API failures, and database errors.
- `BookFinder` integration with the Google Books API for title, author,
  and genre searches plus volume-detail lookup.
- SQLite `DataStore` with automatic database/table creation, CRUD
  persistence, and corrupted-database backup and recovery.
- `Library` operations for add/remove/view, local keyword search,
  combined filters, and sorting by rating, year, title, or date added.
- `ReadingTracker` operations for status, progress, rating, and notes.
- Seed dataset and performance verification for 1,000 library entries.
- Automated pytest coverage for models, data storage, API behavior,
  library algorithms, and reading-tracker rules.
- Sprint 2 QA report with benchmark results and retrospective.

### Changed

- Finalized the Sprint 2 UML and SQLite data-model documentation in
  `PLAN.md`.
- Refined type annotations and test fixtures to satisfy `ruff` checks.

### Fixed

- Reject empty Google Books search text and book IDs before making API
  requests.
- Validate Google Books result limits as whole numbers from 1 to 40.
- Reject boolean, float, and text values as invalid reading progress.
- Convert unusable Google Books JSON response shapes into `APIError`.
- Ensure descending sorts also keep entries with missing values last.
