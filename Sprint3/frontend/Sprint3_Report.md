# Sprint 3 Report - Full-Stack Development

| Item | Detail |
|---|---|
| Project | BookLog |
| Course | CP352301 Script Programming - Semester 1/2569 |
| Sprint | Sprint 3 - Full-Stack Development |
| Team | Phattharawadee Songsrirod, Sujeephon Poobanchuen |
| Roles | Both members: Coder and Debugger |
| Repository | https://github.com/Fahnueaeiei/BookLog |
| Pull Request | https://github.com/Fahnueaeiei/BookLog/pull/2 |

---

## 1. Sprint Goal

Build the BookLog Streamlit front-end and integrate it with the reusable Sprint 2 back-end.

The Sprint 3 application provides a user-friendly web interface for searching books, viewing book details, managing a personal library, tracking reading progress, adding ratings and notes, and browsing books by category.

The front-end communicates with the existing Sprint 2 business-logic and data-access layers through a service layer. No SQL or duplicated business logic is implemented in the Streamlit interface.

---

## 2. Sprint Progress Summary

* [x] Created the Sprint 3 Streamlit front-end structure.
* [x] Designed and implemented the BookLog web interface.
* [x] Created a service layer between the Streamlit UI and Sprint 2 back-end.
* [x] Connected the application to the existing Sprint 2 `BookFinder`, `Library`, `ReadingTracker`, and `DataStore`.
* [x] Connected Google Books API for real book search and book details.
* [x] Implemented book search from the Home page.
* [x] Implemented book detail pages using real Google Books data.
* [x] Implemented adding and removing books from the personal library.
* [x] Implemented My Books with reading-status tabs.
* [x] Implemented reading progress tracking.
* [x] Implemented book rating and personal notes.
* [x] Implemented Home page sections for Continue Reading and Discover Books.
* [x] Implemented Browse functionality using Google Books genre search.
* [x] Added empty-state and error-handling messages for user actions.
* [x] Connected the application to the Sprint 2 SQLite database.

---

## 3. Work Completed

### Streamlit Front-End

The Sprint 3 front-end was implemented using Streamlit with a simple and consistent book-management interface.

Main features include:

* **Home** — Search Books, Continue Reading, and Discover Books
* **My Books** — Manage books by reading status: All, Want to Read, Reading, and Completed
* **Browse** — Discover books by category
* **Book Detail** — View book information and manage reading activities

The interface uses a cream background, neutral brown tones, Lato typography, reusable book cards, and a consistent navigation layout.

### Navigation

The application provides a top navigation bar with:

* BookLog logo
* Home
* My Books
* Browse
* Search Books

Streamlit session state is used to manage page navigation and selected books.

### Book Search and Details

The Home page connects to the Sprint 2 `BookFinder` and Google Books API for real-time book search.

Users can search for books by title and view detailed information including:

* Title
* Author
* Category
* Publication year
* Page count
* Cover
* Description

Duplicate search results are removed using the Google Books volume ID.

### Personal Library

The My Books page allows users to add, remove, and manage books in their personal library.

Books are organized into four reading-status tabs:

* All
* Want to Read
* Reading
* Completed

Library data is retrieved through the Sprint 2 `Library` and `DataStore` layers and stored in SQLite. The Streamlit UI does not access the database directly.

### Reading Tracking

Users can manage their reading activities through:

* Reading status
* Reading progress
* Rating from 1–5 stars
* Personal notes

These operations are handled by the existing Sprint 2 `ReadingTracker`, keeping the business rules in the back-end.

### Discover and Browse

**Discover Books** displays real book data retrieved through the back-end service.

**Browse** allows users to discover books by category using the existing Google Books genre-search functionality.

Example categories include Fiction, Romance, Mystery, Fantasy, Science, History, and Business.

### Reusable Book Card

A reusable `render_book_card()` component was created and used across:

* Search Results
* Discover Books
* My Books
* Browse Results

Each card displays the cover, title, author, category, publication year, and View Details button. CSS rules ensure consistent card heights and truncate long text with ellipses.


## 4. Back-End Integration

Sprint 3 integrates with the existing Sprint 2 back-end without modifying its source code.

```text
Sprint3/frontend/app.py
        ↓
Sprint3/frontend/src/service.py
        ↓
Sprint2 Back-End
 ├── BookFinder
 ├── Library
 ├── ReadingTracker
 └── DataStore
```

The `service.py` layer connects the Streamlit UI with Sprint 2 and converts back-end data into a format suitable for display.

Sprint 3 uses the **Google Books API** for book data and the existing **SQLite database** at:

```text
Sprint2/data/booklog.db
```

The API configuration is loaded from the Sprint 2 `.env` file, allowing Sprint 3 to use the same back-end services and persistent library data.

