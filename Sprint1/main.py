"""BookLog - Sprint 1 entry point (CLI front-end with mock data).

Run from the Sprint1 folder:

    python main.py
"""

from src.cli import CLI, QuitProgram


def main():
    """Run the main menu loop until the user exits.

    The program ends when the user chooses Exit, types 'quit' at any menu,
    or closes the input (Ctrl+C / Ctrl+D).
    """
    cli = CLI()
    cli.display_welcome_message()

    try:
        while True:
            try:
                cli.display_main_menu()
                choice = cli.get_menu_choice(1, 3)

                if choice == 1:
                    cli.search_books()
                elif choice == 2:
                    cli.my_library()
                elif choice == 3:
                    break
            except ValueError:
                # Safety net: menu helpers already handle invalid numbers.
                print("\n[!] Invalid input. Please try again.")
    except (QuitProgram, KeyboardInterrupt, EOFError):
        pass

    print("\nThanks for using BookLog. Happy reading!")


if __name__ == "__main__":
    main()