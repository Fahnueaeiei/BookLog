import sys
from pathlib import Path

import streamlit as st


# =========================================================
# Import Service
# =========================================================

CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from service import (
    search_books,
    get_book_details,
    get_library_books,
    get_home_books,
    add_to_library,
    remove_from_library,
    update_status,
    update_progress,
    update_rating,
    update_note,
    browse_books,  
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="BookLog",
    page_icon="📚",
    layout="wide",
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;500;600;700&display=swap');

    html,
    body,
    .stApp,
    .stApp *:not([data-testid="stIconMaterial"])
    :not([class*="material-icons"])
    :not([class*="material-symbols"]) {
        font-family: 'Lato', sans-serif;
    }

    [data-testid="stIconMaterial"],
    span[class*="material-icons"],
    span[class*="material-symbols"] {
        font-family: 'Material Symbols Rounded',
        'Material Icons' !important;
    }


    /* -------------------------------------------------
       App
    ------------------------------------------------- */

    .stApp {
        background-color: #FAF8F4;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }


    /* -------------------------------------------------
       Top Navigation
    ------------------------------------------------- */

    .st-key-topnav {
        background: #FFFFFF;
        padding: 0.45rem 0;
        margin-bottom: 1.6rem;
        box-shadow: 0 0 0 100vmax #FFFFFF;
        clip-path: inset(0 -100vmax);
    }

    .logo {
        font-size: 27px;
        font-weight: 700;
        color: #382F29;
        letter-spacing: -0.7px;
        white-space: nowrap;
    }

    div[class*="st-key-nav_"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #493D34 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.2rem !important;
        min-height: 40px !important;
        justify-content: center !important;
    }

    div[class*="st-key-nav_"] button p {
        white-space: nowrap !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    div[class*="st-key-nav_"] button:hover {
        background: transparent !important;
        color: #8B735F !important;
    }


    /* -------------------------------------------------
       Search
    ------------------------------------------------- */

    .st-key-topnav [data-baseweb="input"],
    .st-key-topnav [data-baseweb="base-input"] {
        background: #FFFFFF !important;
        border-radius: 4px !important;
    }

    .st-key-topnav [data-testid="stTextInput"] [data-baseweb="input"] {
        border: 1px solid #D6D1CB !important;
        min-height: 40px !important;
    }

    .st-key-topnav [data-testid="stTextInput"]
    [data-baseweb="input"]:focus-within {
        border-color: #A99B8E !important;
        box-shadow: 0 0 0 1px #A99B8E !important;
    }

    .st-key-topnav input {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        color: #3F3933 !important;
        font-size: 15px !important;
    }


    /* -------------------------------------------------
       Main Headings
    ------------------------------------------------- */

    h1 {
        color: #3F3933;
        font-size: 36px !important;
        margin-bottom: 8px;
    }

    h2,
    h3 {
        color: #3F3933;
    }


    /* -------------------------------------------------
       Description
    ------------------------------------------------- */

    .description {
        color: #756C63;
        font-size: 15px;
        line-height: 1.6;
    }


    /* -------------------------------------------------
       General Buttons
    ------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        border: none;
        background-color: #8B735F;
        color: #FFFFFF;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
    }

    .stButton > button:hover {
        background-color: #6F5A49;
        color: #FFFFFF;
    }


    /* -------------------------------------------------
       Section Titles
    ------------------------------------------------- */

    .section-title {
        font-size: 22px;
        font-weight: 650;
        color: #3F3933;
        margin-top: 34px;
        margin-bottom: 15px;
    }

    .section-subtitle {
        color: #8A8076;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 16px;
    }


    /* -------------------------------------------------
       Home Greeting
    ------------------------------------------------- */

    .greeting {
        margin-top: 26px;
        margin-bottom: 8px;
        font-size: 27px;
        font-weight: 650;
        color: #3F3933;
    }

    .greeting-text {
        font-size: 15px;
        color: #756C63;
        margin-bottom: 28px;
    }


    /* -------------------------------------------------
       Book Cards
    ------------------------------------------------- */

    .book-card {
        width: 100%;
    }

    .book-cover-wrapper {
        width: 100%;
        height: 270px;
        overflow: hidden;
        border-radius: 8px;
        background-color: #EAE2D8;
    }

    .book-cover-wrapper img {
        width: 100%;
        height: 270px;
        object-fit: cover;
        display: block;
    }

    .book-title {
        font-size: 16px;
        font-weight: 650;
        color: #3F3933;
        margin-top: 10px;
        line-height: 1.35;
        min-height: 43px;
    }

    .book-author {
        font-size: 13px;
        color: #756C63;
        margin-top: 4px;
        min-height: 20px;
    }

    .book-meta {
        font-size: 12px;
        color: #9A9086;
        margin-top: 7px;
        margin-bottom: 9px;
        min-height: 18px;
    }


    /* -------------------------------------------------
       Continue Reading
    ------------------------------------------------- */

    .reading-progress-text {
        font-size: 12px;
        color: #756C63;
        margin-top: 5px;
    }


    /* -------------------------------------------------
       Book Detail
    ------------------------------------------------- */

    .detail-title {
        font-size: 34px;
        font-weight: 700;
        color: #3F3933;
        line-height: 1.25;
        margin-bottom: 6px;
    }

    .detail-author {
        font-size: 17px;
        color: #756C63;
        margin-bottom: 20px;
    }

    .about-title {
        font-size: 20px;
        font-weight: 650;
        color: #3F3933;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .about-text {
        font-size: 15px;
        color: #655D56;
        line-height: 1.7;
    }

    .detail-label {
        font-size: 13px;
        color: #9A9086;
        margin-bottom: 3px;
    }

    .detail-value {
        font-size: 15px;
        color: #514A44;
        margin-bottom: 13px;
    }

    .detail-cover img {
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(80, 62, 48, 0.14);
    }


    /* -------------------------------------------------
       Back Button
    ------------------------------------------------- */

    .back-button {
        margin-bottom: 20px;
    }

    .back-button .stButton > button {
        background-color: transparent;
        color: #756C63;
        border: none;
        padding: 0;
        font-size: 25px;
        font-weight: 400;
        width: auto;
    }

    .back-button .stButton > button:hover {
        background-color: transparent;
        color: #3F3933;
    }


    /* -------------------------------------------------
       Rating
    ------------------------------------------------- */

    .rating-title {
        font-size: 15px;
        font-weight: 600;
        color: #554C44;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    div[class*="st-key-rating_star_"] {
        width: auto !important;
    }

    div[class*="st-key-rating_star_"] button {
        background: transparent !important;
        justify-content: center !important;
        border: 0 !important;
        box-shadow: none !important;
        color: #D2C7BB !important;
        font-size: 30px !important;
        line-height: 1 !important;
        min-height: 0 !important;
        padding: 0 !important;
        width: auto !important;
    }

    div[class*="st-key-rating_star_"] button:hover {
        background: transparent !important;
        color: #8B735F !important;
    }

    div[class*="st-key-rating_star_active_"] button {
        color: #8B735F !important;
    }


    /* -------------------------------------------------
       Library
    ------------------------------------------------- */

    .library-count {
        font-size: 14px;
        color: #8A8076;
        margin-bottom: 20px;
    }

    .book-title {
        font-size: 16px;
        font-weight: 650;
        color: #3F3933;
        margin-top: 10px;

        /* ความสูงเท่ากันทุกการ์ด */
        height: 43px;

        /* ตัดข้อความเกิน 2 บรรทัด */
        overflow: hidden;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        line-clamp: 2;

        /* แสดง ... */
        text-overflow: ellipsis;

        line-height: 1.35;
    }


    .book-author {
        font-size: 13px;
        color: #756C63;
        margin-top: 4px;

        /* ความสูงเท่ากัน */
        height: 20px;

        /* ถ้ายาวให้ ... */
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }


    .book-meta {
        font-size: 12px;
        color: #9A9086;
        margin-top: 7px;
        margin-bottom: 9px;

        /* ความสูงเท่ากัน */
        height: 18px;

        /* ถ้ายาวให้ ... */
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    .library-meta {
        height: 24px;
        line-height: 24px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-size: 13px;
        color: #8C8177;
    }

    .library-meta-empty {
        visibility: hidden;
    }

    .library-progress-text {
        height: 24px;
        line-height: 24px;
        font-size: 13px;
        color: #8C8177;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Session State
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "detail_source" not in st.session_state:
    st.session_state.detail_source = "Home"

if "nav_search_input" not in st.session_state:
    st.session_state.nav_search_input = ""


# =========================================================
# Helper Functions
# =========================================================

def get_library_book(book_id):
    """Get one book from the real Sprint 2 library."""
    library_books = get_library_books()

    for book in library_books:
        if book["id"] == book_id:
            return book

    return None


def is_in_library(book_id):
    """Check whether a book exists in the real library."""
    return get_library_book(book_id) is not None


def open_book(book, source="Home"):
    """Open Book Detail."""
    try:
        detailed_book = get_book_details(book["id"])
    except Exception:
        detailed_book = book

    st.session_state.selected_book = detailed_book
    st.session_state.detail_source = source
    st.session_state.page = "Book Detail"
    st.rerun()


def render_book_card(book, key_prefix, source):
    """Render a book card using real backend data."""

    cover = book.get("cover", "")
    title = book.get("title", "Untitled")
    author = book.get("author", "Unknown Author")
    category = book.get("category", "Uncategorized")
    year = book.get("year", "Unknown")

    # -----------------------------------------------------
    # Book Cover
    # -----------------------------------------------------
    if cover:
        st.markdown(
            f"""
            <div class="book-cover-wrapper">
                <img src="{cover}" alt="{title}">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="book-cover-wrapper">
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    height:270px;
                    color:#8C8177;
                    font-size:14px;
                ">
                    No Cover
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # Book Information
    # -----------------------------------------------------
    st.markdown(
        f"""
        <div class="book-title">
            {title}
        </div>

        <div class="book-author">
            {author}
        </div>

        <div class="book-meta">
            {category} · {year}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # View Details
    # -----------------------------------------------------
    if st.button(
        "View Details",
        key=f"{key_prefix}_{book['id']}",
        width="stretch",
    ):
        open_book(book, source)


def render_book_grid(books, key_prefix, source="Home"):
    """Render books in horizontal cards."""

    grid = st.container(
        horizontal=True,
        gap="medium",
    )

    with grid:
        for index, book in enumerate(books):
            with st.container(width=180):
                render_book_card(
                    book,
                    f"{key_prefix}_{index}",
                    source,
                )


def clear_search():
    """Clear search state."""

    st.session_state.search_query = ""
    st.session_state.search_results = []
    st.session_state.nav_search_input = ""


def run_nav_search():
    """Run search from the top navigation."""

    text = st.session_state.get(
        "nav_search_input",
        "",
    ).strip()

    st.session_state.search_query = text

    if text:
        try:
            st.session_state.search_results = search_books(text)
        except Exception as e:
            st.session_state.search_results = []
            st.session_state.search_error = str(e)
    else:
        st.session_state.search_results = []

    st.session_state.page = "Home"
    st.session_state.selected_book = None


# =========================================================
# Top Navigation
# =========================================================

with st.container(key="topnav"):

    nav_logo, nav_home, nav_books, nav_browse, nav_search = st.columns(
        [2.0, 0.75, 0.95, 0.9, 3.4],
        gap="small",
        vertical_alignment="center",
    )

    # -------------------------------------------------
    # Logo
    # -------------------------------------------------

    with nav_logo:
        st.markdown(
            '<div class="logo">📚 BookLog</div>',
            unsafe_allow_html=True,
        )

    # -------------------------------------------------
    # Home
    # -------------------------------------------------

    with nav_home:
        if st.button(
            "Home",
            key="nav_home",
            width="stretch",
        ):
            st.session_state.page = "Home"
            st.session_state.selected_book = None
            clear_search()
            st.rerun()

    # -------------------------------------------------
    # My Books
    # -------------------------------------------------

    with nav_books:
        if st.button(
            "My Books",
            key="nav_books",
            width="stretch",
        ):
            st.session_state.page = "Library"
            st.session_state.selected_book = None
            clear_search()
            st.rerun()

    # -------------------------------------------------
    # Browse
    # -------------------------------------------------

    with nav_browse:
        if st.button(
            "Browse",
            key="nav_browse",
            width="stretch",
        ):
            st.session_state.page = "Browse"
            st.session_state.selected_book = None
            clear_search()
            st.rerun()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    with nav_search:
        try:
            st.text_input(
                "Search",
                key="nav_search_input",
                placeholder="Search books",
                label_visibility="collapsed",
                icon=":material/search:",
                on_change=run_nav_search,
            )
        except TypeError:
            st.text_input(
                "Search",
                key="nav_search_input",
                placeholder="Search books",
                label_visibility="collapsed",
                on_change=run_nav_search,
            )

# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    # -----------------------------------------------------
    # Greeting
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="greeting">
            Find a book worth reading.
        </div>

        <div class="greeting-text">
            Search for books and keep track of your reading journey.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # Search Results
    # -----------------------------------------------------

    if st.session_state.get("search_results"):

        st.markdown(
            '<div class="section-title">Search Results</div>',
            unsafe_allow_html=True,
        )

        render_book_grid(
            st.session_state.search_results,
            "search",
            "Home",
        )

        st.markdown("---")

    elif (
        st.session_state.get("search_query")
        and not st.session_state.get("search_results")
    ):

        st.info(
            f'No books found for "{st.session_state.search_query}".'
        )


    # -----------------------------------------------------
    # Continue Reading
    # -----------------------------------------------------

    library_books = get_library_books()

    reading_books = [
        book
        for book in library_books
        if book["status"] == "Reading"
    ]

    if reading_books:

        st.markdown(
            '<div class="section-title">Continue Reading</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-subtitle">
                Pick up where you left off.
            </div>
            """,
            unsafe_allow_html=True,
        )

        reading_container = st.container(
            horizontal=True,
            gap="medium",
        )

        with reading_container:

            for book in reading_books[:5]:

                with st.container(width=180):

                    cover = book.get("cover", "")

                    if cover:
                        st.markdown(
                            f"""
                            <div class="book-cover-wrapper">
                                <img
                                    src="{cover}"
                                    alt="{book["title"]}"
                                >
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            """
                            <div class="book-cover-wrapper">
                                <div style="
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    height:270px;
                                    color:#8C8177;
                                ">
                                    No Cover
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        f"""
                        <div class="book-title">
                            {book["title"]}
                        </div>

                        <div class="book-author">
                            {book["author"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    progress = book["progress"]

                    st.progress(
                        progress / 100,
                        text=f"{progress}% complete",
                    )

                    if st.button(
                        "Continue Reading",
                        key=f"continue_{book['id']}",
                        width="stretch",
                    ):
                        open_book(
                            book,
                            "Home",
                        )


        home_books = get_home_books()

        st.subheader("Discover Books")

        if home_books:
            cols = st.columns(5)

            for i, book in enumerate(home_books):
                with cols[i % 5]:
                    render_book_card(
                        book,
                        f"home_{i}",
                        "Home",
                    )
        else:
            st.info("No books available.")

# =========================================================
# BOOK DETAIL
# =========================================================

elif st.session_state.page == "Book Detail":

    book = st.session_state.selected_book


    # -----------------------------------------------------
    # Back Button
    # -----------------------------------------------------

    st.markdown(
        '<div class="back-button">',
        unsafe_allow_html=True,
    )

    if st.button(
        "←",
        type="secondary",
    ):

        previous_page = st.session_state.get(
            "detail_source",
            "Home",
        )

        st.session_state.page = previous_page
        st.session_state.selected_book = None
        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    if book is None:

        st.warning("No book selected.")

    else:

        # -------------------------------------------------
        # Get current library data
        # -------------------------------------------------

        user_data = get_library_book(
            book["id"]
        )

        in_library = user_data is not None


        # -------------------------------------------------
        # Detail Layout
        # -------------------------------------------------

        left, right = st.columns(
            [0.72, 2.28],
            gap="large",
        )


        # -------------------------------------------------
        # Cover
        # -------------------------------------------------

        with left:

            st.markdown(
                '<div class="detail-cover">',
                unsafe_allow_html=True,
            )

            if book.get("cover"):

                st.image(
                    book["cover"],
                    width=260,
                )

            else:

                st.info(
                    "No cover available."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        # -------------------------------------------------
        # Information
        # -------------------------------------------------

        with right:

            st.markdown(
                f"""
                <div class="detail-title">
                    {book["title"]}
                </div>

                <div class="detail-author">
                    by {book["author"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


            # -------------------------------------------------
            # Book Information
            # -------------------------------------------------

            info_left, info_right = st.columns(
                [0.8, 2]
            )

            with info_left:

                st.markdown(
                    '<div class="detail-label">Category</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="detail-label">Published</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="detail-label">Pages</div>',
                    unsafe_allow_html=True,
                )

            with info_right:

                st.markdown(
                    f"""
                    <div class="detail-value">
                        {book["category"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="detail-value">
                        {book["year"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                total_pages = book.get("pages", 0)

                page_text = (
                    f"{total_pages} pages"
                    if total_pages
                    else "Unknown"
                )

                st.markdown(
                    f"""
                    <div class="detail-value">
                        {page_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # -------------------------------------------------
            # Description
            # -------------------------------------------------

            st.markdown(
                """
                <div class="about-title">
                    About this book
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="about-text">
                    {book["description"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")


            # -------------------------------------------------
            # Library Action
            # -------------------------------------------------

            if not in_library:

                if st.button(
                    "＋ Add to Library",
                    key=f"add_{book['id']}",
                    width="stretch",
                ):

                    try:

                        add_to_library(book)

                        st.success(
                            "Book added to your library."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not add book: {e}"
                        )

                st.info(
                    "Add this book to your library to start "
                    "tracking your reading."
                )

                st.stop()


            # -------------------------------------------------
            # Remove from Library
            # -------------------------------------------------

            if st.button(
                "Remove from Library",
                key=f"remove_{book['id']}",
                width="stretch",
            ):

                try:

                    remove_from_library(
                        book["id"]
                    )

                    st.success(
                        "Book removed from your library."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not remove book: {e}"
                    )


            # -------------------------------------------------
            # Reading Status
            # -------------------------------------------------

            st.markdown(
                """
                <div class="section-title">
                    Reading Status
                </div>
                """,
                unsafe_allow_html=True,
            )

            status_options = [
                "Want to Read",
                "Reading",
                "Completed",
            ]

            current_status = user_data["status"]

            selected_status = st.segmented_control(
                "Reading Status",
                status_options,
                default=current_status,
                label_visibility="collapsed",
                key=f"status_{book['id']}",
            )

            if selected_status:

                if selected_status != current_status:

                    try:

                        update_status(
                            book["id"],
                            selected_status,
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not update status: {e}"
                        )


            # -------------------------------------------------
            # Progress
            # -------------------------------------------------

            st.markdown(
                """
                <div class="rating-title">
                    Reading Progress
                </div>
                """,
                unsafe_allow_html=True,
            )


            # Unknown page count
            if not total_pages:

                st.info(
                    "Page count is unavailable for this book."
                )

                progress = user_data["progress"]

                st.progress(
                    progress / 100,
                    text=f"{progress}% complete",
                )


            else:

                current_pages = round(
                    user_data["progress"]
                    * total_pages
                    / 100
                )

                if selected_status == "Want to Read":

                    current_pages = 0

                elif selected_status == "Completed":

                    current_pages = total_pages

                else:

                    current_pages = st.slider(
                        "Pages read",
                        min_value=0,
                        max_value=total_pages,
                        value=current_pages,
                        step=1,
                        label_visibility="collapsed",
                        key=f"progress_{book['id']}",
                    )


                progress = round(
                    current_pages
                    / total_pages
                    * 100
                )


                # Update only when the value changed
                old_pages = round(
                    user_data["progress"]
                    * total_pages
                    / 100
                )

                if current_pages != old_pages:

                    try:

                        update_progress(
                            book["id"],
                            current_pages,
                        )

                    except Exception as e:

                        st.error(
                            f"Could not update progress: {e}"
                        )


                st.progress(
                    progress / 100,
                    text=(
                        f"{current_pages} of "
                        f"{total_pages} pages · "
                        f"{progress}%"
                    ),
                )


            # -------------------------------------------------
            # Personal Rating
            # -------------------------------------------------

            st.markdown(
                """
                <div class="rating-title">
                    Your Rating
                </div>
                """,
                unsafe_allow_html=True,
            )

            current_rating = user_data["rating"]

            star_columns = st.columns(
                [0.35] * 5 + [4],
                gap="small",
            )[:5]

            for value, column in enumerate(
                star_columns,
                start=1,
            ):

                active = value <= current_rating

                star = (
                    "★"
                    if active
                    else "☆"
                )

                key_prefix = (
                    "rating_star_active"
                    if active
                    else "rating_star"
                )

                with column:

                    if st.button(
                        star,
                        key=(
                            f"{key_prefix}_"
                            f"{book['id']}_"
                            f"{value}"
                        ),
                        type="tertiary",
                    ):

                        try:

                            update_rating(
                                book["id"],
                                value,
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Could not update rating: {e}"
                            )

            if current_rating > 0:

                st.caption(
                    f"You rated this book "
                    f"{current_rating} / 5"
                )

            else:

                st.caption(
                    "Not rated yet"
                )


            # -------------------------------------------------
            # Personal Note
            # -------------------------------------------------

            st.markdown(
                """
                <div class="rating-title">
                    Personal Note
                </div>
                """,
                unsafe_allow_html=True,
            )

            note = st.text_area(
                "Personal Note",
                value=user_data["note"],
                placeholder="Write something about this book...",
                height=110,
                key=f"note_{book['id']}",
                label_visibility="collapsed",
            )

            if note != user_data["note"]:

                try:

                    update_note(
                        book["id"],
                        note,
                    )

                except Exception as e:

                    st.error(
                        f"Could not save note: {e}"
                    )

            st.caption(
                "Your note is private and only used "
                "for your personal reading record."
            )


# =========================================================
# MY LIBRARY
# =========================================================

elif st.session_state.page == "Library":

    st.title("My Books")

    st.markdown(
        """
        <p class="description">
            Keep your books organized and track your reading journey.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Load Library
    # -----------------------------------------------------

    library_books = get_library_books()
    total_books = len(library_books)

    st.markdown(
        f"""
        <div class="library-count">
            {total_books} book
            {"s" if total_books != 1 else ""}
            in your library
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Empty Library
    # -----------------------------------------------------

    if not library_books:

        st.info(
            "Your library is empty. "
            "Search for books on Home and add something to your library."
        )

    else:

        # -------------------------------------------------
        # Status Tabs
        # -------------------------------------------------

        tab_all, tab_want, tab_reading, tab_completed = st.tabs(
            [
                "All",
                "Want to Read",
                "Reading",
                "Completed",
            ]
        )

        # =================================================
        # ALL
        # =================================================

        with tab_all:

            columns = st.columns(5)

            for index, book in enumerate(library_books):

                with columns[index % 5]:

                    render_book_card(
                        book,
                        f"library_all_{index}",
                        "Library",
                    )

                    # Status
                    st.markdown(
                        f"""
                        <div class="library-meta">
                            {book["status"]} · {book["progress"]}%
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Rating
                    if book["rating"] > 0:

                        st.markdown(
                            f"""
                            <div class="library-meta">
                                Your rating: {"★" * book["rating"]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            """
                            <div class="library-meta library-meta-empty">
                                &nbsp;
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # =================================================
        # WANT TO READ
        # =================================================

        with tab_want:

            books = [
                book
                for book in library_books
                if book["status"] == "Want to Read"
            ]

            if not books:

                st.info("No books in Want to Read.")

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_want_{index}",
                            "Library",
                        )

                        # Fixed meta area
                        st.markdown(
                            """
                            <div class="library-meta library-meta-empty">
                                &nbsp;
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown(
                            """
                            <div class="library-meta library-meta-empty">
                                &nbsp;
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # =================================================
        # READING
        # =================================================

        with tab_reading:

            books = [
                book
                for book in library_books
                if book["status"] == "Reading"
            ]

            if not books:

                st.info("No books currently being read.")

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_reading_{index}",
                            "Library",
                        )

                        # Status
                        st.markdown(
                            f"""
                            <div class="library-meta">
                                Reading · {book["progress"]}%
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Progress
                        st.progress(
                            min(max(book["progress"], 0), 100) / 100
                        )

                        st.markdown(
                            f"""
                            <div class="library-progress-text">
                                {book["progress"]}% completed
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # =================================================
        # COMPLETED
        # =================================================

        with tab_completed:

            books = [
                book
                for book in library_books
                if book["status"] == "Completed"
            ]

            if not books:

                st.info("No completed books yet.")

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_completed_{index}",
                            "Library",
                        )

                        # Status
                        st.markdown(
                            """
                            <div class="library-meta">
                                Completed · 100%
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Rating
                        if book["rating"] > 0:

                            st.markdown(
                                f"""
                                <div class="library-meta">
                                    Your rating: {"★" * book["rating"]}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        else:

                            st.markdown(
                                """
                                <div class="library-meta library-meta-empty">
                                    &nbsp;
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


# =================================================
# BROWSE
# =================================================

elif st.session_state.page == "Browse":

    st.title("Browse")

    st.markdown(
        """
        <p class="description">
            Explore books by category and discover something new.
        </p>
        """,
        unsafe_allow_html=True,
    )

    genres = [
        "Fiction",
        "Romance",
        "Mystery",
        "Fantasy",
        "Science",
        "History",
        "Business",
    ]

    selected_genre = st.selectbox(
        "Choose a category",
        genres,
    )

    books = browse_books(selected_genre)

    if not books:
        st.info("No books found in this category.")

    else:
        columns = st.columns(5)

        for index, book in enumerate(books):

            with columns[index % 5]:

                render_book_card(
                    book,
                    f"browse_{selected_genre}_{index}",
                    "Browse",
                )