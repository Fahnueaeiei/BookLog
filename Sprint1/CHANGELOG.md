# Changelog — Sprint 1

## [0.1.0] - 2026-09-21

### Added
- CLI front-end for BookLog: welcome banner and main menu (Search Books, My Library, Exit).
- Command input handling: commands are stripped of spaces and lowercased. Typing `quit` in any letter case exits from any menu or the search prompt.
- Input validation with `try-except ValueError`: non-numeric, negative, and out-of-range input is rejected with a message and the prompt repeats.
- Search Books: search by title, author, or genre (case-insensitive) over mock data, a results list, and a book details view (title, author(s), published date, categories, pages, cover, description).
- Mock dataset of 13 books. Some books have a missing description, cover, or page count, and the published dates use the formats `YYYY`, `YYYY-MM`, and `YYYY-MM-DD`.
- My Library (in memory only): add a book, remove it (with confirmation), set the reading status (Want to Read / Reading / Completed), update reading progress in pages, set a rating from 1 to 5 (or clear it), and edit notes.
- Reading rules: pages read cannot be negative or above the page count; marking a book as Completed sets progress to the page count; adding a book that is already in the library is rejected.
- Placeholders for missing book data ("Unknown", "No cover available", "No description available.").
- Program exits cleanly on Ctrl+C and Ctrl+D.
- Sprint 1 report with the QA table and the retrospective (`Sprint1_Report.md`).

### Changed
- Project topic changed to BookLog (books and reading tracker) from the earlier topic. The CLI was rebuilt for the new topic and keeps the numbered-menu flow of the earlier CLI.
- Project plan rewritten as one `PLAN.md` for the whole project, with a Definition of Done for each sprint.
- Repository reorganized into `Sprint1/`, `Sprint2/`, and `Sprint3/` folders, with a changelog in each sprint folder.

### Fixed
- Search Books: "Try again" after an empty search or no results now re-prompts for a new keyword under the same field (title/author/genre), instead of incorrectly returning to the "Search by" field-selection menu.