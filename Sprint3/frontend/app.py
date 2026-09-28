import streamlit as st

from sprint3.frontend.src.mock_data import mock_books


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
        .stApp * {
            font-family: 'Lato', sans-serif;
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

    .top-nav {
        padding-top: 0.8rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #E5DED5;
        margin-bottom: 2.2rem;
    }

    .nav-wrapper {
        padding-top: 1rem;
        padding-bottom: 0.3rem;
    }

    .logo {
        font-size: 25px;
        font-weight: 700;
        color: #3F3933;
        padding-top: 8px;
    }

    .logo-subtitle {
        font-size: 12px;
        color: #8C8177;
        margin-top: -3px;
    }


    /* -------------------------------------------------
       Navigation Radio
    ------------------------------------------------- */

    div[data-testid="stRadio"] {
        margin-top: 5px;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 8px;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        border-radius: 9px;
        padding: 8px 16px;
        margin: 0;
        cursor: pointer;
        background-color: transparent;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #F1EBE3;
    }

    div[data-testid="stRadio"]
    div[role="radiogroup"]
    > label[data-checked="true"] {
        background-color: #E5D8CB;
    }

    /* Remove radio bullet */
    div[data-testid="stRadio"] input {
        display: none !important;
    }

    div[data-testid="stRadio"]
    div[role="radiogroup"]
    > label
    > div:first-child {
        display: none !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stRadio"]
    div[role="radiogroup"]
    > label p {
        font-size: 14px;
        font-weight: 600;
        color: #554C44;
        margin: 0;
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

    .star-button .stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #D2C7BB !important;
        font-size: 30px !important;
        padding: 0 !important;
        line-height: 1 !important;
    }

    .star-button .stButton > button:hover {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #8B735F !important;
    }

    .star-active .stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #8B735F !important;
        font-size: 30px !important;
        padding: 0 !important;
        line-height: 1 !important;
    }

    .star-active .stButton > button:hover {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #6F5A49 !important;
    }


    /* -------------------------------------------------
       Library
    ------------------------------------------------- */

    .library-count {
        font-size: 14px;
        color: #8A8076;
        margin-bottom: 20px;
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

if "library" not in st.session_state:
    st.session_state.library = []

if "book_data" not in st.session_state:
    st.session_state.book_data = {}

if "detail_source" not in st.session_state:
    st.session_state.detail_source = "Home"


# =========================================================
# Helper Functions
# =========================================================

def get_book_user_data(book_id):
    """Return user-specific data for a book."""

    if book_id not in st.session_state.book_data:
        st.session_state.book_data[book_id] = {
            "status": "Want to Read",
            "progress": 0,
            "rating": 0,
            "note": "",
        }

    return st.session_state.book_data[book_id]


def is_in_library(book_id):
    """Check whether a book is already in My Library."""

    return any(
        book["id"] == book_id
        for book in st.session_state.library
    )


def open_book(book, source="Home"):
    """Open Book Detail and remember the source page."""

    st.session_state.selected_book = book
    st.session_state.detail_source = source
    st.session_state.page = "Book Detail"

    st.rerun()


def render_book_card(book, key_prefix, source):
    """Render a standard book card."""

    # Fixed-height cover area
    st.markdown(
        f"""
        <div class="book-cover-wrapper">
            <img src="{book["cover"]}" alt="{book["title"]}">
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

        <div class="book-meta">
            {book["category"]} · {book["year"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "View Details",
        key=f"{key_prefix}_{book['id']}",
        width="stretch",
    ):
        open_book(book, source)


# =========================================================
# Top Navigation
# =========================================================

st.markdown(
    '<div class="nav-wrapper">',
    unsafe_allow_html=True,
)

nav_left, nav_right = st.columns([2.5, 4])

with nav_left:
    st.markdown(
        """
        <div class="logo">📚 BookLog</div>
        <div class="logo-subtitle">
            Your personal reading space
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_right:
    current_nav = st.session_state.page

    if current_nav == "Book Detail":
        current_nav = st.session_state.get(
            "detail_source",
            "Home",
        )

    selected_nav = st.radio(
        "Navigation",
        ["Home", "Library"],
        index=["Home", "Library"].index(current_nav),
        horizontal=True,
        label_visibility="collapsed",
    )

    if selected_nav != current_nav:
        st.session_state.page = selected_nav
        st.session_state.selected_book = None
        st.rerun()

st.markdown(
    """
    </div>

    <div class="top-nav"></div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    search_col, button_col = st.columns([5, 1])

    with search_col:
        search_query = st.text_input(
            "Search Books",
            value=st.session_state.search_query,
            placeholder="Search by title, author, or genre...",
            label_visibility="collapsed",
        )

    with button_col:
        search_clicked = st.button(
            "Search",
            width="stretch",
        )

    if search_clicked:
        st.session_state.search_query = search_query.strip()

        if search_query.strip():
            query = search_query.lower().strip()

            results = [
                book
                for book in mock_books
                if (
                    query in book["title"].lower()
                    or query in book["author"].lower()
                    or query in book["category"].lower()
                )
            ]

            st.session_state.search_results = results

        else:
            st.session_state.search_results = []


    # -----------------------------------------------------
    # Greeting
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="greeting">
            Find a book worth reading.
        </div>

        <div class="greeting-text">
            Explore popular books, discover something new,
            and keep track of your reading journey.
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

        results = st.session_state.search_results

        columns = st.columns(5)

        for index, book in enumerate(results):

            with columns[index % 5]:

                render_book_card(
                    book,
                    f"search_{index}",
                    "Home",
                )

        st.markdown("---")


    elif (
        st.session_state.get("search_query")
        and not st.session_state.get("search_results")
    ):

        st.info(
            f'No books found for '
            f'"{st.session_state.search_query}".'
        )


    # -----------------------------------------------------
    # Continue Reading
    # -----------------------------------------------------

    reading_books = [
        book
        for book in st.session_state.library
        if get_book_user_data(book["id"])["status"]
        == "Reading"
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

            for index, book in enumerate(reading_books):

                with st.container(width=180):

                    # Fixed-size cover
                    st.markdown(
                        f"""
                        <div class="book-cover-wrapper">
                            <img
                                src="{book["cover"]}"
                                alt="{book["title"]}"
                            >
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

                    data = get_book_user_data(
                        book["id"]
                    )

                    st.progress(
                        data["progress"] / 100
                    )

                    st.markdown(
                        f"""
                        <div class="reading-progress-text">
                            {data["progress"]}% completed
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "Continue",
                        key=f"continue_{index}_{book['id']}",
                        width="stretch",
                    ):
                        open_book(
                            book,
                            "Home",
                        )


    # -----------------------------------------------------
    # Hot Hits
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Hot Hits</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Popular books worth checking out.
        </div>
        """,
        unsafe_allow_html=True,
    )

    hot_books = [
        book
        for book in mock_books
        if book.get("hot", False)
    ]

    hot_container = st.container(
        horizontal=True,
        gap="medium",
    )

    with hot_container:

        for index, book in enumerate(hot_books):

            with st.container(width=180):

                # Fixed-size cover
                st.markdown(
                    f"""
                    <div class="book-cover-wrapper">
                        <img
                            src="{book["cover"]}"
                            alt="{book["title"]}"
                        >
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

                    <div class="book-meta">
                        {book["category"]} · {book["year"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "View Details",
                    key=f"hot_{index}_{book['id']}",
                    width="stretch",
                ):
                    open_book(
                        book,
                        "Home",
                    )


    # -----------------------------------------------------
    # Recommended
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Recommended for You</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            A few books you might enjoy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    recommended_books = [
        book
        for book in mock_books
        if book.get("recommended", False)
    ]

    recommended_columns = st.columns(5)

    for index, book in enumerate(
        recommended_books[:10]
    ):

        with recommended_columns[index % 5]:

            render_book_card(
                book,
                f"recommended_{index}",
                "Home",
            )


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

        # Return to the exact page that opened this detail
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

        st.warning(
            "No book selected."
        )

    else:

        user_data = get_book_user_data(
            book["id"]
        )


        # -------------------------------------------------
        # Detail Layout
        # -------------------------------------------------

        left, right = st.columns(
            [1, 2.2],
            gap="large",
        )


        # -------------------------------------------------
        # Cover
        # -------------------------------------------------

        with left:

            st.image(
                book["cover"],
                width="stretch",
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
                    f'<div class="detail-value">'
                    f'{book["category"]}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="detail-value">'
                    f'{book["year"]}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="detail-value">'
                    f'{book["pages"]} pages</div>',
                    unsafe_allow_html=True,
                )


            # -------------------------------------------------
            # Description
            # -------------------------------------------------

            st.markdown(
                '<div class="about-title">'
                'About this book'
                '</div>',
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

            if is_in_library(book["id"]):

                if st.button(
                    "Remove from My Library",
                    width="stretch",
                ):

                    st.session_state.library = [
                        item
                        for item in st.session_state.library
                        if item["id"] != book["id"]
                    ]

                    st.success(
                        "Book removed from your library."
                    )

                    st.rerun()

            else:

                if st.button(
                    "＋ Add to My Library",
                    width="stretch",
                ):

                    st.session_state.library.append(
                        book
                    )

                    st.success(
                        "Book added to your library."
                    )

                    st.rerun()


            # -------------------------------------------------
            # Reading Status
            # -------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'Reading Status'
                '</div>',
                unsafe_allow_html=True,
            )

            status_options = [
                "Want to Read",
                "Reading",
                "Completed",
            ]

            current_status = user_data["status"]

            selected_status = st.radio(
                "Reading Status",
                status_options,
                index=status_options.index(
                    current_status
                ),
                horizontal=True,
                label_visibility="collapsed",
                key=f"status_{book['id']}",
            )

            user_data["status"] = selected_status


            # -------------------------------------------------
            # Progress
            # -------------------------------------------------

            st.markdown(
                '<div class="rating-title">'
                'Reading Progress'
                '</div>',
                unsafe_allow_html=True,
            )

            if selected_status == "Want to Read":

                progress = 0

            elif selected_status == "Completed":

                progress = 100

            else:

                progress = st.slider(
                    "Progress",
                    min_value=0,
                    max_value=100,
                    value=user_data["progress"],
                    step=5,
                    format="%d%%",
                    key=f"progress_{book['id']}",
                )

            user_data["progress"] = progress

            st.progress(
                progress / 100
            )


            # -------------------------------------------------
            # Personal Rating
            # -------------------------------------------------

            st.markdown(
                '<div class="rating-title">'
                'Your Rating'
                '</div>',
                unsafe_allow_html=True,
            )

            current_rating = user_data["rating"]

            star_cols = st.columns(5)

            for index, col in enumerate(
                star_cols,
                start=1,
            ):

                with col:

                    star = (
                        "★"
                        if index <= current_rating
                        else "☆"
                    )

                    if index <= current_rating:
                        st.markdown(
                            '<div class="star-active">',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            '<div class="star-button">',
                            unsafe_allow_html=True,
                        )

                    if st.button(
                        star,
                        key=f"rating_star_{book['id']}_{index}",
                        width="stretch",
                    ):

                        user_data["rating"] = index
                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True,
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
                '<div class="rating-title">'
                'Personal Note'
                '</div>',
                unsafe_allow_html=True,
            )

            note = st.text_area(
                "Personal Note",
                value=user_data["note"],
                placeholder=(
                    "Write something about this book..."
                ),
                height=110,
                key=f"note_{book['id']}",
                label_visibility="collapsed",
            )

            user_data["note"] = note

            st.caption(
                "Your note is private and only used "
                "for your personal reading record."
            )


# =========================================================
# MY LIBRARY
# =========================================================

elif st.session_state.page == "Library":

    st.title("My Library")

    st.markdown(
        """
        <p class="description">
            Keep your books organized and track your reading journey.
        </p>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # Library Summary
    # -----------------------------------------------------

    total_books = len(
        st.session_state.library
    )

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

    if not st.session_state.library:

        st.info(
            "Your library is empty. "
            "Explore books on Home and add something to your library."
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


        # -------------------------------------------------
        # All
        # -------------------------------------------------

        with tab_all:

            books = st.session_state.library

            columns = st.columns(5)

            for index, book in enumerate(books):

                with columns[index % 5]:

                    render_book_card(
                        book,
                        f"library_all_{index}",
                        "Library",
                    )

                    data = get_book_user_data(
                        book["id"]
                    )

                    st.caption(
                        f'{data["status"]} · '
                        f'{data["progress"]}%'
                    )

                    if data["rating"] > 0:

                        st.caption(
                            f'Your rating: '
                            f'{"★" * data["rating"]}'
                        )


        # -------------------------------------------------
        # Want to Read
        # -------------------------------------------------

        with tab_want:

            books = [
                book
                for book in st.session_state.library
                if get_book_user_data(
                    book["id"]
                )["status"] == "Want to Read"
            ]

            if not books:

                st.info(
                    "No books in Want to Read."
                )

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_want_{index}",
                            "Library",
                        )


        # -------------------------------------------------
        # Reading
        # -------------------------------------------------

        with tab_reading:

            books = [
                book
                for book in st.session_state.library
                if get_book_user_data(
                    book["id"]
                )["status"] == "Reading"
            ]

            if not books:

                st.info(
                    "No books currently being read."
                )

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_reading_{index}",
                            "Library",
                        )

                        data = get_book_user_data(
                            book["id"]
                        )

                        st.progress(
                            data["progress"] / 100
                        )

                        st.caption(
                            f'{data["progress"]}% completed'
                        )


        # -------------------------------------------------
        # Completed
        # -------------------------------------------------

        with tab_completed:

            books = [
                book
                for book in st.session_state.library
                if get_book_user_data(
                    book["id"]
                )["status"] == "Completed"
            ]

            if not books:

                st.info(
                    "No completed books yet."
                )

            else:

                columns = st.columns(5)

                for index, book in enumerate(books):

                    with columns[index % 5]:

                        render_book_card(
                            book,
                            f"library_completed_{index}",
                            "Library",
                        )

                        data = get_book_user_data(
                            book["id"]
                        )

                        if data["rating"] > 0:

                            st.caption(
                                f'Your rating: '
                                f'{"★" * data["rating"]}'
                            )