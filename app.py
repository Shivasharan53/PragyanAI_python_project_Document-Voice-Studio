
# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
from langdetect import detect

import os
import re

# PAGE CONFIG

st.set_page_config(
    page_title="Document Voice Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MODERN DARK THEME

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {
        background: #0b0f14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       GENERAL TEXT
       ======================================================== */

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
        background: #11151c !important;
        border-right: 1px solid #29313d;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-brand {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #8995a5 !important;
        margin-bottom: 20px;
    }

    .sidebar-section {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #8995a5 !important;
        margin-bottom: 12px;
    }

    /* Clean motivation - no box */
    .motivation-card {
        background: transparent;
        border: none;
        padding: 4px 0;
        margin-top: 8px;
    }

    .motivation-text {
        color: #aeb8c5 !important;
        font-size: 13px;
        line-height: 1.6;
        font-style: italic;
    }


    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .project-title {
        color: #ffffff !important;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .project-subtitle {
        color: #8995a5 !important;
        font-size: 16px;
        margin-bottom: 30px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #151a22 !important;
        border: 1px solid #303a48 !important;
        border-radius: 18px !important;
        padding: 8px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #151a22 !important;
        border: 1px dashed #526071 !important;
        border-radius: 14px !important;
        min-height: 175px !important;
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
        font-weight: 650 !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #1d4ed8 !important;
    }


    /* ========================================================
       STAT CARDS
       ======================================================== */

    .stat-card {
        background: #151a22;
        border: 1px solid #293442;
        border-radius: 16px;
        padding: 18px;
        min-height: 105px;
    }

    .stat-label {
        color: #8995a5 !important;
        font-size: 13px;
    }

    .stat-number {
        color: #ffffff !important;
        font-size: 28px;
        font-weight: 800;
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
        margin-top: 22px;
        margin-bottom: 20px;
    }

    .document-name {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
    }

    .document-info {
        color: #8995a5 !important;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ========================================================
       CONTENT CARDS
       ======================================================== */

    .content-card {
        background: #151a22;
        border: 1px solid #293442;
        border-radius: 17px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .content-card h3 {
        color: #ffffff !important;
    }

    .content-card p {
        color: #c7d0dc !important;
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
        color: #ffffff !important;
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
       NUMBER INPUT
       ======================================================== */

    div[data-testid="stNumberInput"] input {
        background: #151a22 !important;
        color: #ffffff !important;
        border: 1px solid #344050 !important;
    }


    /* ========================================================
       EXPANDERS
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
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        background: #151a22 !important;
        color: #e5e7eb !important;
        border-radius: 12px !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: #293442 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        margin-top: 35px;
        padding-top: 18px;
        border-top: 1px solid #293442;
        text-align: center;
        color: #8995a5 !important;
        font-size: 13px;
    }

    .footer-line b {
        color: #dce3eb !important;
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


# ============================================================
# CLEAR ALL
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

    if not text.strip():
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
        paragraphs = [text.strip()]

    return paragraphs


# ============================================================
# SENTENCES
# ============================================================

def get_sentences(text):

    if not text.strip():
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

        if not text.strip():
            return "en"

        return detect(
            text[:3000]
        )

    except:

        return "en"


# ============================================================
# SUPPORTED LANGUAGES
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
# CREATE AUDIO
# ============================================================

def create_audio(
    text,
    filename,
    language
):

    if not text.strip():
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

    s
