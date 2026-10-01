import os
import re
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0b0f14;
    color: #f5f7fa;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 35px;
    padding-bottom: 30px;
}

section[data-testid="stSidebar"] {
    background-color: #11161d;
    border-right: 1px solid #28313d;
}

.sidebar-brand {
    color: #ffffff;
    font-size: 25px;
    font-weight: 800;
}

.sidebar-subtitle {
    color: #8995a5;
    font-size: 13px;
    margin-top: 4px;
}

.sidebar-heading {
    color: #718096;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 12px;
    margin-bottom: 10px;
}

.motivation-text {
    color: #aeb8c5;
    font-size: 13px;
    line-height: 1.7;
    font-style: italic;
}

.project-title {
    color: #ffffff;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 4px;
}

.project-subtitle {
    color: #8d99a8;
    font-size: 16px;
    margin-bottom: 30px;
}

.section-title {
    color: #ffffff;
    font-size: 22px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 15px;
}

.stat-card {
    background-color: #151b23;
    border: 1px solid #2b3542;
    border-radius: 15px;
    padding: 18px;
    min-height: 105px;
}

.stat-label {
    color: #8995a5;
    font-size: 13px;
}

.stat-number {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

.document-card {
    background-color: #151b23;
    border: 1px solid #2b3542;
    border-radius: 15px;
    padding: 18px 20px;
    margin-top: 22px;
    margin-bottom: 25px;
}

.document-name {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
}

.document-info {
    color: #8995a5;
    font-size: 13px;
    margin-top: 5px;
}

.content-card {
    background-color: #151b23;
    border: 1px solid #2b3542;
    border-radius: 15px;
    padding: 22px;
    margin-bottom: 18px;
}

.footer-line {
    border-top: 1px solid #293442;
    margin-top: 35px;
    padding-top: 18px;
    text-align: center;
    color: #8995a5;
    font-size: 13px;
}

.footer-line b {
    color: #dce3eb;
}

[data-testid="stFileUploader"] {
    background-color: #151b23;
    border: 1px solid #303b49;
    border-radius: 17px;
    padding: 8px;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #151b23;
    border: 1px dashed #526071;
    border-radius: 13px;
    min-height: 165px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background-color: #19212b;
    border-color: #60a5fa;
}

[data-testid="stFileUploaderDropzoneInstructions"] * {
    color: #e5e7eb !important;
}

.stButton > button {
    background-color: #171e27 !important;
    color: #ffffff !important;
    border: 1px solid #354151 !important;
    border-radius: 10px !important;
    min-height: 42px;
    font-weight: 650 !important;
}

.stButton > button:hover {
    background-color: #222c38 !important;
    border-color: #60a5fa !important;
}

textarea {
    background-color: #151b23 !important;
    color: #ffffff !important;
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

if "language" not in st.session_state:
    st.session_state.language = "en"

if "page_audio" not in st.session_state:
    st.session_state.page_audio = None

if "paragraph_audio" not in st.session_state:
    st.session_state.paragraph_audio = {}

if "sentence_audio" not in st.session_state:
    st.session_state.sentence_audio = {}


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
    "id": "id",
    "tr": "tr",
    "vi": "vi",
    "th": "th",
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW"
}


# ============================================================
# CLEAR ALL
# ============================================================

def clear_all():
    st.session_state.pages = []
    st.session_state.current_page = 0
    st.session_state.file_name = ""
    st.session_state.file_id = None
    st.session_state.language = "en"
    st.session_state.page_audio = None
    st.session_state.paragraph_audio = {}
    st.session_state.sentence_audio = {}


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

    result = re.split(r"\n\s*\n", text)

    result = [
        item.strip()
        for item in result
        if item.strip()
    ]

    if not result:
        return [text.strip()]

    return result


# ============================================================
# SENTENCES
