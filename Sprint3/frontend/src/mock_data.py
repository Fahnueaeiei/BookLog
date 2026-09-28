# =========================================================
# Mock Data
# =========================================================

mock_books = [
    {
        "id": "atomic-habits",
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self-help",
        "year": "2018",
        "pages": 320,
        "cover": "https://covers.openlibrary.org/b/isbn/9780735211292-M.jpg",
        "description": (
            "A practical guide to building good habits, breaking bad ones, "
            "and making lasting changes through small, consistent improvements."
        ),
        "rating": 4.8,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "the-psychology-of-money",
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "category": "Finance",
        "year": "2020",
        "pages": 256,
        "cover": "https://covers.openlibrary.org/b/isbn/9780857197689-M.jpg",
        "description": (
            "An exploration of the unusual ways people think about money, "
            "wealth, investing, and financial decisions."
        ),
        "rating": 4.7,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "the-alchemist",
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "year": "1988",
        "pages": 208,
        "cover": "https://covers.openlibrary.org/b/isbn/9780062315007-M.jpg",
        "description": (
            "A philosophical novel about a young shepherd who travels in "
            "search of a treasure and discovers his own purpose along the way."
        ),
        "rating": 4.6,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "1984",
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopian",
        "year": "1949",
        "pages": 328,
        "cover": "https://covers.openlibrary.org/b/isbn/9780451524935-M.jpg",
        "description": (
            "A dystopian novel about surveillance, political control, "
            "and a society where independent thought is strictly restricted."
        ),
        "rating": 4.7,
        "hot": True,
        "recommended": False,
    },
    {
        "id": "the-great-gatsby",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Fiction",
        "year": "1925",
        "pages": 180,
        "cover": "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg",
        "description": (
            "A classic novel about love, ambition, wealth, and the "
            "American Dream in the 1920s."
        ),
        "rating": 4.4,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "harry-potter",
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "category": "Fantasy",
        "year": "1997",
        "pages": 309,
        "cover": "https://covers.openlibrary.org/b/isbn/9780590353427-M.jpg",
        "description": (
            "A young wizard discovers his magical heritage and begins "
            "his journey at Hogwarts School of Witchcraft and Wizardry."
        ),
        "rating": 4.8,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "the-hobbit",
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
        "year": "1937",
        "pages": 310,
        "cover": "https://covers.openlibrary.org/b/isbn/9780547928227-M.jpg",
        "description": (
            "Bilbo Baggins joins a group of dwarves on an unexpected "
            "adventure to reclaim their homeland."
        ),
        "rating": 4.7,
        "hot": True,
        "recommended": False,
    },
    {
        "id": "deep-work",
        "title": "Deep Work",
        "author": "Cal Newport",
        "category": "Productivity",
        "year": "2016",
        "pages": 296,
        "cover": "https://covers.openlibrary.org/b/isbn/9781455586691-M.jpg",
        "description": (
            "A guide to developing the ability to focus without distraction "
            "and produce meaningful work in an increasingly distracted world."
        ),
        "rating": 4.5,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "the-power-of-now",
        "title": "The Power of Now",
        "author": "Eckhart Tolle",
        "category": "Self-help",
        "year": "1997",
        "pages": 236,
        "cover": "https://covers.openlibrary.org/b/isbn/9781577314806-M.jpg",
        "description": (
            "A spiritual guide focused on living in the present moment "
            "and developing greater awareness of everyday life."
        ),
        "rating": 4.5,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "sapiens",
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "category": "History",
        "year": "2011",
        "pages": 498,
        "cover": "https://covers.openlibrary.org/b/isbn/9780062316097-M.jpg",
        "description": (
            "A broad history of humankind exploring how Homo sapiens "
            "developed societies, cultures, and systems of belief."
        ),
        "rating": 4.6,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "educated",
        "title": "Educated",
        "author": "Tara Westover",
        "category": "Memoir",
        "year": "2018",
        "pages": 334,
        "cover": "https://covers.openlibrary.org/b/isbn/9780399590504-M.jpg",
        "description": (
            "A memoir about education, family, identity, and the journey "
            "of building a new life through learning."
        ),
        "rating": 4.6,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "the-midnight-library",
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "category": "Fantasy",
        "year": "2020",
        "pages": 304,
        "cover": "https://covers.openlibrary.org/b/isbn/9780525559474-M.jpg",
        "description": (
            "A novel about regret, possibility, and the lives we might "
            "have lived if we had made different choices."
        ),
        "rating": 4.3,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "normal-people",
        "title": "Normal People",
        "author": "Sally Rooney",
        "category": "Romance",
        "year": "2018",
        "pages": 273,
        "cover": "https://covers.openlibrary.org/b/isbn/9780571334650-M.jpg",
        "description": (
            "A contemporary story about relationships, friendship, "
            "communication, and growing up."
        ),
        "rating": 4.2,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "the-four-agreements",
        "title": "The Four Agreements",
        "author": "Don Miguel Ruiz",
        "category": "Self-help",
        "year": "1997",
        "pages": 160,
        "cover": "https://covers.openlibrary.org/b/isbn/9781878424310-M.jpg",
        "description": (
            "A practical guide built around four principles for personal "
            "freedom, happiness, and better relationships."
        ),
        "rating": 4.5,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "ikigai",
        "title": "Ikigai",
        "author": "Héctor García & Francesc Miralles",
        "category": "Lifestyle",
        "year": "2016",
        "pages": 208,
        "cover": "https://covers.openlibrary.org/b/isbn/9780143130727-M.jpg",
        "description": (
            "An introduction to the Japanese concept of ikigai and ideas "
            "for finding meaning, purpose, and balance in everyday life."
        ),
        "rating": 4.3,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "to-kill-a-mockingbird",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Classic",
        "year": "1960",
        "pages": 336,
        "cover": "https://covers.openlibrary.org/b/isbn/9780061120084-M.jpg",
        "description": (
            "A coming-of-age story that explores justice, empathy, "
            "prejudice, and morality in a small Southern town."
        ),
        "rating": 4.8,
        "hot": True,
        "recommended": False,
    },
    {
        "id": "pride-and-prejudice",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": "Romance",
        "year": "1813",
        "pages": 279,
        "cover": "https://covers.openlibrary.org/b/isbn/9780141439518-M.jpg",
        "description": (
            "A classic romance following Elizabeth Bennet as she navigates "
            "family, social expectations, misunderstanding, and love."
        ),
        "rating": 4.7,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "the-hunger-games",
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "category": "Young Adult",
        "year": "2008",
        "pages": 374,
        "cover": "https://covers.openlibrary.org/b/isbn/9780439023481-M.jpg",
        "description": (
            "In a dystopian society, Katniss Everdeen is forced to compete "
            "in a televised fight for survival."
        ),
        "rating": 4.6,
        "hot": True,
        "recommended": False,
    },
    {
        "id": "the-book-thief",
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "category": "Historical Fiction",
        "year": "2005",
        "pages": 552,
        "cover": "https://covers.openlibrary.org/b/isbn/9780375842207-M.jpg",
        "description": (
            "A moving story set in Nazi Germany about a young girl, "
            "books, friendship, and the power of words."
        ),
        "rating": 4.7,
        "hot": True,
        "recommended": True,
    },
    {
        "id": "the-7-habits",
        "title": "The 7 Habits of Highly Effective People",
        "author": "Stephen R. Covey",
        "category": "Self-help",
        "year": "1989",
        "pages": 464,
        "cover": "https://covers.openlibrary.org/b/isbn/9781982137274-M.jpg",
        "description": (
            "A classic personal development book presenting principles "
            "for becoming more effective in work and everyday life."
        ),
        "rating": 4.5,
        "hot": False,
        "recommended": True,
    },
    {
        "id": "thinking-fast-and-slow",
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "category": "Psychology",
        "year": "2011",
        "pages": 499,
        "cover": "https://covers.openlibrary.org/b/isbn/9780374533557-M.jpg",
        "description": (
            "An exploration of the two systems that shape human thinking "
            "and how they influence judgment and decision-making."
        ),
        "rating": 4.4,
        "hot": False,
        "recommended": True,
    },
]