import os
import sys
from pathlib import Path

import streamlit as st

# On Streamlit Cloud the key comes from Secrets; locally it comes from .env.
try:
    os.environ.setdefault(
        "GOOGLE_BOOKS_API_KEY",
        st.secrets["GOOGLE_BOOKS_API_KEY"],
    )
except Exception:
    pass
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
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,800&family=DM+Sans:wght@400;500;700&family=Noto+Sans+Thai:wght@400;500;700&display=swap');

    :root {
        --paper: #F6F0E6;      /* ครีม */
        --card: #FFFBF4;       /* ครีมอ่อน */
        --ink: #3B2F2A;        /* น้ำตาลเข้มเกือบดำ */
        --muted: #7A6A5E;      /* น้ำตาลเทา */
        --green: #6B4F3B;      /* น้ำตาลหลัก (ใช้กับ Nav และปุ่ม) */
        --green-soft: #E9DDCB; /* เบจ */
        --mustard: #C9A27A;    /* น้ำตาลอ่อนสำหรับไฮไลต์ */
        --serif: 'Fraunces', 'Noto Sans Thai', serif;
        --sans: 'DM Sans', 'Noto Sans Thai', sans-serif;
    }

    html, body, .stApp,
    .stApp *:not([data-testid="stIconMaterial"])
    :not([class*="material-icons"])
    :not([class*="material-symbols"]) {
        font-family: var(--sans);
    }
    [data-testid="stIconMaterial"],
    span[class*="material-icons"],
    span[class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    .stApp { background: var(--paper); color: var(--ink); }
    .block-container {
        max-width: 1240px;
        padding: 1.2rem 2rem 4rem 2rem;
    }
    h1, h2, h3, .logo, .hero-title, .section-title, .detail-title,
    .genre-title, .about-title {
        font-family: var(--serif) !important;
        color: var(--ink);
        letter-spacing: -0.02em;
    }
    h1 { font-size: 40px !important; font-weight: 800 !important; }

    /* ---------- Top Navigation ---------- */
    .st-key-topnav {
        background: var(--green);
        padding: 0.5rem 0;
        margin-bottom: 1.8rem;
        box-shadow: 0 0 0 100vmax var(--green);
        clip-path: inset(0 -100vmax);
    }
    .logo {
        font-size: 28px; font-weight: 800; color: #FFFFFF !important;
        white-space: nowrap;
    }
    .logo b { color: var(--mustard); }

    div[class*="st-key-nav_"] button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        color: #E6EEE9 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        min-height: 40px !important;
        padding: 0.35rem 0.2rem !important;
        transition: border-color .2s, color .2s;
    }
    div[class*="st-key-nav_"] button p {
        color: inherit !important; font-size: 16px !important;
        white-space: nowrap !important;
    }
    div[class*="st-key-nav_"] button:hover {
        background: transparent !important;
        color: #FFFFFF !important;
        border-bottom-color: var(--mustard) !important;
    }

    /* Browse dropdown (popover) */
    [data-testid="stPopoverBody"] {
        background: var(--card) !important;
        border: 1px solid var(--green-soft) !important;
        border-radius: 14px !important;
        box-shadow: 0 18px 40px rgba(31, 42, 39, .22) !important;
        padding: .6rem !important;
        min-width: 230px;
    }
    div[class*="st-key-pop_genre_"] button {
        background: transparent !important;
        color: var(--ink) !important;
        border: none !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        padding: .5rem .75rem !important;
        font-weight: 500 !important;
        transition: background .15s, padding-left .15s;
    }
    div[class*="st-key-pop_genre_"] button:hover {
        background: var(--green-soft) !important;
        color: var(--green) !important;
        padding-left: 1.05rem !important;
    }

    /* Search */
    .st-key-topnav [data-baseweb="input"],
    .st-key-topnav [data-baseweb="base-input"] {
        background: #FFFFFF !important;
        border-radius: 999px !important;
    }
    .st-key-topnav [data-testid="stTextInput"] [data-baseweb="input"] {
        border: none !important; min-height: 40px !important;
    }
    .st-key-topnav input {
        background: transparent !important; color: var(--ink) !important;
        font-size: 15px !important;
    }

    /* ---------- Hero ---------- */
    .hero {
        display: grid;
        grid-template-columns: 1.15fr 1fr;
        gap: 2rem;
        align-items: center;
        background: var(--card);
        border-radius: 22px;
        padding: 2.6rem 3rem;
        margin-bottom: 2.4rem;
        border: 1px solid var(--green-soft);
        overflow: hidden;
    }
    .hero-title {
        font-size: 50px; line-height: 1.08; font-weight: 800; margin: 0 0 .9rem 0;
    }
    .hero-text {
        color: var(--muted); font-size: 17px; line-height: 1.65; max-width: 460px;
    }
    .shelf {
        display: flex; align-items: flex-end; justify-content: center;
        gap: 6px; height: 210px;
        border-bottom: 6px solid var(--green);
    }
    .spine {
        width: 44px; border-radius: 4px 4px 0 0;
        transform-origin: bottom center;
        box-shadow: inset -6px 0 0 rgba(0,0,0,.12);
        animation: rise .9s cubic-bezier(.2,.8,.2,1) both;
    }
    .spine:nth-child(1) { height: 150px; background: #23463C; animation-delay: .05s; }
    .spine:nth-child(2) { height: 190px; background: #E0A526; animation-delay: .15s; }
    .spine:nth-child(3) { height: 165px; background: #7A9E8E; animation-delay: .25s; }
    .spine:nth-child(4) { height: 200px; background: #1F2A27; animation-delay: .35s; }
    .spine:nth-child(5) { height: 140px; background: #B9553A; animation-delay: .45s; }
    .spine:nth-child(6) { height: 178px; background: #C9D8CF; animation-delay: .55s; }
    .spine.lean { transform: rotate(9deg); margin-left: 14px; }
    @keyframes rise {
        from { transform: translateY(40px); opacity: 0; }
        to   { opacity: 1; }
    }
    @media (max-width: 800px) {
        .hero { grid-template-columns: 1fr; padding: 1.6rem; }
        .hero-title { font-size: 36px; }
    }
    @media (prefers-reduced-motion: reduce) { .spine { animation: none; } }

    /* ---------- Section titles ---------- */
    .section-title {
        display: flex; align-items: center; gap: 1rem;
        font-size: 28px; font-weight: 700;
        margin: 2.4rem 0 .4rem 0;
    }
    .section-title::after {
        content: ""; flex: 1; height: 2px; background: var(--green-soft);
    }
    .section-subtitle { color: var(--muted); font-size: 15px; margin-bottom: 1.1rem; }
    .description { color: var(--muted); font-size: 16px; line-height: 1.6; }

    /* ---------- Genre header (Browse) ---------- */
    .genre-hero {
        background: var(--green); color: #fff;
        border-radius: 22px; padding: 2.4rem 3rem; margin-bottom: 2rem;
        position: relative; overflow: hidden;
    }
    .genre-hero::after {
        content: attr(data-icon); position: absolute; right: 2.5rem; top: 50%;
        transform: translateY(-50%) rotate(-8deg);
        font-size: 120px; opacity: .22;
    }
    .genre-title { color: #fff !important; font-size: 46px; font-weight: 800; margin: 0 0 .4rem 0; }
    .genre-desc { color: #CFE0D6; font-size: 17px; max-width: 560px; line-height: 1.6; }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px; border: none;
        background: var(--green); color: #FFFFFF;
        font-weight: 600; padding: .5rem 1.2rem;
        transition: background .2s, transform .15s;
    }
    .stButton > button:hover { background: #17332B; color: #fff; transform: translateY(-1px); }

    /* ---------- Book cards ---------- */
    .book-cover-wrapper {
        width: 100%; height: 270px; overflow: hidden;
        border-radius: 4px 10px 10px 4px;
        background: var(--green-soft);
        border-left: 5px solid var(--green);
        box-shadow: 0 10px 22px rgba(31, 42, 39, .18);
        position: relative;
        transition: transform .25s ease, box-shadow .25s ease;
    }
    .book-cover-wrapper::after {
        content: ""; position: absolute; top: 0; right: 14px;
        width: 14px; height: 0; background: var(--mustard);
        clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 80%, 0 100%);
        transition: height .25s ease;
    }
    .book-cover-wrapper:hover {
        transform: translateY(-6px) rotate(-1deg);
        box-shadow: 0 18px 30px rgba(31, 42, 39, .28);
    }
    .book-cover-wrapper:hover::after { height: 38px; }
    .book-cover-wrapper img {
        width: 100%; height: 270px; object-fit: cover; display: block;
    }
    .book-title {
        font-family: var(--serif); font-size: 17px; font-weight: 700;
        color: var(--ink); margin-top: 14px; line-height: 1.3; height: 44px;
        overflow: hidden; display: -webkit-box;
        -webkit-box-orient: vertical; -webkit-line-clamp: 2; line-clamp: 2;
    }
    .book-author {
        font-size: 14px; color: var(--muted); margin-top: 4px; height: 20px;
        overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
    }
    .book-meta {
        font-size: 12px; color: #8D9993; margin: 6px 0 9px 0; height: 18px;
        overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
    }
    .library-meta {
        height: 24px; line-height: 24px; font-size: 13px; color: var(--muted);
        overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
    }
    .library-meta-empty { visibility: hidden; }
    .library-progress-text { height: 24px; line-height: 24px; font-size: 13px; color: var(--muted); }
    .library-count { font-size: 14px; color: var(--muted); margin-bottom: 20px; }
    .reading-progress-text { font-size: 12px; color: var(--muted); margin-top: 5px; }

    /* ---------- Book Detail (เดิม ปรับสี) ---------- */
    .detail-title { font-size: 40px; font-weight: 800; line-height: 1.15; margin-bottom: 6px; }
    .detail-author { font-size: 18px; color: var(--muted); margin-bottom: 20px; }
    .about-title { font-size: 22px; font-weight: 700; margin: 25px 0 8px 0; }
    .about-text { font-size: 15px; color: #4A5752; line-height: 1.75; }
    .detail-label { font-size: 13px; color: #8D9993; margin-bottom: 3px; }
    .detail-value { font-size: 15px; color: var(--ink); margin-bottom: 13px; }
    .detail-cover img { border-radius: 6px 12px 12px 6px; box-shadow: 0 14px 30px rgba(31,42,39,.25); }
    .rating-title { font-size: 15px; font-weight: 700; color: var(--ink); margin: 20px 0 8px 0; }

    .back-button .stButton > button {
        background: transparent; color: var(--muted);
        padding: 0; font-size: 25px; width: auto;
    }
    .back-button .stButton > button:hover { background: transparent; color: var(--ink); }

    div[class*="st-key-rating_star_"] { width: auto !important; }
    div[class*="st-key-rating_star_"] button {
        background: transparent !important; border: 0 !important; box-shadow: none !important;
        color: #C4CFC9 !important; font-size: 30px !important; line-height: 1 !important;
        min-height: 0 !important; padding: 0 !important; width: auto !important;
    }
    div[class*="st-key-rating_star_"] button:hover { color: var(--mustard) !important; }
    div[class*="st-key-rating_star_active_"] button { color: var(--mustard) !important; }

    /* ---------- Layout กว้างขึ้น + ไม่ให้ชิดขอบบน ---------- */
header[data-testid="stHeader"] { display: none; }

.block-container {
    max-width: 1360px !important;
    padding-top: 0 !important;
}

/* ---------- Top Navigation ---------- */
.st-key-topnav {
    background: var(--green) !important;
    padding: 1.3rem 0 !important;      /* สูงขึ้น ตัวหนังสือไม่ชิดบน */
    margin-top: 0 !important;
    margin-bottom: 2.4rem !important;
    box-shadow: 0 0 0 100vmax var(--green), 0 6px 18px rgba(59, 47, 42, .18) !important;
}
.st-key-topnav [data-testid="stHorizontalBlock"] {
    min-height: 56px;
    gap: 1.2rem !important;
}
.logo { font-size: 30px !important; }

div[class*="st-key-nav_"] button {
    color: #F3E9DA !important;
    font-size: 17px !important;
    min-height: 48px !important;
    padding: .6rem .9rem !important;
}
div[class*="st-key-nav_"] button p { font-size: 17px !important; }
.st-key-topnav [data-testid="stTextInput"] [data-baseweb="input"] {
    min-height: 46px !important;
    background: var(--card) !important;
}

/* ---------- สีที่ฝังไว้ในโค้ดเดิม ---------- */
.stButton > button:hover { background: #4E3829 !important; }
.genre-desc { color: #EADCC8 !important; }
.hero-text, .about-text { color: #6A5B50 !important; }
.book-meta, .detail-label { color: #A09082 !important; }
.book-cover-wrapper { box-shadow: 0 10px 22px rgba(59, 47, 42, .18) !important; }
.book-cover-wrapper:hover { box-shadow: 0 18px 30px rgba(59, 47, 42, .28) !important; }
.detail-cover img { box-shadow: 0 14px 30px rgba(59, 47, 42, .25) !important; }
[data-testid="stPopoverBody"] { box-shadow: 0 18px 40px rgba(59, 47, 42, .22) !important; }
div[class*="st-key-rating_star_"] button { color: #D8CBBA !important; }

/* สันหนังสือใน Hero โทนน้ำตาล */
.spine:nth-child(1) { background: #6B4F3B !important; }
.spine:nth-child(2) { background: #C9A27A !important; }
.spine:nth-child(3) { background: #A98467 !important; }
.spine:nth-child(4) { background: #3B2F2A !important; }
.spine:nth-child(5) { background: #8C5A3C !important; }
.spine:nth-child(6) { background: #E3D3BC !important; }
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

@st.cache_data(ttl=600, show_spinner=False)
def cached_home_books():
    """Home recommendations, cached for 10 minutes.

    Errors and empty results raise, so they are never cached and the
    next page load tries Google Books again.
    """
    books = get_home_books()
    if not books:
        raise ValueError("No books returned")
    return books


@st.cache_data(ttl=600, show_spinner=False)
def cached_browse_books(genre):
    """Browse results for one genre, cached for 10 minutes.

    Errors and empty results raise, so they are never cached.
    """
    books = browse_books(genre)
    if not books:
        raise ValueError("No books returned")
    return books


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


def open_book(book, source="Home", full=False):
    """Open Book Detail.

    full=True shows the full reading-tracker view for a book that is in
    the library (My Books and Continue Reading). Otherwise a book that
    is already in the library just shows "Added to Library".
    """
    try:
        detailed_book = get_book_details(book["id"])
    except Exception:
        detailed_book = book

    st.session_state.selected_book = detailed_book
    st.session_state.detail_source = source
    st.session_state.detail_full = full or source == "Library"
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
    st.session_state.search_error = ""

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

GENRES = {
    "Fiction":  ("📖", "เรื่องเล่าที่พาไปไกลกว่าชีวิตประจำวัน ทั้งนิยายร่วมสมัยและวรรณกรรมคลาสสิก"),
    "Romance":  ("💌", "เรื่องราวความรักทุกรสชาติ ตั้งแต่หวานละมุนจนถึงเจ็บแต่คุ้ม"),
    "Mystery":  ("🔍", "ปริศนา คดีลึกลับ และตอนจบที่คุณเดาไม่ถูก"),
    "Fantasy":  ("🐉", "โลกเวทมนตร์ ตำนาน และการผจญภัยที่ไม่มีอยู่จริง"),
    "Science":  ("🔬", "ความรู้วิทยาศาสตร์ที่อ่านสนุกและเข้าใจง่าย"),
    "History":  ("🏛️", "เรื่องราวในอดีตที่อธิบายว่าทำไมโลกถึงเป็นแบบทุกวันนี้"),
    "Business": ("💼", "แนวคิดการทำงาน การเงิน และการสร้างธุรกิจ"),
}

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = "Fiction"

# =========================================================
# Top Navigation
# =========================================================

with st.container(key="topnav"):

    nav_logo, nav_home, nav_books, nav_browse, nav_search = st.columns(
        [2.2, 0.95, 1.15, 1.05, 3.2],
        gap="small",
        vertical_alignment="center",
    )

    with nav_logo:
        st.markdown(
            '<div class="logo">📚 Book<b>Log</b></div>',
            unsafe_allow_html=True,
        )

    with nav_home:
        if st.button("Home", key="nav_home", width="stretch"):
            st.session_state.page = "Home"
            st.session_state.selected_book = None
            clear_search()
            st.rerun()

    with nav_books:
        if st.button("My Books", key="nav_books", width="stretch"):
            st.session_state.page = "Library"
            st.session_state.selected_book = None
            clear_search()
            st.rerun()

    # Browse = dropdown เลือกประเภท
    with nav_browse:
        with st.container(key="nav_browse"):
            with st.popover("Browse", width="stretch"):
                for genre, (icon, _) in GENRES.items():
                    if st.button(
                        f"{icon}  {genre}",
                        key=f"pop_genre_{genre}",
                        width="stretch",
                    ):
                        st.session_state.selected_genre = genre
                        st.session_state.page = "Browse"
                        st.session_state.selected_book = None
                        clear_search()
                        st.rerun()

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
        <div class="hero">
            <div>
                <h1 class="hero-title">หนังสือเล่มต่อไป<br>รออยู่บนชั้นนี้</h1>
                <div class="hero-text">
                    ค้นหาหนังสือ เก็บไว้ในคลังของคุณ
                    และบันทึกว่าอ่านถึงหน้าไหนแล้ว
                </div>
            </div>
            <div class="shelf">
                <div class="spine"></div>
                <div class="spine"></div>
                <div class="spine"></div>
                <div class="spine"></div>
                <div class="spine"></div>
                <div class="spine lean"></div>
            </div>
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

        if st.session_state.get("search_error"):
            st.warning(
                "Could not search right now. "
                "Please check the error details below."
            )
            with st.expander("Error details"):
                st.code(st.session_state.search_error)
        else:
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
                            full=True,
                        )


    # -----------------------------------------------------
    # Discover Books (always shown)
    # -----------------------------------------------------

    home_books = []

    try:
        home_books = cached_home_books()
    except Exception:
        home_books = []

    st.markdown(
        '<div class="section-title">Discover Books</div>',
        unsafe_allow_html=True,
    )

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
        st.warning(
            "Could not load books right now. "
            "Google Books may be busy, so please try again in a moment."
        )
        st.button("Try again", key="home_retry")

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
            # Opened from search / Browse / Discover: just show
            # that the book is added (no tracking controls)
            # -------------------------------------------------

            if not st.session_state.get("detail_full", False):

                st.button(
                    "✓ Added to Library",
                    key=f"added_{book['id']}",
                    width="stretch",
                    disabled=True,
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

    genre = st.session_state.selected_genre
    icon, desc = GENRES[genre]

    st.markdown(
        f"""
        <div class="genre-hero" data-icon="{icon}">
            <h1 class="genre-title">{genre}</h1>
            <div class="genre-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    books = None
    try:
        books = cached_browse_books(genre)
    except Exception:
        books = None

    if books is None:
        st.warning(
            "โหลดหนังสือไม่สำเร็จ Google Books อาจกำลังหนาแน่น "
            "ลองอีกครั้งในอีกสักครู่"
        )
        st.button("Try again", key="browse_retry")

    else:
        st.markdown(
            f'<div class="library-count">{len(books)} books in {genre}</div>',
            unsafe_allow_html=True,
        )

        columns = st.columns(5)

        for index, book in enumerate(books):
            with columns[index % 5]:
                render_book_card(
                    book,
                    f"browse_{genre}_{index}",
                    "Browse",
                )