## 5. Error Handling and User Feedback

The Streamlit interface handles common user-facing situations with clear feedback messages.

Examples include:

* Empty search results
* Empty personal library
* No books in a selected reading-status tab
* No books found in a Browse category
* API or back-end errors during book operations
* Missing book covers

The UI displays friendly messages rather than exposing implementation details such as SQL errors or internal object structures.

Back-end exceptions continue to be handled by the Sprint 2 custom exception system.

---

## 6. Testing

**Test suite:** `test_sprint3_full.py`
**Total test cases:** 61
**Result:** 59 Passed, 1 Failed, 1 XFailed

| ID    | Test item                         | Input / Test condition                           | Expected result                                     | Actual result                                                            | Status     |
| ----- | --------------------------------- | ------------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------ | ---------- |
| TC-01 | Add book: DB & UI consistency     | Add valid book                                   | Book exists in DB and UI                            | Book existed in DB and UI                                                | PASSED     |
| TC-02 | Status consistency: Want to Read  | Set status to `Want to Read`                     | UI and DB show matching status                      | UI and DB matched                                                        | PASSED     |
| TC-03 | Status consistency: Reading       | Set status to `Reading`                          | UI and DB show matching status                      | UI and DB matched                                                        | PASSED     |
| TC-04 | Status consistency: Completed     | Set status to `Completed`                        | UI and DB show matching status                      | UI and DB matched                                                        | PASSED     |
| TC-05 | Progress DB/UI consistency        | Set 100 pages of 200                             | DB stores 100 pages; UI shows 50%                   | DB stored 100; UI showed 50%                                             | PASSED     |
| TC-06 | Completed progress                | Set status to Completed                          | UI shows 100%; DB stores full page count            | UI showed 100%; DB stored 200 pages                                      | PASSED     |
| TC-07 | Rating set and clear              | Set rating 4, then 0                             | Rating is stored and can be cleared                 | Rating stored and cleared correctly                                      | PASSED     |
| TC-08 | Note roundtrip                    | Save `"hello"`                                   | Note is stored and returned unchanged               | Note matched DB and UI                                                   | PASSED     |
| TC-09 | Remove book                       | Remove existing book                             | Book removed from DB and UI                         | Book removed from both                                                   | PASSED     |
| TC-10 | Persistence after restart         | Save status, rating and note; create new session | Data remains available                              | Data persisted correctly                                                 | PASSED     |
| TC-11 | Two-session consistency           | Session A sets rating 4; Session B reads it      | Session B sees latest value                         | Session B saw the latest value correctly                                 | PASSED     |
| TC-12 | Invalid progress: -1              | Progress = `-1`                                  | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-13 | Invalid progress: over page count | Progress = `201`                                 | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-14 | Invalid progress: extreme value   | Progress = `1000000000`                          | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-15 | Invalid progress: wrong type      | Progress = `"abc"`                               | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-16 | Invalid progress: None            | Progress = `None`                                | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-17 | Invalid progress: float           | Progress = `100.5`                               | `InvalidProgressError`                              | Exception raised; value unchanged                                        | PASSED     |
| TC-18 | Progress without page count       | Book has no page count; set progress 10          | `InvalidProgressError`                              | Exception raised; progress remained 0                                    | PASSED     |
| TC-19 | Progress boundary: 0              | 0 pages of 200                                   | UI shows 0%                                         | UI showed 0%                                                             | PASSED     |
| TC-20 | Progress boundary: 100            | 100 pages of 200                                 | UI shows 50%                                        | UI showed 50%                                                            | PASSED     |
| TC-21 | Progress boundary: 200            | 200 pages of 200                                 | UI shows 100%                                       | UI showed 100%                                                           | PASSED     |
| TC-22 | Valid rating: 1                   | Rating = 1                                       | Accepted                                            | Accepted                                                                 | PASSED     |
| TC-23 | Valid rating: 2                   | Rating = 2                                       | Accepted                                            | Accepted                                                                 | PASSED     |
| TC-24 | Valid rating: 3                   | Rating = 3                                       | Accepted                                            | Accepted                                                                 | PASSED     |
| TC-25 | Valid rating: 4                   | Rating = 4                                       | Accepted                                            | Accepted                                                                 | PASSED     |
| TC-26 | Valid rating: 5                   | Rating = 5                                       | Accepted                                            | Accepted                                                                 | PASSED     |
| TC-27 | Invalid rating: -1                | Rating = `-1`                                    | `InvalidRatingError` or `ValueError`                | Expected validation exception raised                                     | PASSED     |
| TC-28 | Invalid rating: 6                 | Rating = `6`                                     | `InvalidRatingError` or `ValueError`                | Exception raised                                                         | PASSED     |
| TC-29 | Invalid rating: 4.5               | Rating = `4.5`                                   | `InvalidRatingError` or `ValueError`                | Exception raised                                                         | PASSED     |
| TC-30 | Invalid rating: string            | Rating = `"3"`                                   | `InvalidRatingError` or `ValueError`                | Expected validation exception raised                                     | PASSED     |
| TC-31 | Invalid rating: None              | Rating = `None`                                  | `InvalidRatingError` or `ValueError`                | Expected validation exception raised                                     | PASSED     |
| TC-32 | Empty note                        | Note = `""`                                      | Empty note is stored correctly                      | Stored correctly                                                         | PASSED     |
| TC-33 | Long note                         | 5,000-character note                             | Note is stored exactly                              | Stored correctly                                                         | PASSED     |
| TC-34 | Unicode note                      | Thai text + emoji                                | Note is stored exactly                              | Stored correctly                                                         | PASSED     |
| TC-35 | Script-like note                  | `<script>alert(1)</script>`                      | Note is stored as text                              | Stored correctly                                                         | PASSED     |
| TC-36 | Multiline note                    | `line1\nline2`                                   | Line breaks are preserved                           | Preserved correctly                                                      | PASSED     |
| TC-37 | Invalid status: Bogus             | Status = `Bogus`                                 | `ValueError`                                        | `ValueError` raised                                                      | PASSED     |
| TC-38 | Invalid status: None              | Status = `None`                                  | `ValueError`                                        | `ValueError` raised                                                      | PASSED     |
| TC-39 | Invalid status: lowercase         | Status = `reading`                               | `ValueError`                                        | `ValueError` raised                                                      | PASSED     |
| TC-40 | Invalid status: empty             | Status = `""`                                    | `ValueError`                                        | `ValueError` raised                                                      | PASSED     |
| TC-41 | Invalid status: wrong type        | Status = `3`                                     | `ValueError`                                        | `ValueError` raised                                                      | PASSED     |
| TC-42 | Duplicate book                    | Add same book twice                              | `DuplicateBookError`                                | Exception raised                                                         | PASSED     |
| TC-43 | Remove unknown book               | Remove non-existing ID                           | `BookNotFoundError`                                 | Exception raised                                                         | PASSED     |
| TC-44 | Update unknown status book        | Unknown ID + status                              | `BookNotFoundError`                                 | Exception raised                                                         | PASSED     |
| TC-45 | Update unknown progress book      | Unknown ID + progress                            | `BookNotFoundError`                                 | Exception raised                                                         | PASSED     |
| TC-46 | Update unknown rating book        | Unknown ID + rating                              | `BookNotFoundError`                                 | Exception raised                                                         | PASSED     |
| TC-47 | Update unknown note book          | Unknown ID + note                                | `BookNotFoundError`                                 | Exception raised                                                         | PASSED     |
| TC-48 | Empty library                     | No books in library                              | Return empty list                                   | Returned `[]`                                                            | PASSED     |
| TC-49 | Empty search                      | Search = `""`                                    | `ValueError`                                        | Exception raised                                                         | PASSED     |
| TC-50 | Whitespace search                 | Search = `"   "`                                 | `ValueError`                                        | Exception raised                                                         | PASSED     |
| TC-51 | None search                       | Search = `None`                                  | `ValueError`                                        | Exception raised                                                         | PASSED     |
| TC-52 | Wrong-type search                 | Search = `123`                                   | `ValueError`                                        | Exception raised                                                         | PASSED     |
| TC-53 | Missing DB file                   | DB file does not exist                           | DB is created and usable                            | DB created successfully                                                  | PASSED     |
| TC-54 | Empty DB file                     | Existing empty DB file                           | DB becomes usable                                   | DB was usable                                                            | PASSED     |
| TC-55 | Missing parent folder             | DB parent directory does not exist               | Parent folder and DB should be created              | Parent folder was not created                                            | **XFAIL**  |
| TC-56 | Corrupt DB                        | Invalid/corrupt DB contents                      | Error is handled using custom exception             | Custom exception handling worked                                         | PASSED     |
| TC-57 | Read-only DB                      | DB file set to read-only; update note            | `DatabaseError`                                     | `DatabaseError` raised                                                   | PASSED     |
| TC-58 | Dropped table                     | Drop `library_entries` table                     | Error is handled, not raw SQLite error              | Custom exception handling worked                                         | PASSED     |
| TC-59 | DB deleted while running          | Delete DB after initialization                   | Error is handled, not raw SQLite error              | Raw Windows `PermissionError` occurred while deleting the locked DB file | **FAILED** |
| TC-60 | Large library                     | Add 200 books                                    | All books returned, unique IDs, retrieval < 1 sec   | 200 books retrieved successfully within limit                            | PASSED     |
| TC-61 | Status filter counts              | Add 9 books across 3 statuses                    | Each status has 3 books; total matches library size | Counts were 3/3/3 and total matched                                      | PASSED     |

