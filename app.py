# ============================================================
# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE
# ============================================================

import os
import re
import hashlib

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
from langdetect import detect


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
# MODERN DARK UI
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
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    p, span, label {
        color: #cbd5e1;
    }

    hr {
        border-color: #293442 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #10151d !important;
        border-right: 1px solid #27313e;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-product {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 800;
        margin-top: 5px;
    }

    .sidebar-subtitle {
        color: #7f8b9a !important;
        font-size: 11px;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    .sidebar-section {
        color: #7f8b9a !important;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: 10px;
    }

    .motivation-card {
        background: #151b24;
        border: 1px solid #293442;
        border-radius: 12px;
        padding: 12px;
        margin-top: 8px;
    }

    .motivation-title {
        color: #ffffff !important;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.7px;
        margin-bottom: 6px;
    }

    .motivation-text {
        color: #9ca8b7 !important;
        font-size: 11px;
        line-height: 1.5;
    }

    .sidebar-bottom {
        color: #667384 !important;
        font-size: 10px;
        text-align: center;
        margin-top: 18px;
    }


    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .project-title {
        color: #ffffff !important;
        font-size: 40px;
        font-weight: 850;
        letter-spacing: -1.2px;
        margin-bottom: 4px;
    }

    .project-subtitle {
        color: #8995a5 !important;
        font-size: 15px;
        margin-bottom: 28px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 21px;
        font-weight: 800;
        margin-top: 22px;
        margin-bottom: 14px;
    }


    /* ========================================================
       UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #141a22 !important;
        border: 1px solid #303b49 !important;
        border-radius: 17px !important;
        padding: 8px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #141a22 !important;
        border: 1px dashed #536173 !important;
        border-radius: 13px !important;
        min-height: 165px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: #19212b !important;
        border-color: #60a5fa !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #e5e7eb !important;
    }

    [data-testid="stFileUploaderDropzone"] small {
        color: #8b97a7 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .stat-card {
        background: #141a22;
        border: 1px solid #293442;
        border-radius: 14px;
        padding: 17px;
        min-height: 95px;
    }

    .stat-label {
        color: #8490a0 !important;
        font-size: 12px;
    }

    .stat-number {
        color: #ffffff !important;
        font-size: 26px;
        font-weight: 850;
        margin-top: 5px;
    }

    .document-card {
        background: #141a22;
        border: 1px solid #293442;
        border-radius: 15px;
        padding: 17px 19px;
        margin-top: 18px;
    }

    .document-name {
        color: #ffffff !important;
        font-size: 16px;
        font-weight: 750;
    }

    .document-info {
        color: #8490a0 !important;
        font-size: 12px;
        margin-top: 5px;
    }

    .content-card {
        background: #141a22;
        border: 1px solid #293442;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .content-title {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .content-text {
        color: #b8c2cf !important;
        font-size: 13px;
        line-height: 1.65;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background: #171e27 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
        border-radius: 9px !important;
        min-height: 40px;
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
        background: #141a22 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #141a22 !important;
        border: 1px solid #293442 !important;
        border-radius: 11px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        margin-top: 38px;
        padding: 18px 10px 5px 10px;
        border-top: 1px solid #293442;
        text-align: center;
    }

    .footer-quote {
        color: #9da9b8 !important;
        font-size: 12px;
        font-weight: 500;
    }

    .footer-brand {
        color: #ffffff !important;
        font-size: 12px;
        font-weight: 750;
        margin-top: 7px;
    }

    .footer-tagline {
        color: #596575 !important;
        font-size: 10px;
        margin-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "pages": [],
    "current_page": 0,
    "file_name": "",
    "file_id": None,
    "detected_language": "en",
    "page_audio": None,
    "paragraph_audio": {},
    "sentence_audio": {}
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CLEAR ALL
# IMPORTANT:
# DO NOT MODIFY st.session_state.document_uploader
# ============================================================

def clear_all():

    st.session_state.pages = []
    st.session_state.current_page = 0
    st.session_state.file_name = ""
    st.session_state.file_id = None
    st.session_state.detected_language = "en"
    st.session_state.page_audio = None
    st.session_state.paragraph_audio = {}
    st.session_state.sentence_audio = {}


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text.strip())
        else:
            pages.append("")

    return pages


# ============================================================
# PARAGRAPH EXTRACTION
# ============================================================

def get_paragraphs(text):

    if not text or not text.strip():
        return []

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    paragraphs = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

    if not paragraphs:
        return [text.strip()]

    return paragraphs


# ============================================================
# SENTENCE EXTRACTION
# ============================================================

def get_sentences(text):

    if not text or not text.strip():
        return []

    sentences = re.split(
        r"(?<=[.!?।！？])\s+",
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return sentences


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text):

    try:

        if not text or not text.strip():
            return "en"

        return detect(
            text[:3000]
        )

    except Exception:
        return "en"


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
# CREATE VOICE
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
            f"Voice generation error: {error}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-product">
            🎙️ Document Voice Studio
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

    # --------------------------------------------------------
    # MOTIVATION
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="motivation-card">

            <div class="motivation-title">
                💡 DAILY THOUGHT
            </div>

            <div class="motivation-text">
                Every word you listen to can become
                knowledge you remember.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-bottom">
            Listen • Learn • Remember • Grow
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
# DASHBOARD — UPLOAD
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        """
        <div class="section-title">
            📄 Upload Your Document
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your PDF document",
        type=["pdf"],
        key="document_uploader"
    )

    # --------------------------------------------------------
    # PROCESS FILE
    # --------------------------------------------------------

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        current_file_id = hashlib.md5(
            file_bytes
        ).hexdigest()

        if (
            st.session_state.file_id
            != current_file_id
        ):

            try:

                with st.spinner(
                    "Reading your document..."
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
                        current_file_id
                    )

                    st.session_state.page_audio = None

                    st.session_state.paragraph_audio = {}

                    st.session_state.sentence_audio = {}

                    complete_text = " ".join(
                        pages
                    )

                    st.session_state.detected_language = (
                        detect_language(
                            complete_text
                        )
                    )

                st.success(
                    "✅ Document loaded successfully."
                )

            except Exception as error:

                st.error(
                    f"❌ Could not read PDF: {error}"
                )


# ============================================================
# NO DOCUMENT
# ============================================================

if not st.session_state.pages:

    if navigation == "🏠 Dashboard":

        st.info(
            "📄 Upload a PDF above to start."
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

    else:

        st.info(
            "📄 Please upload a PDF from the Dashboard first."
        )


# ============================================================
# FOOTER FUNCTION
# ============================================================

def show_footer():

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


# ============================================================
# STOP IF NO DOCUMENT
# ============================================================

if not st.session_state.pages:

    show_footer()

    st.stop()


# ============================================================
# DOCUMENT VARIABLES
# ============================================================

pages = st.session_state.pages

total_pages = len(pages)

current_page = st.session_state.current_page

current_text = pages[current_page]

paragraphs = get_paragraphs(
    current_text
)

sentences = get_sentences(
    current_text
)

character_count = len(
    current_text
)

word_count = len(
    current_text.split()
)

paragraph_count = len(
    paragraphs
)

sentence_count = len(
    sentences
)

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


# ============================================================
# DASHBOARD DOCUMENT SUMMARY
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        """
        <div class="section-title">
            YOUR DOCUMENT
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

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

    with c2:

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

    with c3:

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

    with c4:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">
                    📑 Paragraphs
                </div>

                <div class="stat-number">
                    {total_paragraphs}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c5:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">
                    🔤 Sentences
                </div>

                <div class="stat-number">
                    {total_sentences}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # CURRENT DOCUMENT
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # FILE INFORMATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CONTENT INFORMATION
    # --------------------------------------------------------

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
                {total_paragraphs}

                <br><br>

                <b>Sentences:</b>
                {total_sentences}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE NAVIGATION
# ============================================================

if navigation in [
    "🏠 Dashboard",
    "📄 Document",
    "🎙️ Voice Studio"
]:

    st.markdown(
        """
        <div class="section-title">
            📖 Page Navigation
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col1:

        if st.button(
            "← Previous",
            use_container_width=True,
            disabled=current_page == 0,
            key="previous_page"
        ):

            st.session_state.current_page -= 1

            st.session_state.page_audio = None

            st.rerun()

    with col2:

        selected_page = st.number_input(
            "Current Page",
            min_value=1,
            max_value=total_pages,
            value=current_page + 1,
            step=1,
            key="page_selector"
        )

        if selected_page - 1 != current_page:

            st.session_state.current_page = (
                selected_page - 1
            )

            st.session_state.page_audio = None

            st.rerun()

    with col3:

        if st.button(
            "Next →",
            use_container_width=True,
            disabled=current_page == total_pages - 1,
            key="next_page"
        ):

            st.session_state.current_page += 1

            st.session_state.page_audio = None

            st.rerun()


# ============================================================
# PAGE SECTION
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        f"""
        <div class="content-card">

            <div class="content-title">
                📖 Page {current_page + 1}
            </div>

            <div class="content-text">
                Current document page content
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.text_area(
        "Page Content",
        value=current_text,
        height=300,
        disabled=True,
        key="dashboard_page_content"
    )


# ============================================================
# DOCUMENT PAGE
# ============================================================

elif navigation == "📄 Document":

    st.markdown(
        f"""
        <div class="section-title">
            📄 Page {current_page + 1}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        f"Document: {st.session_state.file_name}"
    )

    st.text_area(
        "Page Content",
        value=current_text,
        height=450,
        disabled=True,
        key="document_page_content"
    )


    # --------------------------------------------------------
    # PAGE STATISTICS
    # --------------------------------------------------------

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
            f"{character_count:,}"
        )

    with c2:
        st.metric(
            "Words",
            f"{word_count:,}"
        )

    with c3:
        st.metric(
            "Paragraphs",
            paragraph_count
        )

    with c4:
        st.metric(
            "Sentences",
            sentence_count
        )


    # --------------------------------------------------------
    # PARAGRAPHS
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📝 Paragraphs
        </div>
        """,
        unsafe_allow_html=True
    )

    if paragraphs:

        for i, paragraph in enumerate(
            paragraphs
        ):

            with st.expander(
                f"Paragraph {i + 1}"
            ):

                st.write(
                    paragraph
                )

    else:

        st.info(
            "No paragraphs found."
        )


    # --------------------------------------------------------
    # SENTENCES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            🔤 Sentences
        </div>
        """,
        unsafe_allow_html=True
    )

    if sentences:

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
            "No sentences found."
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

    detected_language = (
        st.session_state.detected_language
    )

    st.info(
        f"🌐 Detected language: {detected_language}"
    )


    # ========================================================
    # PAGE VOICE
    # ========================================================

    st.markdown(
        f"""
        <div class="section-title">
            📖 Page {current_page + 1} Voice
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🎙️ Generate Page Voice",
        type="primary",
        use_container_width=True,
        key="generate_page_voice"
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
                detected_language
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
                data=audio_file.read(),
                file_name=os.path.basename(
                    st.session_state.page_audio
                ),
                mime="audio/mpeg",
                use_container_width=True,
                key="download_page_voice"
            )


    # ========================================================
    # PARAGRAPH VOICE
    # ========================================================

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            📝 Paragraph Voice
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
                key=f"paragraph_button_{current_page}_{i}",
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
                        detected_language
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
                        data=file.read(),
                        file_name=os.path.basename(
                            audio_file
                        ),
                        mime="audio/mpeg",
                        use_container_width=True,
                        key=f"download_paragraph_{current_page}_{i}"
                    )


    # ========================================================
    # SENTENCE VOICE
    # ========================================================

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            🔤 Sentence Voice
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
                key=f"sentence_button_{current_page}_{i}",
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
                        detected_language
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
                        data=file.read(),
                        file_name=os.path.basename(
                            audio_file
                        ),
                        mime="audio/mpeg",
                        use_container_width=True,
                        key=f"download_sentence_{current_page}_{i}"
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

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📄 Pages",
            total_pages
        )

    with c2:
        st.metric(
            "🔤 Characters",
            f"{total_characters:,}"
        )

    with c3:
        st.metric(
            "📝 Words",
            f"{total_words:,}"
        )

    with c4:
        st.metric(
            "🔤 Sentences",
            total_sentences
        )

    st.divider()

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
                {total_paragraphs}

                <br><br>

                <b>Sentences:</b>
                {total_sentences}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CLEAR ALL
# IMPORTANT:
# This button is OUTSIDE the sidebar.
# It does NOT change the file uploader state directly.
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8b97a7;
        font-size:12px;
        margin-bottom:10px;
    ">
        Reset your current workspace
    </div>
    """,
    unsafe_allow_html=True
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

show_footer()
