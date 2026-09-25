"""Live smoke test: proves BookFinder can reach the REAL Google Books
API — nothing here is mocked.

This is deliberately separate from the pytest suite (which mocks
requests.get on purpose, for speed and repeatability). Run this file
directly whenever you want to confirm the actual network connection
still works, e.g. right before a live demo.

Run from the Sprint2 project root:

    python3 book_finder_live_check.py
"""

import sys

from src.book_finder import BookFinder
from src.exceptions import APIError

# Change these two to try different searches.
SEARCH_FIELD = "author"
SEARCH_KEYWORD = "dan brown"


def main():
    finder = BookFinder()  # picks up GOOGLE_BOOKS_API_KEY from .env if set

    print(f"Searching Google Books for {SEARCH_FIELD}:'{SEARCH_KEYWORD}'...")
    try:
        results = finder.search(SEARCH_FIELD, SEARCH_KEYWORD)
    except APIError as error:
        print(f"FAILED — could not reach the real API: {error}")
        sys.exit(1)

    if not results:
        print(f"Connected, but got zero results for '{SEARCH_KEYWORD}'.")
        sys.exit(1)

    print(f"SUCCESS — got {len(results)} real result(s) from Google Books.\n")

    for i, book in enumerate(results, start=1):
        authors = ", ".join(book.authors) if book.authors else "Unknown author"
        year = book.published_year or "?"
        print(f"{i:>2}. {book.title} — {authors} ({year})")


if __name__ == "__main__":
    main()