"""Mock book data and mock search for BookLog (Sprint 1).

Sprint 1 only builds the CLI front-end, so book data comes from this
hard-coded list. In Sprint 2 the Google Books API (BookFinder) replaces it.

A few books deliberately have missing fields and different date formats
(YYYY, YYYY-MM, YYYY-MM-DD) so the CLI can be tested against the kind of
messy data a real API returns. Descriptions are short summaries written for
this project, and the cover URLs are placeholders.
"""

MOCK_BOOKS = [
    {
        "book_id": "mock-001",
        "title": "Dune",
        "authors": ["Frank Herbert"],
        "description": (
            "A young nobleman's family takes control of a desert planet "
            "that is the only source of a valuable spice, and is drawn "
            "into a struggle for power."
        ),
        "published_date": "1965",
        "categories": ["Science Fiction"],
        "cover_url": "https://example.com/covers/mock-001.jpg",
        "page_count": 412,
    },
    {
        "book_id": "mock-002",
        "title": "The Hobbit",
        "authors": ["J.R.R. Tolkien"],
        "description": (
            "A quiet hobbit joins a company of dwarves on a journey to "
            "win back their treasure from a dragon."
        ),
        "published_date": "1937",
        "categories": ["Fantasy"],
        "cover_url": "https://example.com/covers/mock-002.jpg",
        "page_count": 310,
    },
    {
        "book_id": "mock-003",
        "title": "1984",
        "authors": ["George Orwell"],
        "description": (
            "In a state that watches everything its citizens do, a "
            "low-ranking official begins to question the Party."
        ),
        "published_date": "1949",
        "categories": ["Fiction", "Dystopian"],
        "cover_url": "https://example.com/covers/mock-003.jpg",
        "page_count": 328,
    },
    {
        "book_id": "mock-004",
        "title": "Pride and Prejudice",
        "authors": ["Jane Austen"],
        "description": (
            "Elizabeth Bennet deals with family pressure, class, and "
            "first impressions in her relationship with Mr. Darcy."
        ),
        "published_date": "1813",
        "categories": ["Classics", "Romance"],
        "cover_url": "https://example.com/covers/mock-004.jpg",
        "page_count": 279,
    },
    {
        "book_id": "mock-005",
        "title": "To Kill a Mockingbird",
        "authors": ["Harper Lee"],
        "description": (
            "Seen through a child's eyes, a small Southern town faces "
            "its own prejudice during a court trial."
        ),
        "published_date": "1960",
        "categories": ["Classics", "Fiction"],
        "cover_url": "https://example.com/covers/mock-005.jpg",
        "page_count": 336,
    },
    {
        "book_id": "mock-006",
        "title": "The Pragmatic Programmer",
        "authors": ["Andrew Hunt", "David Thomas"],
        "description": (
            "Practical advice on becoming a more effective and adaptable "
            "software developer."
        ),
        "published_date": "1999-10",
        "categories": ["Computers", "Programming"],
        "cover_url": "https://example.com/covers/mock-006.jpg",
        "page_count": 352,
    },
    {
        "book_id": "mock-007",
        "title": "Clean Code",
        "authors": ["Robert C. Martin"],
        "description": (
            "A guide to writing code that other people can read, change, "
            "and maintain."
        ),
        "published_date": "2008",
        "categories": ["Computers", "Software Engineering"],
        "cover_url": "https://example.com/covers/mock-007.jpg",
        "page_count": 464,
    },
    {
        "book_id": "mock-008",
        "title": "Harry Potter and the Philosopher's Stone",
        "authors": ["J.K. Rowling"],
        "description": (
            "An orphaned boy learns he is a wizard and starts his first "
            "year at a school of magic."
        ),
        "published_date": "1997-06-26",
        "categories": ["Fantasy", "Young Adult"],
        "cover_url": "https://example.com/covers/mock-008.jpg",
        "page_count": 223,
    },
    {
        "book_id": "mock-009",
        "title": "Atomic Habits",
        "authors": ["James Clear"],
        "description": (
            "A practical system for building good habits and breaking bad "
            "ones through small, steady changes."
        ),
        "published_date": "2018-10",
        "categories": ["Self-Help"],
        "cover_url": "https://example.com/covers/mock-009.jpg",
        "page_count": 320,
    },
    {
        "book_id": "mock-010",
        "title": "The Little Prince",
        "authors": ["Antoine de Saint-Exupery"],
        "description": (
            "A pilot stranded in the desert meets a young prince who "
            "tells him about the planets he has visited."
        ),
        "published_date": "1943",
        "categories": ["Fiction", "Fable"],
        "cover_url": None,  # missing cover
        "page_count": 96,
    },
    {
        "book_id": "mock-011",
        "title": "Educated",
        "authors": ["Tara Westover"],
        "description": (
            "A memoir about growing up in a strict, isolated family and "
            "finding a way to education."
        ),
        "published_date": "2018-02",
        "categories": ["Biography", "Memoir"],
        "cover_url": "https://example.com/covers/mock-011.jpg",
        "page_count": 334,
    },
    {
        "book_id": "mock-012",
        "title": "The Martian",
        "authors": ["Andy Weir"],
        "description": (
            "An astronaut left behind on Mars must find a way to survive "
            "until a rescue is possible."
        ),
        "published_date": "2014",
        "categories": ["Science Fiction"],
        "cover_url": "https://example.com/covers/mock-012.jpg",
        "page_count": 369,
    },
    {
        "book_id": "mock-013",
        "title": "Norwegian Wood",
        "authors": ["Haruki Murakami"],
        "description": None,  # missing description
        "published_date": "1987",
        "categories": ["Fiction"],
        "cover_url": None,  # missing cover
        "page_count": None,  # missing page count
    },
]

SEARCH_FIELDS = ("title", "author", "genre")


def search_mock_books(field, keyword):
    """Search the mock books by title, author, or genre.

    The match is case-insensitive and finds the keyword anywhere in the text.

    Args:
        field: One of "title", "author", or "genre".
        keyword: Text to look for. Spaces around it are ignored.

    Returns:
        A list of matching book dictionaries. The list is empty when the
        keyword is empty or nothing matches.

    Raises:
        ValueError: If field is not one of the supported search fields.
    """
    if field not in SEARCH_FIELDS:
        raise ValueError(f"Unknown search field: {field}")

    keyword = keyword.strip().lower()
    if not keyword:
        return []

    results = []
    for book in MOCK_BOOKS:
        if field == "title":
            texts = [book["title"]]
        elif field == "author":
            texts = book["authors"]
        else:
            texts = book["categories"]

        if any(keyword in text.lower() for text in texts):
            results.append(book)

    return results