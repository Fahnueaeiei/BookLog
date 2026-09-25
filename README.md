# BookLog

BookLog is a Python application that helps readers find books, build a personal library, and track their reading. Search for books with the Google Books API, save them to your library, mark them as *Want to Read*, *Reading*, or *Completed*, add ratings and notes, and search, filter, and sort your collection. Everything is stored in SQLite, so your library is still there next time.

Final project for **CP352301 Script Programming** (Semester 1/2569).

## Features

- **Search books** by title, author, or genre (Google Books API)
- **Book details:** title, author, description, published date, categories, cover
- **My Library:** add and remove books, saved locally
- **Reading tracker:** Want to Read / Reading / Completed, with reading progress
- **Rating and notes** for each book
- **Search, filter, and sort** your library (by status, category, rating, published year, and more)
- **SQLite persistence** for your library and reading data
- **Web interface** (Streamlit) and a CLI

## Tech Stack

- Python 3.10+
- Google Books API (`requests`)
- SQLite (`sqlite3`)
- Streamlit (web app, Sprint 3)
- pytest, ruff, GitHub Actions (Final Sprint)

## Architecture

The application is split into three layers:

```text
Presentation Layer    CLI  →  Streamlit web app
Business Logic Layer  BookFinder · Library · ReadingTracker · models · exceptions
Data Access Layer     DataStore (SQLite) · Google Books API
```

See [PLAN.md](PLAN.md) for the full design, class diagram, database schema, and Definition of Done.

## Project Structure

```text
book-library-manager/
├── README.md
├── PLAN.md                # project plan for the whole project
├── requirements.txt
├── Sprint1/               # CLI front-end with mock data
├── Sprint2/               # back-end: business logic, SQLite, search/filter/sort
├── Sprint3/               # full-stack web app
└── .github/workflows/     # CI (Final Sprint)
```

Each `SprintN/` folder is a runnable snapshot of the project at the end of that sprint and contains its own `CHANGELOG.md` and sprint report (with the retrospective).

## Sprint Status

| Sprint | Focus | Status | Changelog | Report |
|---|---|---|---|---|
| Sprint 1 | Plan + CLI front-end | Finished | [CHANGELOG](Sprint1/CHANGELOG.md) | [Report](Sprint1/Sprint1_Report.md) |
| Sprint 2 | Back-end (business logic, SQLite, search/filter/sort, Google Books) | In progress  | [CHANGELOG](Sprint2/CHANGELOG.md) | [Report](Sprint2/Sprint2_Report.md) |
| Sprint 3 | Full-stack web app | Planned | [CHANGELOG](Sprint3/CHANGELOG.md) | [Report](Sprint3/Sprint3_Report.md) |
| Final Sprint | Automated tests, CI/CD, AI feature | Planned | — | — |

## Getting Started

The commands below work once the matching sprint is finished.

### Install

```bash
git clone https://github.com/Fahnueaeiei/Booklog.git
cd Booklog
pip install -r requirements.txt
```

### Run

```bash
# Sprint 1: CLI with mock data
cd Sprint1
python main.py

# Sprint 2: back-end (CLI connected to the back-end)
cd Sprint2
python main.py

# Sprint 3: web app
cd Sprint3
streamlit run app.py
```

### Run the tests

```bash
cd Sprint2
pytest
```

### Configuration

The Google Books API can be used without a key for light use. If you have an API key, set it as an environment variable instead of writing it in the code:

```bash
export GOOGLE_BOOKS_API_KEY="your-key"      # macOS / Linux
setx GOOGLE_BOOKS_API_KEY "your-key"        # Windows
```

The SQLite database file is created automatically the first time the app runs.

## Documentation

- [PLAN.md](PLAN.md) — project plan, architecture, UML, schema, Definition of Done
- `SprintN/SprintN_Report.md` — progress, QA log, and retrospective (Wow! / Whoops!) for each sprint
- `SprintN/CHANGELOG.md` — what changed in each sprint

## Team

- Phattharawadee Songsrirod
- Sujeephon Poobanchuen

Sprint 1: Phattharawadee Songsrirod (Planner), Sujeephon Poobanchuen (Coder/Debugger). From Sprint 2 onward, both members work as Coder and Debugger. Details are recorded in each sprint report.