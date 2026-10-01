```python
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
# CSS - MODERN DARK DASHBOARD
# ============================================================

st.markdown(
    """
    <style>

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

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: #11151c !important;
        border-right: 1px solid #293442;
    }

    .sidebar-brand {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff !important;
    }

    .sidebar-subtitle {
        color: #8995a5 !important;
        font-size: 13px;
        margin-top: 3px;
    }

    .sidebar-heading {
        color: #8995a5 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.4px;
        margin-bottom: 10px;
    }

    .motivation-text {
        color: #aeb8c5 !important;
        font-size: 13px;
        line-height: 1.6;
        font-style: italic;
    }

    /* ================= HEADER ================= */

    .project-title {
        color: #ffffff !important;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .project-subtitle {
        color: #8995a5 !important;
        font-size: 16px;
        margin-top: 5px;
        margin-bottom: 28px;
    }

    /* ================= SECTION ================= */

    .section-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* ================= UPLOADER ================= */

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
        min-height: 170px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: #19212b !important;
        border-color: #60a5fa !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #e5e7eb !important;
    }

    [data-testid="stFileUploaderDro]()
```
