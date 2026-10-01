# ============================================================
# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE
# ============================================================

# ============================================================
# INSTALL
# ============================================================
# For Streamlit Cloud, add these to requirements.txt:
#
# streamlit
# pypdf
# gtts
# langdetect
#
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
from langdetect import detect

import os
import re
import hashlib


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Document Voice Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# MODERN DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #0b0f14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    p, span, label {
        color: #d1d5db;
    }

    hr {
        border-color: #293442 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #11151c !important;
        border-right: 1px solid #29313d;
    }

    section[data-testid="stSidebar"] * {
        box-sizing: border-box;
    }

    .sidebar-brand {
        color: #ffffff !important;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        color: #8995a5 !important;
        font-size: 13px;
        margin-bottom: 20px;
    }

    .sidebar-section {
        color: #8995a5 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-top: 8px;
        margin-bottom: 10px;
    }

    .motivation-card {
        background: #171d26;
        border: 1px solid #2d3746;
        border-radius: 14px;
        padding: 14px;
        margin-top: 5px;
    }

    .motivation-text {
        color: #e5e7eb !important;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.5;
    }

    .sidebar-bottom {
        margin-top: 15px;
        padding-top: 12px;
        border-top: 1px solid #293442;
    }

    .sidebar-product {
        color: #ffffff !important;
        font-size: 13px;
        font-weight: 750;
    }

    .sidebar-tagline {
        color: #6b7280 !important;
        font-size: 11px;
        margin-top: 4px;
    }


    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .project-title {
        color: #ffffff !important;
        font-size: 40px;
        font-weight: 850;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .project-subtitle {
        color: #8f9baa !important;
        font-size: 16px;
        margin-bottom: 28px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 800;
        margin-top: 22px;
        margin-bottom: 12px;
    }


    /* ========================================================
       UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #151a22 !important;
        border: 1px solid #303a48 !important;
        border-radius: 18px !important;
        padding: 10px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #151a22 !important;
        border: 1px dashed #526071 !important;
        border-radius: 14px !important;
        min-height: 170px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: #19212b !important;
        border-color: #60a5fa !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #e5e7eb !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #e5e7eb !important;
    }

    [data-testid="stFileUploaderDropzone"] small {
        color: #9ca3af !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       STAT CARDS
       ======================================================== */

    .stat-card {
        background: #151a22;
        border: 1px solid #293442;
        border-radius: 15px;
        padding: 18px;
        min-height: 105px;
    }

    .stat-label {
        color: #8f9baa !important;
        font-size: 12px;
        font-weight: 600;
    }

    .stat-number {
        color: #ffffff !important;
        font-size: 27px;
        font-weight: 850;
        margin-top: 6px;
    }


    /* ========================================================
       DOCUMENT CARD
       ======================================================== */

    .document-card {
        background: #151a22;
        border: 1px solid #293442;
        border-radius: 16px;
        padding: 18px 20px;
        margin-top: 20px;
    }

    .document-name {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 750;
    }

    .document-info {
        color: #8f9baa !important;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ========================================================
       CONTENT CARD
       ======================================================== */

    .content-card {
        background: #151a22;
        border: 1px solid #293442;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .content-title {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .content-text {
        color: #bfc8d4 !important;
        font-size: 14px;
        line-height: 1.6;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background: #171d26 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
        border-radius: 10px !important;
        min-height: 42px;
        font-weight: 650 !important;
    }

    .stButton > button:hover {
        background: #202a37 !important;
        border-color: #60a5fa !important;
    }

    button[kind="primary"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        background: #1d4ed8 !important;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    textarea {
        background: #151a22 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input {
        background: #151a22 !important;
        color: #ffffff !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: #151a22 !important;
        border: 1px solid #293442 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        margin-top: 35px;
        padding-top: 18px;
        border-top: 1px solid #293442;
        text-align: center;
    }

    .footer-quote {
        color: #e5e7eb !important;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.5;
    }

    .footer-brand {
        color: #ffffff !important;
        font-size: 13px;
        font-weight: 750;
        margin-top: 5px;
    }

    .footer-tagline {
        color: #6b7280 !important;
        font-size: 11px;
        margin-top: 3px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "pages" not in st.session_state:
    st.session_state.pages = []

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "file_id" not in st.session_state:
    st.session_state.file_id = None

if "detected_language" not in st.session_state:
    st.session_state.detected_language = "en"

if "page_audio" not in st.session_state:
    st.session_state.page_audio = None

if "paragraph_audio" not in st.session_state:
    st.session_state.paragraph_audio = {}

if "sentence_audio" not in st.session_state:
    st.session_state.sentence_audio = {}

# IMPORTANT:
# This is used to safely reset the uploader.
if "uploader_version" not in st.session_state:
    st.session_state.uploader_version = 0


# ============================================================
# LANGUAGE MAP
# ============================================================

LANGUAGE_MAP = {
    "en": "en",
    "hi": "hi",
    "kn": "kn",
    "te": "te",
    "ta": "ta",
    "ml": "ml",
    "mr": "mr",
    "bn": "bn",
    "gu": "gu",
    "pa": "pa",
    "ur": "ur",
    "ne": "ne",

    "fr": "fr",
    "de": "de",
    "es": "es",
    "it": "it",
    "pt": "pt",
    "ru": "ru",
    "ar": "ar",
    "ja": "ja",
    "ko": "ko",

    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",

    "id": "id",
    "tr": "tr",
    "vi": "vi",
    "th": "th"
}


# ============================================================
# CLEAR ALL
# ============================================================

def clear_all():

    # Clear document
    st.session_state.pages = []

    # Reset current page
    st.session_state.current_page = 0

    # Clear file information
    st.session_state.file_name = ""
    st.session_state.file_id = None

    # Reset language
    st.session_state.detected_language = "en"

    # Clear generated audio
    st.session_state.page_audio = None
    st.session_state.paragraph_audio = {}
    st.session_state.sentence_audio = {}

    # Safely create a new uploader widget
    st.session_state.uploader_version += 1


# ============================================================
# FILE ID
# ============================================================

def make_file_id(uploaded_file):

    uploaded_file.seek(0)

    data = uploaded_file.read()

    uploaded_file.seek(0)

    return (
        uploaded_file.name,
        uploaded_file.size,
        hashlib.md5(data).hexdigest()
    )


# ============================================================
# EXTRACT PDF
# ============================================================

def extract_pdf(uploaded_file):

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:

        try:
            text = page.extract_text()
        except Exception:
            text = ""

        if text:
            pages.append(text.strip())
        else:
            pages.append("")

    uploaded_file.seek(0)

    return pages


# ============================================================
# GET PARAGRAPHS
# ============================================================

def get_paragraphs(text):

    if not text or not text.strip():
        return []

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    paragraphs = [
        p.strip()
        for p in paragraphs
        if p.strip()
    ]

    if not paragraphs:
        return [text.strip()]

    return paragraphs


# ============================================================
# GET SENTENCES
# ============================================================

def get_sentences(text):

    if not text or not text.strip():
        return []

    sentences = re.split(
        r"(?<=[.!?।！？])\s+",
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    return sentences


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text):

    try:

        if not text or not text.strip():
            return "en"

        detected = detect(
            text[:3000]
        )

        return detected

    except Exception:
        return "en"


# ============================================================
# CREATE AUDIO
# ============================================================

def create_audio(
    text,
    filename,
    language
):

    if not text or not text.strip():
        return None

    try:

        gtts_language = LANGUAGE_MAP.get(
            language,
            "en"
        )

        tts = gTTS(
            text=text,
            lang=gtts_language,
            slow=False
        )

        tts.save(filename)

        return filename

    except Exception as error:

        st.error(
            f"❌ Voice generation error: {error}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            🎙️ Document Voice
        </div>

        <div class="sidebar-subtitle">
            Document-Audio Studio
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-section">
            NAVIGATION
        </div>
        """,
        unsafe_allow_html=True
    )

    navigation = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Document",
            "🎙️ Voice Studio",
            "📊 Analytics"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # IMPORTANT:
    # Sidebar motivation is plain Streamlit text.
    # No HTML div is used here.
    st.markdown(
        "### 💡 Daily Thought"
    )

    st.info(
        "Every word you listen to can become "
        "knowledge you remember."
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-bottom">

            <div class="sidebar-product">
                🎙️ Document Voice Studio
            </div>

            <div class="sidebar-tagline">
                Listen • Learn • Remember • Grow
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="project-title">
        🎙️ Document Voice Studio
    </div>

    <div class="project-subtitle">
        Transform your documents into voice
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if navigation == "🏠 Dashboard":

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📄 Upload Your Document
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Upload a PDF and explore it page by page, "
        "paragraph by paragraph, and sentence by sentence."
    )

    uploaded_file = st.file_uploader(
        "Drag and drop your PDF here",
        type=["pdf"],
        key=f"document_uploader_{st.session_state.uploader_version}"
    )


    # --------------------------------------------------------
    # PROCESS PDF
    # --------------------------------------------------------

    if uploaded_file is not None:

        new_file_id = make_file_id(
            uploaded_file
        )

        if st.session_state.file_id != new_file_id:

            try:

                with st.spinner(
                    "📖 Reading your document..."
                ):

                    pages = extract_pdf(
                        uploaded_file
                    )

                    st.session_state.pages = pages

                    st.session_state.current_page = 0

                    st.session_state.file_name = (
                        uploaded_file.name
                    )

                    st.session_state.file_id = (
                        new_file_id
                    )

                    st.session_state.page_audio = None

                    st.session_state.paragraph_audio = {}

                    st.session_state.sentence_audio = {}

                    full_text = "\n".join(
                        pages
                    )

                    st.session_state.detected_language = (
                        detect_language(
                            full_text
                        )
                    )

                st.success(
                    "✅ Document loaded successfully."
                )

            except Exception as error:

                st.error(
                    f"❌ Could not read PDF: {error}"
                )


    # --------------------------------------------------------
    # DOCUMENT DETAILS
    # --------------------------------------------------------

    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        full_text = "\n".join(
            pages
        )

        all_paragraphs = get_paragraphs(
            full_text
        )

        all_sentences = get_sentences(
            full_text
        )

        total_characters = len(
            full_text
        )

        total_words = len(
            full_text.split()
        )


        # ----------------------------------------------------
        # CURRENT DOCUMENT
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📘 Current Document
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="document-card">

                <div class="document-name">
                    📄 {st.session_state.file_name}
                </div>

                <div class="document-info">
                    {total_pages} Pages
                    •
                    {total_characters:,} Characters
                    •
                    {total_words:,} Words
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # DOCUMENT ANALYTICS
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📊 Document Analytics
            </div>
            """,
            unsafe_allow_html=True
        )

        a1, a2, a3, a4, a5 = st.columns(5)

        with a1:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        📄 Pages
                    </div>
                    <div class="stat-number">
                        {total_pages}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a2:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        🔤 Characters
                    </div>
                    <div class="stat-number">
                        {total_characters:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a3:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        📝 Words
                    </div>
                    <div class="stat-number">
                        {total_words:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a4:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        📑 Paragraphs
                    </div>
                    <div class="stat-number">
                        {len(all_paragraphs)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a5:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        🔤 Sentences
                    </div>
                    <div class="stat-number">
                        {len(all_sentences)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # DOCUMENT INFORMATION
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📋 Document Information
            </div>
            """,
            unsafe_allow_html=True
        )

        info1, info2 = st.columns(2)

        with info1:

            st.markdown(
                f"""
                <div class="content-card">

                    <div class="content-title">
                        📄 File Information
                    </div>

                    <div class="content-text">
                        <b>File:</b>
                        {st.session_state.file_name}
                        <br><br>

                        <b>Pages:</b>
                        {total_pages}
                        <br><br>

                        <b>Language:</b>
                        {st.session_state.detected_language}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with info2:

            st.markdown(
                f"""
                <div class="content-card">

                    <div class="content-title">
                        📊 Content Information
                    </div>

                    <div class="content-text">
                        <b>Characters:</b>
                        {total_characters:,}
                        <br><br>

                        <b>Words:</b>
                        {total_words:,}
                        <br><br>

                        <b>Paragraphs:</b>
                        {len(all_paragraphs)}
                        <br><br>

                        <b>Sentences:</b>
                        {len(all_sentences)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # PAGE NAVIGATION
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📖 Page Navigation
            </div>
            """,
            unsafe_allow_html=True
        )

        nav1, nav2, nav3 = st.columns(
            [1, 2, 1]
        )

        with nav1:

            if st.button(
                "← Previous",
                use_container_width=True,
                disabled=(
                    st.session_state.current_page == 0
                ),
                key="dashboard_previous"
            ):

                st.session_state.current_page -= 1

                st.session_state.page_audio = None

                st.rerun()


        with nav2:

            selected_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=(
                    st.session_state.current_page + 1
                ),
                step=1,
                key="dashboard_page_number"
            )

            if (
                selected_page - 1
                != st.session_state.current_page
            ):

                st.session_state.current_page = (
                    selected_page - 1
                )

                st.session_state.page_audio = None

                st.rerun()


        with nav3:

            if st.button(
                "Next →",
                use_container_width=True,
                disabled=(
                    st.session_state.current_page
                    == total_pages - 1
                ),
                key="dashboard_next"
            ):

                st.session_state.current_page += 1

                st.session_state.page_audio = None

                st.rerun()


        # ----------------------------------------------------
        # CURRENT PAGE
        # ----------------------------------------------------

        current_page = (
            st.session_state.current_page
        )

        current_text = pages[
            current_page
        ]

        paragraphs = get_paragraphs(
            current_text
        )

        sentences = get_sentences(
            current_text
        )


        st.markdown(
            f"""
            <div class="section-title">
                📄 Page {current_page + 1}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.text_area(
            "Current Page Content",
            value=current_text,
            height=300,
            disabled=True,
            key="dashboard_current_page"
        )


        # ----------------------------------------------------
        # PAGE STATISTICS
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📊 Page Statistics
            </div>
            """,
            unsafe_allow_html=True
        )

        p1, p2, p3, p4 = st.columns(4)

        with p1:
            st.metric(
                "Characters",
                f"{len(current_text):,}"
            )

        with p2:
            st.metric(
                "Words",
                f"{len(current_text.split()):,}"
            )

        with p3:
            st.metric(
                "Paragraphs",
                len(paragraphs)
            )

        with p4:
            st.metric(
                "Sentences",
                len(sentences)
            )


        # ----------------------------------------------------
        # PAGE VOICE
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                🎙️ Page Voice
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🎙️ Generate Page Voice",
            type="primary",
            use_container_width=True,
            key="dashboard_page_voice"
        ):

            filename = (
                f"page_{current_page + 1}_voice.mp3"
            )

            with st.spinner(
                "Generating page voice..."
            ):

                audio = create_audio(
                    current_text,
                    filename,
                    st.session_state.detected_language
                )

            if audio:

                st.session_state.page_audio = audio

                st.success(
                    "✅ Page voice generated."
                )

        if st.session_state.page_audio:

            st.audio(
                st.session_state.page_audio
            )

            with open(
                st.session_state.page_audio,
                "rb"
            ) as audio_file:

                st.download_button(
                    "⬇️ Download Page Voice",
                    data=audio_file,
                    file_name=os.path.basename(
                        st.session_state.page_audio
                    ),
                    mime="audio/mpeg",
                    use_container_width=True,
                    key="dashboard_download_page_voice"
                )


        # ----------------------------------------------------
        # PARAGRAPHS
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                📝 Paragraphs
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, paragraph in enumerate(
            paragraphs
        ):

            paragraph_key = (
                f"{current_page}_{i}"
            )

            with st.expander(
                f"📝 Paragraph {i + 1}",
                expanded=False
            ):

                st.write(
                    paragraph
                )

                if st.button(
                    f"🎙️ Generate Paragraph {i + 1} Voice",
                    key=f"dash_paragraph_generate_{current_page}_{i}",
                    use_container_width=True
                ):

                    filename = (
                        f"page_{current_page + 1}"
                        f"_paragraph_{i + 1}.mp3"
                    )

                    with st.spinner(
                        "Generating paragraph voice..."
                    ):

                        audio = create_audio(
                            paragraph,
                            filename,
                            st.session_state.detected_language
                        )

                    if audio:

                        st.session_state.paragraph_audio[
                            paragraph_key
                        ] = audio

                        st.success(
                            "✅ Paragraph voice generated."
                        )

                if paragraph_key in (
                    st.session_state.paragraph_audio
                ):

                    audio_file = (
                        st.session_state.paragraph_audio[
                            paragraph_key
                        ]
                    )

                    st.audio(
                        audio_file
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download Paragraph Voice",
                            data=file,
                            file_name=os.path.basename(
                                audio_file
                            ),
                            mime="audio/mpeg",
                            use_container_width=True,
                            key=f"dash_paragraph_download_{current_page}_{i}"
                        )


        # ----------------------------------------------------
        # SENTENCES
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
                🔤 Sentences
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, sentence in enumerate(
            sentences
        ):

            sentence_key = (
                f"{current_page}_{i}"
            )

            with st.expander(
                f"🔤 Sentence {i + 1}",
                expanded=False
            ):

                st.write(
                    sentence
                )

                if st.button(
                    f"🎙️ Generate Sentence {i + 1} Voice",
                    key=f"dash_sentence_generate_{current_page}_{i}",
                    use_container_width=True
                ):

                    filename = (
                        f"page_{current_page + 1}"
                        f"_sentence_{i + 1}.mp3"
                    )

                    with st.spinner(
                        "Generating sentence voice..."
                    ):

                        audio = create_audio(
                            sentence,
                            filename,
                            st.session_state.detected_language
                        )

                    if audio:

                        st.session_state.sentence_audio[
                            sentence_key
                        ] = audio

                        st.success(
                            "✅ Sentence voice generated."
                        )

                if sentence_key in (
                    st.session_state.sentence_audio
                ):

                    audio_file = (
                        st.session_state.sentence_audio[
                            sentence_key
                        ]
                    )

                    st.audio(
                        audio_file
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download Sentence Voice",
                            data=file,
                            file_name=os.path.basename(
                                audio_file
                            ),
                            mime="audio/mpeg",
                            use_container_width=True,
                            key=f"dash_sentence_download_{current_page}_{i}"
                        )


    # --------------------------------------------------------
    # NO DOCUMENT
    # --------------------------------------------------------

    else:

        st.info(
            "📄 Upload a PDF above to start "
            "using Document Voice Studio."
        )

        st.markdown(
            """
            <div class="content-card">

                <div class="content-title">
                    💡 How It Works
                </div>

                <div class="content-text">

                    <b>01</b> — Upload your PDF document
                    <br><br>

                    <b>02</b> — View your document page by page
                    <br><br>

                    <b>03</b> — Read individual paragraphs
                    <br><br>

                    <b>04</b> — Convert pages, paragraphs
                    and sentences into voice
                    <br><br>

                    <b>05</b> — Play and download your audio

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DOCUMENT PAGE
# ============================================================

elif navigation == "📄 Document":

    st.markdown(
        """
        <div class="section-title">
            📄 Document
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Read and explore your uploaded document page by page."
    )


    # HOW TO USE

    st.markdown(
        """
        <div class="content-card">

            <div class="content-title">
                💡 How to Use Document
            </div>

            <div class="content-text">

                <b>01</b> — Go to Dashboard and upload a PDF.
                <br><br>

                <b>02</b> — Return here to read extracted text.
                <br><br>

                <b>03</b> — Use Previous and Next to move
                between pages.
                <br><br>

                <b>04</b> — Check page statistics.
                <br><br>

                <b>05</b> — Expand paragraphs and sentences
                to read individual sections.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        current_page = (
            st.session_state.current_page
        )

        current_text = pages[
            current_page
        ]

        paragraphs = get_paragraphs(
            current_text
        )

        sentences = get_sentences(
            current_text
        )


        # PAGE NAVIGATION

        st.markdown(
            """
            <div class="section-title">
                📖 Page Navigation
            </div>
            """,
            unsafe_allow_html=True
        )

        d1, d2, d3 = st.columns(
            [1, 2, 1]
        )

        with d1:

            if st.button(
                "← Previous",
                use_container_width=True,
                disabled=current_page == 0,
                key="document_previous"
            ):

                st.session_state.current_page -= 1

                st.rerun()


        with d2:

            selected_page = st.number_input(
                "Page Number",
                min_value=1,
                max_value=total_pages,
                value=current_page + 1,
                step=1,
                key="document_page_number"
            )

            if (
                selected_page - 1
                != current_page
            ):

                st.session_state.current_page = (
                    selected_page - 1
                )

                st.rerun()


        with d3:

            if st.button(
                "Next →",
                use_container_width=True,
                disabled=current_page == total_pages - 1,
                key="document_next"
            ):

                st.session_state.current_page += 1

                st.rerun()


        # PAGE

        st.markdown(
            f"### 📄 Page {current_page + 1}"
        )

        st.caption(
            f"Document: {st.session_state.file_name}"
        )

        st.text_area(
            "Page Content",
            value=current_text,
            height=430,
            disabled=True,
            key="document_page_content"
        )


        # PAGE STATISTICS

        st.markdown(
            """
            <div class="section-title">
                📊 Page Statistics
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Characters",
                f"{len(current_text):,}"
            )

        with c2:
            st.metric(
                "Words",
                f"{len(current_text.split()):,}"
            )

        with c3:
            st.metric(
                "Paragraphs",
                len(paragraphs)
            )

        with c4:
            st.metric(
                "Sentences",
                len(sentences)
            )


        # PARAGRAPHS

        st.markdown(
            """
            <div class="section-title">
                📝 Paragraphs
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, paragraph in enumerate(
            paragraphs
        ):

            with st.expander(
                f"Paragraph {i + 1}"
            ):

                st.write(
                    paragraph
                )


        # SENTENCES

        st.markdown(
            """
            <div class="section-title">
                🔤 Sentences
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, sentence in enumerate(
            sentences
        ):

            with st.expander(
                f"Sentence {i + 1}"
            ):

                st.write(
                    sentence
                )

    else:

        st.info(
            "📄 Please upload a PDF from Dashboard first."
        )


# ============================================================
# VOICE STUDIO
# ============================================================

elif navigation == "🎙️ Voice Studio":

    st.markdown(
        """
        <div class="section-title">
            🎙️ Voice Studio
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Convert pages, paragraphs and sentences into voice."
    )


    # HOW TO USE

    st.markdown(
        """
        <div class="content-card">

            <div class="content-title">
                💡 How to Use Voice Studio
            </div>

            <div class="content-text">

                <b>01</b> — Upload a PDF from Dashboard.
                <br><br>

                <b>02</b> — Select the page you want.
                <br><br>

                <b>03</b> — Generate complete page voice.
                <br><br>

                <b>04</b> — Generate individual paragraph voice.
                <br><br>

                <b>05</b> — Generate individual sentence voice.
                <br><br>

                <b>06</b> — Play and download generated audio.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        current_page = (
            st.session_state.current_page
        )

        current_text = pages[
            current_page
        ]

        paragraphs = get_paragraphs(
            current_text
        )

        sentences = get_sentences(
            current_text
        )

        detected = (
            st.session_state.detected_language
        )


        st.info(
            f"🌐 Detected language: {detected}"
        )


        # PAGE NAVIGATION

        st.markdown(
            "### 📖 Page Navigation"
        )

        v1, v2, v3 = st.columns(
            [1, 2, 1]
        )

        with v1:

            if st.button(
                "← Previous",
                use_container_width=True,
                disabled=current_page == 0,
                key="voice_previous"
            ):

                st.session_state.current_page -= 1

                st.session_state.page_audio = None

                st.rerun()


        with v2:

            voice_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=current_page + 1,
                step=1,
                key="voice_page_number"
            )

            if (
                voice_page - 1
                != current_page
            ):

                st.session_state.current_page = (
                    voice_page - 1
                )

                st.session_state.page_audio = None

                st.rerun()


        with v3:

            if st.button(
                "Next →",
                use_container_width=True,
                disabled=current_page == total_pages - 1,
                key="voice_next"
            ):

                st.session_state.current_page += 1

                st.session_state.page_audio = None

                st.rerun()


        # PAGE VOICE

        st.markdown(
            f"### 📄 Page {current_page + 1} Voice"
        )

        if st.button(
            "🎙️ Generate Page Voice",
            type="primary",
            use_container_width=True,
            key="voice_generate_page"
        ):

            filename = (
                f"page_{current_page + 1}_voice.mp3"
            )

            with st.spinner(
                "Generating page voice..."
            ):

                audio = create_audio(
                    current_text,
                    filename,
                    detected
                )

            if audio:

                st.session_state.page_audio = audio

                st.success(
                    "✅ Page voice generated."
                )


        if st.session_state.page_audio:

            st.audio(
                st.session_state.page_audio
            )

            with open(
                st.session_state.page_audio,
                "rb"
            ) as audio_file:

                st.download_button(
                    "⬇️ Download Page Voice",
                    data=audio_file,
                    file_name=os.path.basename(
                        st.session_state.page_audio
                    ),
                    mime="audio/mpeg",
                    use_container_width=True,
                    key="voice_download_page"
                )


        # PARAGRAPH VOICE

        st.divider()

        st.markdown(
            "### 📝 Paragraph Voice"
        )

        for i, paragraph in enumerate(
            paragraphs
        ):

            paragraph_key = (
                f"{current_page}_{i}"
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**Paragraph {i + 1}**"
                )

                st.write(
                    paragraph
                )

                if st.button(
                    f"🎙️ Generate Paragraph {i + 1} Voice",
                    key=f"voice_paragraph_generate_{current_page}_{i}",
                    use_container_width=True
                ):

                    filename = (
                        f"page_{current_page + 1}"
                        f"_paragraph_{i + 1}.mp3"
                    )

                    with st.spinner(
                        "Generating paragraph voice..."
                    ):

                        audio = create_audio(
                            paragraph,
                            filename,
                            detected
                        )

                    if audio:

                        st.session_state.paragraph_audio[
                            paragraph_key
                        ] = audio

                        st.success(
                            "✅ Paragraph voice generated."
                        )


                if paragraph_key in (
                    st.session_state.paragraph_audio
                ):

                    audio_file = (
                        st.session_state.paragraph_audio[
                            paragraph_key
                        ]
                    )

                    st.audio(
                        audio_file
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download Paragraph Voice",
                            data=file,
                            file_name=os.path.basename(
                                audio_file
                            ),
                            mime="audio/mpeg",
                            use_container_width=True,
                            key=f"voice_paragraph_download_{current_page}_{i}"
                        )


        # SENTENCE VOICE

        st.divider()

        st.markdown(
            "### 🔤 Sentence Voice"
        )

        for i, sentence in enumerate(
            sentences
        ):

            sentence_key = (
                f"{current_page}_{i}"
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**Sentence {i + 1}**"
                )

                st.write(
                    sentence
                )

                if st.button(
                    f"🎙️ Generate Sentence {i + 1} Voice",
                    key=f"voice_sentence_generate_{current_page}_{i}",
                    use_container_width=True
                ):

                    filename = (
                        f"page_{current_page + 1}"
                        f"_sentence_{i + 1}.mp3"
                    )

                    with st.spinner(
                        "Generating sentence voice..."
                    ):

                        audio = create_audio(
                            sentence,
                            filename,
                            detected
                        )

                    if audio:

                        st.session_state.sentence_audio[
                            sentence_key
                        ] = audio

                        st.success(
                            "✅ Sentence voice generated."
                        )


                if sentence_key in (
                    st.session_state.sentence_audio
                ):

                    audio_file = (
                        st.session_state.sentence_audio[
                            sentence_key
                        ]
                    )

                    st.audio(
                        audio_file
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download Sentence Voice",
                            data=file,
                            file_name=os.path.basename(
                                audio_file
                            ),
                            mime="audio/mpeg",
                            use_container_width=True,
                            key=f"voice_sentence_download_{current_page}_{i}"
                        )

    else:

        st.info(
            "📄 Upload a PDF from Dashboard first."
        )


# ============================================================
# ANALYTICS
# ============================================================

elif navigation == "📊 Analytics":

    st.markdown(
        """
        <div class="section-title">
            📊 Document Analytics
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "View detailed statistics about your uploaded document."
    )


    # HOW TO USE

    st.markdown(
        """
        <div class="content-card">

            <div class="content-title">
                💡 How to Use Analytics
            </div>

            <div class="content-text">

                <b>01</b> — Upload a PDF from Dashboard.
                <br><br>

                <b>02</b> — The application extracts the text.
                <br><br>

                <b>03</b> — Analytics automatically count
                pages, characters, words, paragraphs and sentences.
                <br><br>

                <b>04</b> — Use these statistics to understand
                the size and structure of your document.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        full_text = "\n".join(
            pages
        )

        total_characters = len(
            full_text
        )

        total_words = len(
            full_text.split()
        )

        total_paragraphs = len(
            get_paragraphs(full_text)
        )

        total_sentences = len(
            get_sentences(full_text)
        )


        # STATISTICS

        a1, a2, a3, a4, a5 = st.columns(5)

        with a1:
            st.metric(
                "📄 Pages",
                total_pages
            )

        with a2:
            st.metric(
                "🔤 Characters",
                f"{total_characters:,}"
            )

        with a3:
            st.metric(
                "📝 Words",
                f"{total_words:,}"
            )

        with a4:
            st.metric(
                "📑 Paragraphs",
                total_paragraphs
            )

        with a5:
            st.metric(
                "🔤 Sentences",
                total_sentences
            )


        # INFORMATION

        st.markdown(
            """
            <div class="section-title">
                📋 Document Information
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="content-card">

                <div class="content-text">

                    <b>📄 File Name:</b>
                    {st.session_state.file_name}

                    <br><br>

                    <b>📄 Total Pages:</b>
                    {total_pages}

                    <br><br>

                    <b>🔤 Total Characters:</b>
                    {total_characters:,}

                    <br><br>

                    <b>📝 Total Words:</b>
                    {total_words:,}

                    <br><br>

                    <b>📑 Total Paragraphs:</b>
                    {total_paragraphs}

                    <br><br>

                    <b>🔤 Total Sentences:</b>
                    {total_sentences}

                    <br><br>

                    <b>🌐 Detected Language:</b>
                    {st.session_state.detected_language}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "📄 Upload a PDF from Dashboard first."
        )


# ============================================================
# CLEAR ALL
# IMPORTANT:
# This is OUTSIDE the sidebar.
# It appears BEFORE the footer.
# ============================================================

st.divider()

st.markdown(
    "### 🧹 Reset Workspace"
)

clear_col1, clear_col2, clear_col3 = st.columns(
    [1, 2, 1]
)

with clear_col2:

    if st.button(
        "🧹 Clear All",
        use_container_width=True,
        key="clear_all_button"
    ):

        clear_all()

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-line">

        <div class="footer-quote">
            Every word you listen to can become
            knowledge you remember.
        </div>

        <div class="footer-brand">
            🎙️ Document Voice Studio
        </div>

        <div class="footer-tagline">
            Listen • Learn • Remember • Grow
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
