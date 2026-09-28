# Changelog

All notable changes to the BookLog Sprint 3 front-end and back-end
integration are documented in this file.

## [0.3.0] - 2026-09-28

### Added

* Streamlit front-end for the BookLog application.
* Home page with book search, Continue Reading, and Discover Books.
* My Books page with All, Want to Read, Reading, and Completed views.
* Book Detail page for viewing book information and managing reading activities.
* Browse functionality for discovering books by category.
* Reusable `render_book_card()` component for displaying books consistently
  across the application.
* Reading management features for status, progress, ratings, and personal
  notes.
* Session-state navigation for managing pages and selected books.
* `service.py` service layer for connecting the Streamlit front-end with
  the Sprint 2 back-end.

### Changed

* Replaced mock book data with real data from the Google Books API.
* Connected the front-end to the existing Sprint 2 `BookFinder`, `Library`,
  `ReadingTracker`, and `DataStore`.
* Reused the existing SQLite database from Sprint 2 for persistent library
  data.
* Improved the UI with a consistent navigation layout, reusable book cards,
  cream and neutral-brown styling, and Lato typography.
* Added duplicate-result handling for Google Books search results.
* Added consistent text truncation and card sizing for book lists.

### Fixed

* Removed dependencies on mock book data from the Sprint 3 front-end.
* Prevented duplicate books from appearing in search results.
* Improved navigation and selected-book handling using Streamlit
  session state.
* Prevented unnecessary direct database access from the front-end by
  routing operations through the service layer.
* Improved handling of missing book information such as covers,
  categories, authors, and page counts.