### Summary

| Result    |  Count |
| --------- | -----: |
| PASSED    |     59 |
| FAILED    |      1 |
| XFAILED   |      1 |
| **TOTAL** | **61** |

### Failed Test

The only failed test was **TC-59: DB deleted while running**.

1. **DB deletion while running (TC-59)**
   The test attempted to delete the SQLite database file while it was still being used by an active database connection. On Windows, the file was locked by the running process, resulting in a raw `PermissionError: [WinError 32]` before the test could reach the application's database-error handling logic.

### Expected Failure

**TC-55: Missing parent folder** was intentionally marked **XFAIL** because the current `DataStore` implementation does not automatically create a missing parent directory for the database file.

### Overall Test Assessment

The Sprint 3 test suite achieved **59 passing tests out of 61**, with one expected failure and one environment/platform-related failure. Core functionality including CRUD operations, UI–database consistency, persistence, progress tracking, rating and status validation, notes, search validation, exception handling, and large-library retrieval passed the tests. The remaining failed case concerns SQLite file locking behavior on Windows when attempting to delete an active database file.

---

## 7. Definition of Done - Sprint 3

* [x] Streamlit front-end is implemented.
* [x] Home page is implemented.
* [x] My Books page is implemented.
* [x] Book detail page is implemented.
* [x] Search is connected to Google Books API.
* [x] Real Google Books data is displayed in the UI.
* [x] Books can be added to the personal library.
* [x] Books can be removed from the personal library.
* [x] Library data is loaded from the Sprint 2 SQLite database.
* [x] Reading status can be changed from the UI.
* [x] Reading progress can be updated from the UI.
* [x] Book ratings can be updated from the UI.
* [x] Personal notes can be saved from the UI.
* [x] Discover Books uses real back-end data.
* [x] Browse supports genre-based book discovery.
* [x] Search results and library books use reusable book-card components.
* [x] Empty states are provided for empty library and search/category results.
* [x] SQL is not implemented in the Streamlit front-end.
* [x] Business rules remain in the Sprint 2 back-end.
* [x] Sprint 3 communicates with the back-end through the service layer.

