# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE
# ============================================================

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS

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
       MAIN
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

    p {
        color: #cbd5e1;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #11161f !important;
        border-right: 1px solid #26303d;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-brand {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #8d99a8 !important;
        margin-bottom: 20px;
    }

    .sidebar-section {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: #788596 !important;
        margin-bottom: 10px;
    }

    .sidebar-motivation {
        background: #171e28;
        border: 1px solid #2b3645;
        border-radius: 14px;
        padding: 15px;
        margin-top: 10px;
    }

    .sidebar-motivation-text {
        color: #e2e8f0 !important;
        font-size: 13px;
        line-height: 1.6;
        font-weight: 600;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .project-title {
        color: #ffffff !important;
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 3px;
    }

    .project-subtitle {
        color: #8995a5 !important;
        font-size: 16px;
        margin-bottom: 28px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 15px;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #151b24 !important;
        border: 1px solid #303b4a !important;
        border-radius: 18px !important;
        padding: 8px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #151b24 !important;
        border: 1px dashed #566477 !important;
        border-radius: 14px !important;
        min-height: 170px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: #19212c !important;
        border-color: #60a5fa !important;
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
        background: #151b24;
        border: 1px solid #2b3543;
        border-radius: 15px;
        padding: 18px;
        min-height: 105px;
    }

    .stat-label {
        color: #8f9baa !important;
        font-size: 13px;
    }

    .stat-number {
        color: #ffffff !important;
        font-size: 27px;
        font-weight: 800;
        margin-top: 7px;
    }


    /* ========================================================
       DOCUMENT CARD
       ======================================================== */

    .document-card {
        background: #151b24;
        border: 1px solid #2b3543;
        border-radius: 16px;
        padding: 18px 20px;
        margin-top: 22px;
        margin-bottom: 20px;
    }

    .document-name {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
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
        background: #151b24;
        border: 1px solid #2b3543;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background: #171e28 !important;
        color: #f8fafc !important;
        border: 1px solid #354152 !important;
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
        background: #151b24 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #151b24 !important;
        border: 1px solid #2b3543 !important;
        border-radius: 12px !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        background: #151b24 !important;
        color: #e5e7eb !important;
        border-radius: 12px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        margin-top: 42px;
        padding-top: 22px;
        border-top: 1px solid #293442;
        text-align: center;
    }

    .footer-quote {
        color: #cbd5e1 !important;
        font-size: 14px;
        font-weight: 600;
    }

    .footer-brand {
        color: #ffffff !important;
        font-size: 13px;
        font-weight: 700;
        margin-top: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "pages": [],
    "current_page": 0,
    "file_name": "",
    "file_id": None,
    "detected_language": "en",
    "page_audio": None,
    "paragraph_audio": {},
    "sentence_audio": {}
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text):

    """
    Lightweight language detection.

    No langdetect package is required.

    Supports common Indian and international languages
    using Unicode/script detection.
    """

    if not text or not text.strip():
        return "en"

    sample = text[:5000]

    # Kannada
    if re.search(r"[\u0C80-\u0CFF]", sample):
        return "kn"

    # Hindi / Marathi / Nepali
    if re.search(r"[\u0900-\u097F]", sample):
        return "hi"

    # Telugu
    if re.search(r"[\u0C00-\u0C7F]", sample):
        return "te"

    # Tamil
    if re.search(r"[\u0B80-\u0BFF]", sample):
        return "ta"

    # Malayalam
    if re.search(r"[\u0D00-\u0D7F]", sample):
        return "ml"

    # Bengali
    if re.search(r"[\u0980-\u09FF]", sample):
        return "bn"

    # Gujarati
    if re.search(r"[\u0A80-\u0AFF]", sample):
        return "gu"

    # Punjabi
    if re.search(r"[\u0A00-\u0A7F]", sample):
        return "pa"

    # Arabic / Urdu
    if re.search(r"[\u0600-\u06FF]", sample):
        return "ar"

    # Japanese
    if re.search(r"[\u3040-\u30FF]", sample):
        return "ja"

    # Korean
    if re.search(r"[\uAC00-\uD7AF]", sample):
        return "ko"

    # Chinese
    if re.search(r"[\u4E00-\u9FFF]", sample):
        return "zh-CN"

    # Cyrillic
    if re.search(r"[\u0400-\u04FF]", sample):
        return "ru"

    # Latin fallback
    return "en"


# ============================================================
# GOOGLE TTS LANGUAGE MAP
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

    "zh-CN": "zh-CN",
    "zh-TW": "zh-TW",

    "id": "id",
    "tr": "tr",
    "vi": "vi",
    "th": "th"
}


# ============================================================
# CLEAR ALL
# ============================================================

def clear_all():

    for key, value in DEFAULTS.items():

        if isinstance(value, list):
            st.session_state[key] = []

        elif isinstance(value, dict):
            st.session_state[key] = {}

        else:
            st.session_state[key] = value

    if "document_uploader" in st.session_state:
        del st.session_state["document_uploader"]


# ============================================================
# EXTRACT PDF
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
# PARAGRAPHS
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
# SENTENCES
# ============================================================

