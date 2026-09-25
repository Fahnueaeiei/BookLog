"""Command-line interface (Presentation Layer) for BookLog (Sprint 1).

Sprint 1 goal: build the front-end flow and see how the application will be
structured. Book data comes from mock data, and the personal library is kept
in memory only, so it is lost when the program closes. Saving to SQLite and
the real business logic classes arrive in Sprint 2.
"""

import textwrap

from src.mock_data import SEARCH_FIELDS, search_mock_books

STATUS_LABELS = {
    "want_to_read": "Want to Read",
    "reading": "Reading",
    "completed": "Completed",
}
STATUS_ORDER = ["want_to_read", "reading", "completed"]

MIN_RATING = 1
MAX_RATING = 5


class QuitProgram(Exception):
    """Raised when the user types 'quit' to exit the program."""


class CLI:
    """Menus, input handling, and display for BookLog.

    Attributes:
        library: In-memory library. Maps book_id to an entry dictionary with
            the keys "book", "status", "pages_read", "rating", and "notes".
    """

    def __init__(self):
        """Create the CLI with an empty in-memory library."""
        self.library = {}

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------
    def get_command_input(self, prompt="\nSelect: "):
        """Read a command, strip spaces around it, and lowercase it.

        Raises:
            QuitProgram: If the user types 'quit' in any letter case.
        """
        command = input(prompt).strip().lower()
        if command == "quit":
            raise QuitProgram
        return command

    def get_text_input(self, prompt, allow_quit=True):
        """Read free text. Spaces are stripped but letter case is kept.

        Args:
            prompt: Text shown to the user.
            allow_quit: If True, typing 'quit' raises QuitProgram.

        Raises:
            QuitProgram: If allow_quit is True and the user types 'quit'.
        """
        text = input(prompt).strip()
        if allow_quit and text.lower() == "quit":
            raise QuitProgram
        return text

    def get_menu_choice(self, min_value, max_value):
        """Ask for a menu number and repeat until it is in the valid range."""
        message = f"[!] Invalid input. Please select {min_value}-{max_value}."

        while True:
            raw = self.get_command_input("\nSelect: ")

            try:
                choice = int(raw)
            except ValueError:
                print(message)
                continue

            if min_value <= choice <= max_value:
                return choice

            print(message)

    def get_number(self, prompt, min_value, max_value=None, label="Value"):
        """Ask for a whole number and repeat until it is valid.

        Args:
            prompt: Text shown to the user.
            min_value: Smallest accepted number.
            max_value: Largest accepted number, or None for no upper limit.
            label: Name used in the error message.

        Returns:
            The number, or None if the user types 'back'.
        """
        while True:
            raw = self.get_command_input(f"{prompt} (or 'back'): ")

            if raw == "back":
                return None

            try:
                number = int(raw)
            except ValueError:
                print("[!] Invalid input. Please enter a whole number.")
                continue

            too_small = number < min_value
            too_big = max_value is not None and number > max_value

            if too_small or too_big:
                if max_value is None:
                    print(f"[!] {label} must be at least {min_value}.")
                else:
                    print(
                        f"[!] {label} must be between "
                        f"{min_value} and {max_value}."
                    )
                continue

            return number

    def ask_try_again(self):
        """Show 'Try again / Back'. Return True if the user retries."""
        print("\n1. Try again")
        print("2. Back")
        return self.get_menu_choice(1, 2) == 1

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    def display_welcome_message(self):
        """Show the welcome banner."""
        print("\n=====================================")
        print("  BookLog - Your Personal Book Library")
        print("=====================================")
        print("Search for books, build your library, and track your reading.")
        print("Tip: type 'quit' at any menu to exit.")

    def display_main_menu(self):
        """Show the main menu."""
        print("\n---------- Main Menu ----------")
        print("1. Search Books")
        print("2. My Library")
        print("3. Exit")

    @staticmethod
    def format_authors(book):
        """Return the authors as text, or 'Unknown author' if none."""
        authors = book.get("authors") or []
        return ", ".join(authors) if authors else "Unknown author"

    @staticmethod
    def format_progress(entry):
        """Return reading progress as text, e.g. '120/412 pages (29%)'."""
        pages_read = entry["pages_read"]
        page_count = entry["book"].get("page_count")

        if page_count:
            percent = round(100 * pages_read / page_count)
            return f"{pages_read}/{page_count} pages ({percent}%)"
        return f"{pages_read} pages"

    @staticmethod
    def format_rating(entry):
        """Return the rating as text, e.g. '4/5', or 'Not rated'."""
        rating = entry["rating"]
        return f"{rating}/{MAX_RATING}" if rating else "Not rated"

    def display_book_list(self, books):
        """Show a numbered list of books."""
        for index, book in enumerate(books, start=1):
            print(f"{index}. {book['title']} - {self.format_authors(book)}")

    def display_book_details(self, book):
        """Show the details of one book. Missing fields show a placeholder."""
        print("\n--------------------------------")
        print(book["title"])
        print("--------------------------------")
        print(f"Author(s):  {self.format_authors(book)}")
        print(f"Published:  {book.get('published_date') or 'Unknown'}")

        categories = ", ".join(book.get("categories") or []) or "Uncategorized"
        print(f"Categories: {categories}")
        print(f"Pages:      {book.get('page_count') or 'Unknown'}")
        print(f"Cover:      {book.get('cover_url') or 'No cover available'}")

        description = book.get("description") or "No description available."
        print("\nDescription:")
        print(textwrap.fill(description, width=70))

    def display_library(self, entries):
        """Show the library with status, progress, and rating."""
        for index, entry in enumerate(entries, start=1):
            book = entry["book"]
            print(f"{index}. {book['title']} - {self.format_authors(book)}")
            print(
                f"   {STATUS_LABELS[entry['status']]} | "
                f"{self.format_progress(entry)} | "
                f"{self.format_rating(entry)}"
            )

    # ------------------------------------------------------------------
    # Search Books
    # ------------------------------------------------------------------
    def search_books(self):
        """Search flow: choose a field, enter a keyword, then pick a result."""
        while True:
            print("\n---------- Search Books ----------")
            print("Search by:")
            print("1. Title")
            print("2. Author")
            print("3. Genre")
            print("4. Back")

            choice = self.get_menu_choice(1, 4)
            if choice == 4:
                return

            field = SEARCH_FIELDS[choice - 1]
            keyword = self.get_text_input(f"\nEnter {field} to search: ")

            if not keyword:
                print("\n[!] Search text cannot be empty.")
                if not self.ask_try_again():
                    return
                continue

            results = search_mock_books(field, keyword)

            if not results:
                print(f"\n[!] No books found for {field} '{keyword}'.")
                if not self.ask_try_again():
                    return
                continue

            self.show_search_results(results)

    def show_search_results(self, results):
        """Show the search results and let the user open one."""
        while True:
            print(f"\nFound {len(results)} book(s):")
            self.display_book_list(results)
            print(f"{len(results) + 1}. Back")

            choice = self.get_menu_choice(1, len(results) + 1)
            if choice == len(results) + 1:
                return

            self.show_book_from_search(results[choice - 1])

    def show_book_from_search(self, book):
        """Show a book's details and offer to add it to the library."""
        self.display_book_details(book)

        print("\n1. Add to My Library")
        print("2. Back")

        if self.get_menu_choice(1, 2) == 1:
            self.add_to_library(book)

    def add_to_library(self, book):
        """Add a book to the in-memory library as 'Want to Read'."""
        if book["book_id"] in self.library:
            print("\n[!] This book is already in your library.")
            return

        self.library[book["book_id"]] = {
            "book": book,
            "status": "want_to_read",
            "pages_read": 0,
            "rating": None,
            "notes": "",
        }
        print(f"\n'{book['title']}' was added as 'Want to Read'.")

    # ------------------------------------------------------------------
    # My Library
    # ------------------------------------------------------------------
    def my_library(self):
        """Show the library and let the user open a book."""
        while True:
            print("\n---------- My Library ----------")
            entries = list(self.library.values())

            if not entries:
                print("\nYour library is empty.")
                print("Use 'Search Books' to add some books.")
                return

            self.display_library(entries)
            print(f"{len(entries) + 1}. Back")

            choice = self.get_menu_choice(1, len(entries) + 1)
            if choice == len(entries) + 1:
                return

            self.manage_entry(entries[choice - 1])

    def manage_entry(self, entry):
        """Show one library book and let the user change or remove it."""
        book = entry["book"]

        while True:
            print(f"\n---------- {book['title']} ----------")
            print(f"Status:   {STATUS_LABELS[entry['status']]}")
            print(f"Progress: {self.format_progress(entry)}")
            print(f"Rating:   {self.format_rating(entry)}")
            print(f"Notes:    {entry['notes'] or '(none)'}")

            print("\n1. View book details")
            print("2. Update status")
            print("3. Update progress")
            print("4. Set rating")
            print("5. Edit notes")
            print("6. Remove from library")
            print("7. Back")

            choice = self.get_menu_choice(1, 7)

            if choice == 1:
                self.display_book_details(book)
            elif choice == 2:
                self.update_status(entry)
            elif choice == 3:
                self.update_progress(entry)
            elif choice == 4:
                self.update_rating(entry)
            elif choice == 5:
                self.edit_notes(entry)
            elif choice == 6:
                if self.remove_from_library(entry):
                    return
            elif choice == 7:
                return

    def update_status(self, entry):
        """Change the status. 'Completed' sets progress to all pages."""
        print("\nSet status:")
        for index, key in enumerate(STATUS_ORDER, start=1):
            print(f"{index}. {STATUS_LABELS[key]}")
        print(f"{len(STATUS_ORDER) + 1}. Cancel")

        choice = self.get_menu_choice(1, len(STATUS_ORDER) + 1)
        if choice == len(STATUS_ORDER) + 1:
            return

        entry["status"] = STATUS_ORDER[choice - 1]

        page_count = entry["book"].get("page_count")
        if entry["status"] == "completed" and page_count:
            entry["pages_read"] = page_count

        print(f"\nStatus updated to '{STATUS_LABELS[entry['status']]}'.")

    def update_progress(self, entry):
        """Change pages read. It cannot be negative or above the page count."""
        page_count = entry["book"].get("page_count") or None

        if page_count:
            print(f"\nThis book has {page_count} pages.")
        else:
            print("\nThe page count of this book is unknown.")

        pages_read = self.get_number(
            "Pages read", 0, page_count, label="Pages read"
        )
        if pages_read is None:
            return

        entry["pages_read"] = pages_read
        print("\nProgress updated.")

    def update_rating(self, entry):
        """Set the rating (1-5), or clear it by typing 'clear'."""
        while True:
            raw = self.get_command_input(
                f"\nRating {MIN_RATING}-{MAX_RATING} "
                f"('clear' to remove, 'back' to cancel): "
            )

            if raw == "back":
                return

            if raw == "clear":
                entry["rating"] = None
                print("\nRating cleared.")
                return

            try:
                rating = int(raw)
            except ValueError:
                print(
                    f"[!] Invalid input. Please enter a whole number "
                    f"from {MIN_RATING} to {MAX_RATING}."
                )
                continue

            if not MIN_RATING <= rating <= MAX_RATING:
                print(
                    "[!] Rating must be between "
                    f"{MIN_RATING} and {MAX_RATING}."
                )
                continue

            entry["rating"] = rating
            print(f"\nRating set to {rating}/{MAX_RATING}.")
            return

    def edit_notes(self, entry):
        """Replace the notes. Empty input cancels; 'clear' removes them."""
        print(f"\nCurrent notes: {entry['notes'] or '(none)'}")
        text = self.get_text_input(
            "Enter new notes (Enter to cancel, 'clear' to remove): ",
            allow_quit=False,
        )

        if not text:
            print("\nNo changes made.")
        elif text.lower() == "clear":
            entry["notes"] = ""
            print("\nNotes cleared.")
        else:
            entry["notes"] = text
            print("\nNotes saved.")

    def remove_from_library(self, entry):
        """Ask for confirmation, then remove the book. True if removed."""
        book = entry["book"]
        print(f"\nRemove '{book['title']}' from your library?")
        print("1. Yes, remove it")
        print("2. No, keep it")

        if self.get_menu_choice(1, 2) == 2:
            return False

        del self.library[book["book_id"]]
        print(f"\n'{book['title']}' was removed from your library.")
        return True