---

## 8. Retrospective

### Wow!

* The existing Sprint 2 architecture made it possible to build the Streamlit interface without duplicating database and business-logic code.
* The service layer provided a clear boundary between the UI and the existing back-end.
* Using real Google Books data made the search and discovery features functional rather than dependent on static mock data.
* Reusing the same book-card component made the Home, Browse, and My Books interfaces more consistent.
* The existing `Library` and `ReadingTracker` classes allowed reading status, progress, rating, and notes to be integrated without rewriting the underlying rules.

### Whoops!

* Early versions of the front-end used mock data in some UI sections, which had to be replaced with real back-end data during integration.
* The initial front-end structure contained presentation and data-access concerns that needed to be separated through the service layer.
* Google Books API requests could produce rate-limit errors when multiple searches were performed unnecessarily.
* Different book-title and metadata lengths caused inconsistent card layouts before fixed-height and text-truncation CSS rules were added.
* Some Streamlit navigation and widget states required session-state handling to prevent unexpected page behavior after interactions.

### Fixes and Next Steps

* Replaced mock book data with real Google Books and Sprint 2 back-end data.
* Improved the UI by adding reusable book cards, consistent layouts, and session-state navigation.
* In the next sprint, the system will be further improved through additional testing and user experience enhancements. This will include testing the Front-End and Back-End integration, improving error handling for API or data-related issues, and refining the navigation and UI to make the application more convenient and consistent to use.

---

## 9. Sprint 3 Handoff

Sprint 3 delivers the Streamlit presentation layer and integrates it with the reusable Sprint 2 back-end.

The final architecture is:

```text
┌───────────────────────────────┐
│       Sprint 3 Front-End      │
│          Streamlit            │
│                               │
│ Home / Search / Browse        │
│ My Books / Book Details       │
└───────────────┬───────────────┘
                │
                ↓
┌───────────────────────────────┐
│       Sprint 3 Service        │
│          service.py            │
└───────────────┬───────────────┘
                │
                ↓
┌───────────────────────────────┐
│       Sprint 2 Back-End       │
│                               │
│ BookFinder                    │
│ Library                       │
│ ReadingTracker                │
│ DataStore                     │
│ Models                        │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ↓                ↓
 Google Books API     SQLite DB
```

The Sprint 3 UI uses the existing Sprint 2 business logic and data-access layer rather than implementing a second set of business rules.

**Overall status:** Sprint 3 front-end development and back-end integration are complete, with the Streamlit interface connected to the existing BookLog back-end and persistent library data.