def get_sentences(text):

    if not text or not text.strip():
        return []

    sentences = re.split(
        r"(?<=[.!?।！？])\s+",
        text
    )

    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


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

        language = LANGUAGE_MAP.get(
            language,
            "en"
        )

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.save(filename)

        return filename

    except Exception as e:

        st.error(
            f"Voice generation error: {e}"
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

    # --------------------------------------------------------
    # SIDEBAR MOTIVATION
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-section">
            ✨ DAILY THOUGHT
        </div>

        <div class="sidebar-motivation">

            <div class="sidebar-motivation-text">
                Turn listening into learning,
                and learning into progress.
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
# DASHBOARD UPLOAD
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
        "Drag and drop your PDF here",
        type=["pdf"],
        key="document_uploader"
    )

    if uploaded_file is not None:

        current_file_id = (
            uploaded_file.name,
            uploaded_file.size
        )

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

                    complete_text = " ".join(pages)

                    st.session_state.detected_language = (
                        detect_language(
                            complete_text
                        )
                    )

                st.success(
                    "✅ Document loaded successfully."
                )

            except Exception as e:

                st.error(
                    f"❌ Could not read PDF: {e}"
                )


# ============================================================
# IF NO DOCUMENT
# ============================================================

if not st.session_state.pages:

    if navigation == "🏠 Dashboard":

        st.info(
            "📄 Upload a PDF above to start using Document Voice Studio."
        )

    else:

        st.info(
            "📄 Please upload a PDF from the Dashboard first."
        )

    # ========================================================
    # CLEAR ALL
    # ========================================================

    st.divider()

    clear_col1, clear_col2, clear_col3 = st.columns(
        [2, 2, 2]
    )

    with clear_col2:

        if st.button(
            "🧹 Clear All",
            use_container_width=True
        ):

            clear_all()

            st.rerun()


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer-line">

            <div class="footer-quote">
                Every word you listen to can become knowledge you remember.
            </div>

            <div class="footer-brand">
                🎙️ Document Voice Studio
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# DOCUMENT DATA
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

character_count = len(current_text)

word_count = len(
    current_text.split()
)


# ============================================================
# DASHBOARD DOCUMENT DETAILS
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

    full_text = " ".join(pages)

    all_paragraphs = get_paragraphs(
        full_text
    )

    all_sentences = get_sentences(
        full_text
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
                    {len(full_text):,}
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
                    {len(full_text.split()):,}
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
                    {len(all_paragraphs)}
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
                    {len(all_sentences)}
                </div>

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
                {len(full_text):,} Characters
                •
                {len(full_text.split()):,} Words
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
            disabled=current_page == 0
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
            step=1
        )

        if (
            selected_page - 1
            != current_page
        ):

            st.session_state.current_page = (
                selected_page - 1
            )

            st.session_state.page_audio = None

            st.rerun()

    with col3:

        if st.button(
            "Next →",
            use_container_width=True,
            disabled=current_page == total_pages - 1
        ):

            st.session_state.current_page += 1

            st.session_state.page_audio = None

            st.rerun()


# ============================================================
# DOCUMENT
# ============================================================

if navigation == "📄 Document":

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
        disabled=True
    )

    st.markdown(
        "### 📊 Page Statistics"
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
            len(paragraphs)
        )

    with c4:
        st.metric(
            "Sentences",
            len(sentences)
        )

    st.markdown(
        "### 📝 Paragraphs"
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

    st.markdown(
        "### 🔤 Sentences"
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

    detected_language = (
        st.session_state.detected_language
    )

    st.info(
        f"🌐 Detected language: **{detected_language}**"
    )


    # ========================================================
    # PAGE VOICE
    # ========================================================

    st.markdown(
        f"### 📖 Page {current_page + 1} Voice"
    )

    if st.button(
        "🎙️ Generate Page Voice",
        type="primary",
        use_container_width=True
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
                data=audio_file,
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
        "### 📝 Paragraph Voice"
    )

    for i, paragraph in enumerate(
        paragraphs
    ):

        with st.container(border=True):

            st.markdown(
                f"**Paragraph {i + 1}**"
            )

            st.write(
                paragraph
            )

            paragraph_key = (
                f"{current_page}_{i}"
            )

            if st.button(
                f"🎙️ Generate Paragraph {i + 1} Voice",
                key=f"paragraph_{current_page}_{i}",
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
                        key=f"download_paragraph_{current_page}_{i}",
                        use_container_width=True
                    )


    # ========================================================
    # SENTENCE VOICE
    # ========================================================

    st.divider()

    st.markdown(
        "### 🔤 Sentence Voice"
    )

    for i, sentence in enumerate(
        sentences
    ):

        with st.container(border=True):

            st.markdown(
                f"**Sentence {i + 1}**"
            )

            st.write(
                sentence
            )

            sentence_key = (
                f"{current_page}_{i}"
            )

            if st.button(
                f"🎙️ Generate Sentence {i + 1} Voice",
                key=f"sentence_{current_page}_{i}",
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
                        key=f"download_sentence_{current_page}_{i}",
                        use_container_width=True
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
        "### 📋 Document Information"
    )

    st.markdown(
        f"""
        <div class="content-card">

        <p>
        <b>File:</b>
        {st.session_state.file_name}
        </p>

        <p>
        <b>Total Pages:</b>
        {total_pages}
        </p>

        <p>
        <b>Total Characters:</b>
        {total_characters:,}
        </p>

        <p>
        <b>Total Words:</b>
        {total_words:,}
        </p>

        <p>
        <b>Total Paragraphs:</b>
        {total_paragraphs}
        </p>

        <p>
        <b>Total Sentences:</b>
        {total_sentences}
        </p>

        <p>
        <b>Detected Language:</b>
        {st.session_state.detected_language}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CLEAR ALL
# ============================================================
# IMPORTANT:
# Clear All is BEFORE the footer.
# It is NOT inside the sidebar.

st.divider()

clear_col1, clear_col2, clear_col3 = st.columns(
    [2, 2, 2]
)

with clear_col2:

    if st.button(
        "🧹 Clear All",
        use_container_width=True
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
            Every word you listen to can become knowledge you remember.
        </div>

        <div class="footer-brand">
            🎙️ Document Voice Studio
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
