"""Generate data/seed_books.json for Sprint 2 performance testing.

Not part of the application itself — this is a one-off dev script used
to build a large (hundreds of books), realistically messy dataset for
measuring Library.search/filter/sort performance and for exercising
DataStore with more than a handful of rows.

Run from the Sprint2 folder:

    python generate_seed_data.py

Uses a fixed random seed, so running it again reproduces the exact
same file.
"""

import json
import random

SEED = 42
BOOK_COUNT = 300
OUTPUT_PATH = "data/seed_books.json"

GENRES = [
    "Science Fiction", "Fantasy", "Mystery", "Romance", "Thriller",
    "Horror", "Classics", "Biography", "History", "Self-Help",
    "Poetry", "Young Adult", "Fiction", "Non-Fiction", "Adventure",
]

TITLE_PARTS_A = [
    "The Silent", "A Quiet", "The Last", "Beyond the", "The Hidden",
    "Whispers of", "The Broken", "Shadows of", "The Forgotten",
    "Echoes of", "The Distant", "A Winter's", "The Golden",
    "Fragments of", "The Long",
]
TITLE_PARTS_B = [
    "River", "Garden", "Horizon", "Kingdom", "Letter", "Storm",
    "Mountain", "City", "Ocean", "Forest", "Star", "Promise",
    "Journey", "Mirror", "Road",
]

FIRST_NAMES = [
    "Alex", "Maria", "James", "Priya", "Noah", "Elena", "Kenji",
    "Fatima", "Liam", "Sofia", "Omar", "Grace", "Lucas", "Amara",
    "Ivan",
]
LAST_NAMES = [
    "Carter", "Nguyen", "Okafor", "Rossi", "Lindqvist", "Silva",
    "Kowalski", "Haddad", "Torres", "Kim", "Novak", "Andersen",
    "Mensah", "Petrov", "Ahmed",
]

DESCRIPTION_TEMPLATES = [
    "A story about {genre_lower} that follows one character's search "
    "for meaning against the odds.",
    "This {genre_lower} novel explores family, memory, and the choices "
    "that define a life.",
    "A tightly plotted {genre_lower} tale set across three generations "
    "of one household.",
    "Part {genre_lower}, part meditation on loss, this book lingers "
    "long after the last page.",
]


def make_published_date(rng):
    """Return a published date in one of the three supported formats,
    or None (about 5% of the time) to simulate missing data.
    """
    if rng.random() < 0.05:
        return None

    year = rng.randint(1920, 2025)
    date_format = rng.choice(["year", "year_month", "full_date"])

    if date_format == "year":
        return str(year)
    if date_format == "year_month":
        return f"{year}-{rng.randint(1, 12):02d}"
    return f"{year}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"


def make_book(index, rng):
    """Build one seed book record as a plain dict (matches Book fields)."""
    title = f"{rng.choice(TITLE_PARTS_A)} {rng.choice(TITLE_PARTS_B)}"
    author_count = rng.choice([1, 1, 1, 2])  # mostly single-author
    authors = [
        f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        for _ in range(author_count)
    ]

    genre_count = rng.choice([1, 1, 2])
    categories = rng.sample(GENRES, genre_count)

    has_description = rng.random() >= 0.10  # ~10% missing
    has_cover = rng.random() >= 0.10  # ~10% missing
    has_page_count = rng.random() >= 0.05  # ~5% missing

    return {
        "book_id": f"seed-{index:04d}",
        "title": title,
        "authors": authors,
        "description": (
            DESCRIPTION_TEMPLATES[index % len(DESCRIPTION_TEMPLATES)].format(
                genre_lower=categories[0].lower()
            )
            if has_description
            else None
        ),
        "published_date": make_published_date(rng),
        "categories": categories,
        "cover_url": (
            f"https://example.com/covers/seed-{index:04d}.jpg"
            if has_cover
            else None
        ),
        "page_count": rng.randint(80, 900) if has_page_count else None,
    }


def main():
    """Generate BOOK_COUNT seed books and write them to OUTPUT_PATH."""
    rng = random.Random(SEED)
    books = [make_book(i, rng) for i in range(1, BOOK_COUNT + 1)]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)

    print(f"Wrote {len(books)} books to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()