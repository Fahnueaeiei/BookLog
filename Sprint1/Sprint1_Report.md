# Sprint 1 Result Report

- **Project Name:** BookLog
- **Sprint:** 1 (Building the Foundation: Plan + CLI)
- **Team Members:**
  - Planner / Team Leader: *Phattharawadee Songsrirod*
  - Coder & Debugger: *Sujeephon Poobanchuen*
- **Repository:** https://github.com/Fahnueaeiei/Booklog
- **Pull Request:** https://github.com/Fahnueaeiei/Booklog/pull/1

> Sprint 1 was redone after the project topic changed to BookLog.

## 1. Sprint Progress Summary

- [x] Defined the project scope and Definition of Done in `PLAN.md`
- [x] Designed the CLI menu and main application flow
- [x] Implemented the CLI as separate functions: welcome message, command input, displays, and `main()` loop
- [x] Implemented book search by title, author, and genre using mock data
- [x] Displayed book details, with placeholders for missing data
- [x] Implemented the in-memory library: add, remove, status, progress, rating, and notes
- [x] Added input validation and error handling (`try-except ValueError`, empty input, out-of-range values)
- [x] Tested the edge cases in the QA table below
- [x] Wrote the sprint changelog (`CHANGELOG.md`, version 0.1.0)
- [x] Delivered the code through a Pull Request on GitHub

## 2. Quality Assurance & Debugging Report

Each test was run by starting `python main.py` and entering the inputs shown.

| ID    | Test item | Input used | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| TC-01 | Start and exit | Run the program, then `3` | Banner and 3-option menu are shown; Exit shows a goodbye message | Banner and menu shown; goodbye message shown and the program ended | PASSED |
| TC-02 | Quit, lowercase | `quit` at the main menu | Goodbye message and the program stops | Goodbye message shown and the program stopped | PASSED |
| TC-03 | Quit, uppercase | `QUIT` | Same as above | Same as above | PASSED |
| TC-04 | Quit, spaces and mixed case | `  QuIt  ` | Same as above | Same as above | PASSED |
| TC-05 | Quit inside a submenu | `1`, then `Quit` at the Search by menu | Program exits immediately | Goodbye message shown and the program stopped | PASSED |
| TC-06 | Quit at the search text prompt | `1`, `1`, then ` QUIT ` | Program exits immediately | Goodbye message shown and the program stopped | PASSED |
| TC-07 | Invalid menu input | `abc`, `-1`, `99`, empty input, `2.5` | Message is shown, the prompt repeats, no crash | "[!] Invalid input. Please select 1-3." shown for each input; no crash | PASSED |
| TC-08 | Search by title | `1`, `1`, `dune` | Dune is listed | "Found 1 book(s): 1. Dune - Frank Herbert" | PASSED |
| TC-09 | Search is case-insensitive | `DUNE` | Same result as `dune` | Same result as `dune` | PASSED |
| TC-10 | Search by author | `1`, `2`, `tolkien` | The Hobbit is listed | "1. The Hobbit - J.R.R. Tolkien" | PASSED |
| TC-11 | Search by genre | `1`, `3`, `fantasy` | Both fantasy books are listed | 2 books found: The Hobbit and Harry Potter and the Philosopher's Stone | PASSED |
| TC-12 | Empty search | Spaces only as the search text | Message shown with "Try again / Back" | "[!] Search text cannot be empty." with the 2 options; Back returned to the main menu | PASSED |
| TC-13 | No results | `zzzz` | "No books found" message | "[!] No books found for title 'zzzz'." | PASSED |
| TC-14 | Book with missing data | Open the details of Norwegian Wood | Placeholders instead of missing fields | "Pages: Unknown", "Cover: No cover available", "No description available." | PASSED |
| TC-15 | Add a book to the library | Add Dune from the results | Added as Want to Read and shown in My Library | Added; library shows "Want to Read \| 0/412 pages (0%) \| Not rated" | PASSED |
| TC-16 | Add a duplicate | Add Dune twice | Message shown and no second copy | "[!] This book is already in your library." | PASSED |
| TC-17 | Empty library | My Library with no books | Message shown, no crash | "Your library is empty." | PASSED |
| TC-18 | Status: Completed | Set Dune to Completed | Progress becomes all pages | "Progress: 412/412 pages (100%)" | PASSED |
| TC-19 | Progress above the page count | `999` for Dune | Rejected with a message | "[!] Pages read must be between 0 and 412." | PASSED |
| TC-20 | Negative progress | `-5` | Rejected with a message | "[!] Pages read must be between 0 and 412." | PASSED |
| TC-21 | Progress is not a number | `abc` | Rejected with a message | "[!] Invalid input. Please enter a whole number." | PASSED |
| TC-22 | Valid progress | `150` | Saved | "Progress: 150/412 pages (36%)" | PASSED |
| TC-23 | Unknown page count | Norwegian Wood: `-1`, then `99999` | Negative is rejected; a large value is accepted | "[!] Pages read must be at least 0."; "Progress: 99999 pages" | PASSED |
| TC-24 | Rating: invalid, then valid | `6`, `0`, `abc`, then `4` | Invalid values rejected; 4 saved | Rating messages shown for `6`, `0`, and `abc`; "Rating set to 4/5." | PASSED |
| TC-25 | Clear the rating | `clear` | Rating removed | "Rating cleared." and "Rating: Not rated" | PASSED |
| TC-26 | Notes keep letter case | `My Note With CAPS`, then `clear` | Text is saved as typed, then removed | "Notes: My Note With CAPS", then "Notes cleared." | PASSED |
| TC-27 | `quit` typed as a note | `quit` at the notes prompt | Saved as text; program keeps running | "Notes: quit" and the program continued | PASSED |
| TC-28 | Remove with confirmation | `No`, then `Yes` | No keeps the book; Yes removes it | Book kept after No; "'Dune' was removed from your library." after Yes | PASSED |
| TC-29 | Input closed (Ctrl+D) | End of input at a prompt | Program exits cleanly | Goodbye message shown, no error | PASSED |
| TC-30 | Ctrl+C | Ctrl+C at a prompt | Program exits cleanly | Goodbye message shown, no error | PASSED |
| TC-31 | "Try again" after no results | 1, 3 (Genre), fix (no match), 1 (Try again), fic | Re-prompts for a genre keyword directly (same field), not the "Search by" field-selection menu | Re-prompted "Enter genre to search:" directly; found 6 books for 'fic' | PASSED |

## 3. Weekly Retrospective (Wow! & Whoops!)

### Wow! (what went well)
- The CLI is split into small functions and one `CLI` class (display, input, flows) with a short `main()` loop. Every function and class has a docstring, and the code passes `pycodestyle` and `pyflakes`.
- Input handling is in three helpers (`get_command_input`, `get_menu_choice`, `get_number`), so `quit` works everywhere and invalid numbers never crash the program. All 30 test cases pass.
- The mock data deliberately includes missing fields and mixed date formats (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`), so the placeholder handling is tested before the real Google Books API arrives in Sprint 2.
- The reading rules (progress limits, Completed sets progress, no duplicates) already work in the prototype, so Sprint 2 can move them into the business logic layer.

### Whoops! (problems found and how they were fixed)
- **Problem:** The earlier CLI (from the previous project topic) did not match the Sprint 1 guide. It had no `quit` command, checked menu input with `isdigit()` instead of `try-except ValueError`, and ended with a Python error when input was closed with Ctrl+C or Ctrl+D.
  **Fix:** Rebuilt the input helpers and handled `QuitProgram`, `KeyboardInterrupt`, and `EOFError` in `main()`.
- **Problem:** Lowercasing works for commands but would ruin free text such as notes, which would lose their capital letters.
  **Fix:** Added a separate `get_text_input()` that only strips spaces. `quit` is not recognized at the notes prompt, so typed notes are not lost by accident.
- **Problem:** The style check found lines longer than 79 characters (PEP 8).
  **Fix:** Reflowed the long lines and ran the check again until it was clean.
- **Problem:** In `search_books()`, choosing "Try again" after an empty search or "no results found" incorrectly looped back to the top-level "Search by" field-selection menu (Title/Author/Genre) instead of re-prompting for a new keyword under the same field. Found while manually re-testing the genre search flow.
  **Fix:** Split the keyword-prompt-and-search logic out into its own method, `search_by_keyword(field)`, with its own retry loop. "Try again" now re-prompts for a keyword under the same field; "Back" still exits the whole search flow to the main menu, unchanged.

### Carried over to Sprint 2
- The library lives in memory only, so it is lost when the program closes. SQLite persistence is Sprint 2 work.
- Book data is mock data. The Google Books API replaces it in Sprint 2.
- Search finds the keyword anywhere in the text. The search, filter, and sort algorithms for the library are Sprint 2 work.

## 4. Definition of Done — Sprint 1

Taken from `PLAN.md`, section 10.2.

- [x] Typing `quit` in any letter case and with extra spaces exits the program immediately with a goodbye message
- [x] A non-numeric, negative, or out-of-range menu choice shows a message and asks again without crashing
- [x] An empty search shows a message and lets the user try again or go back
- [x] Searching mock data by title, author, or genre lists the matching books; selecting one shows its details
- [x] A book can be added to and removed from the in-memory library, and its status, progress, rating, and notes can be changed
- [x] A rating outside 1–5 and invalid progress are rejected with a message
- [x] Every function has a docstring; code is split into functions and classes (display, input, main)
- [x] This report includes the QA table and Wow!/Whoops!; `CHANGELOG.md` has version 0.1.0
- [x] Delivered through a Pull Request

**Overall status:** Sprint 1 is complete except for opening the Pull Request. Persistence, the real book data source, and the library algorithms are planned for Sprint 2.