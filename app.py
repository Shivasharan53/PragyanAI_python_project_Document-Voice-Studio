# ============================================================
# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE
# ============================================================

import os
import re
import uuid

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
# DARK MODERN THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       APP BACKGROUND
       ====================================================== */

    .stApp {
        background-color: #0b0f14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: #11151c !important;
        border-right: 1px solid #29313d;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #ffffff !important;
    }

    p {
        color: #cbd5e1;
    }


    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {
        background-color: #151a22 !important;
        border: 1px solid #344050 !important;
        border-radius: 16px !important;
        padding: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #151a22 !important;
        border: 1px dashed #526071 !important;
        border-radius: 14px !important;
        min-height: 170px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background-color: #19212b !important;
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
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 9px !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        background-color: #171d26 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
        border-radius: 10px !important;
        min-height: 42px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background-color: #202a37 !important;
        border-color: #60a5fa !important;
    }

    button[kind="primary"] {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }


    /* ======================================================
       TEXT AREAS
       ====================================================== */

    textarea {
        background-color: #151a22 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
    }


    /* ======================================================
       NUMBER INPUT
       ====================================================== */

    div[data-testid="stNumberInput"] input {
        background-color: #151a22 !important;
        color: #ffffff !important;
        border: 1px solid #344050 !important;
    }


    /* ======================================================
       SELECT / RADIO
       ====================================================== */

    div[data-baseweb="select"] {
        background-color: #151a22 !important;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background-color: #151a22;
        border: 1px solid #293442;
        border-radius: 14px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    [data-testid="stExpander"] {
        background-color: #151a22 !important;
        border: 1px solid #293442 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }


    /* ======================================================
       SIDEBAR MOTIVATION BOX
       ====================================================== */

    .motivation-box {
        background-color: #151a22;
        border: 1px solid #293442;
        border-radius: 14px;
        padding: 15px;
        margin-top: 10px;
    }

    .motivation-heading {
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
    }

    .motivation-message {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 7px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 600;
        margin-top: 15px;
    }

    .footer-brand {
        text-align: center;
        color: #ffffff;
        font-size: 14px;
        font-weight: 700;
        margin-top: 8px;
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
    "sentence_audio": {},
}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


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
        p.strip()
        for p in paragraphs
        if p.strip()
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
            text[:5000]
        )

        if detected in LANGUAGE_MAP:

            return detected

        return "en"

    except Exception:

        return "en"


# ============================================================
# CREATE AUDIO
# ============================================================

def create_audio(
    text,
    prefix,
    language
):

    if not text or not text.strip():

        return None

    try:

        gtts_language = LANGUAGE_MAP.get(
            language,
            "en"
        )

        unique_id = uuid.uuid4().hex[:8]

        filename = (
            f"{prefix}_{unique_id}.mp3"
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
        "## 🎙️ Document Voice"
    )

    st.caption(
        "Document-Audio Studio"
    )

    st.divider()

    st.markdown(
        "### NAVIGATION"
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
        "### 💡 DAILY THOUGHT"
    )

    st.markdown(
        """
        <div class="motivation-box">

            <div class="motivation-heading">
                Keep learning.
            </div>

            <div class="motivation-message">
                Every step you take in learning
                turns into progress.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption(
        "🎙️ Document Voice Studio"
    )

    st.caption(
        "PDF → Text → Voice"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "🎙️ Document Voice Studio"
)

st.caption(
    "Transform your documents into voice"
)


# ============================================================
# DASHBOARD
# ============================================================

if navigation == "🏠 Dashboard":

    st.header(
        "📄 Upload Your Document"
    )

    st.write(
        "Upload a PDF to read it page by page "
        "and convert its content into voice."
    )

    uploaded_file = st.file_uploader(
        "Upload your PDF document",
        type=["pdf"],
        key="document_uploader"
    )

    # --------------------------------------------------------
    # PROCESS DOCUMENT
    # --------------------------------------------------------

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
                        current_file_id
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

            except Exception as e:

                st.error(
                    f"❌ Could not read PDF: {e}"
                )


# ============================================================
# NO DOCUMENT
# ============================================================

if not st.session_state.pages:

    if navigation == "🏠 Dashboard":

        st.info(
            "📄 Upload a PDF above to start using "
            "Document Voice Studio."
        )

        st.subheader(
            "How it works"
        )

        st.write(
            "01  •  Upload your PDF document"
        )

        st.write(
            "02  •  View your document page by page"
        )

        st.write(
            "03  •  Read individual paragraphs"
        )

        st.write(
            "04  •  Convert paragraphs and sentences into voice"
        )

        st.write(
            "05  •  Play and download your audio"
        )

    else:

        st.info(
            "📄 Please upload a PDF from the Dashboard first."
        )


    # --------------------------------------------------------
    # CLEAR ALL
    # --------------------------------------------------------

    st.divider()

    clear_col1, clear_col2, clear_col3 = st.columns(
        [1, 2, 1]
    )

    with clear_col2:

        if st.button(
            "🧹 Clear All",
            use_container_width=True
        ):

            clear_all()

            st.rerun()


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        """
        <div class="footer-text">
            Every word you listen to can become
            knowledge you remember.
        </div>

        <div class="footer-brand">
            🎙️ Document Voice Studio
        </div>
        """,
        unsafe_allow_html=True
    )

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

page_characters = len(
    current_text
)

page_words = len(
    current_text.split()
)

page_paragraphs = len(
    paragraphs
)

page_sentences = len(
    sentences
)


# ============================================================
# COMPLETE DOCUMENT STATISTICS
# ============================================================

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
# DASHBOARD DETAILS
# ============================================================

if navigation == "🏠 Dashboard":

    st.header(
        "YOUR DOCUMENT"
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

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
            "📑 Paragraphs",
            total_paragraphs
        )

    with c5:

        st.metric(
            "🔤 Sentences",
            total_sentences
        )

    # --------------------------------------------------------
    # DOCUMENT INFORMATION
    # --------------------------------------------------------

    st.subheader(
        "📄 Current Document"
    )

    with st.container(border=True):

        st.markdown(
            f"### 📄 {st.session_state.file_name}"
        )

        st.caption(
            f"{total_pages} Pages  •  "
            f"{total_characters:,} Characters  •  "
            f"{total_words:,} Words"
        )

        st.caption(
            f"{total_paragraphs} Paragraphs  •  "
            f"{total_sentences} Sentences"
        )

        st.caption(
            f"🌐 Detected Language: "
            f"{st.session_state.detected_language}"
        )


# ============================================================
# PAGE NAVIGATION
# ============================================================

if navigation in [
    "🏠 Dashboard",
    "📄 Document",
    "🎙️ Voice Studio"
]:

    st.divider()

    st.subheader(
        "📖 Page Navigation"
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    # --------------------------------------------------------
    # PREVIOUS
    # --------------------------------------------------------

    with col1:

        if st.button(
            "← Previous",
            use_container_width=True,
            disabled=current_page == 0
        ):

            st.session_state.current_page -= 1

            st.session_state.page_audio = None

            st.rerun()

    # --------------------------------------------------------
    # PAGE NUMBER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # NEXT
    # --------------------------------------------------------

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
# DOCUMENT PAGE
# ============================================================

if navigation == "📄 Document":

    st.header(
        f"📄 Page {current_page + 1}"
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

    st.subheader(
        "📊 Page Statistics"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Characters",
            f"{page_characters:,}"
        )

    with c2:

        st.metric(
            "Words",
            f"{page_words:,}"
        )

    with c3:

        st.metric(
            "Paragraphs",
            page_paragraphs
        )

    with c4:

        st.metric(
            "Sentences",
            page_sentences
        )

    # --------------------------------------------------------
    # PARAGRAPHS
    # --------------------------------------------------------

    st.subheader(
        "📝 Paragraphs"
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

        st.warning(
            "No paragraphs found on this page."
        )

    # --------------------------------------------------------
    # SENTENCES
    # --------------------------------------------------------

    st.subheader(
        "🔤 Sentences"
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

        st.warning(
            "No sentences found on this page."
        )


# ============================================================
# VOICE STUDIO
# ============================================================

elif navigation == "🎙️ Voice Studio":

    st.header(
        "🎙️ Voice Studio"
    )

    st.caption(
        "Convert your document content into voice."
    )

    detected_language = (
        st.session_state.detected_language
    )

    st.info(
        f"🌐 Detected language: "
        f"**{detected_language}**"
    )

    # ========================================================
    # PAGE VOICE
    # ========================================================

    st.subheader(
        f"📖 Page {current_page + 1} Voice"
    )

    if st.button(
        "🎙️ Generate Page Voice",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Generating page voice..."
        ):

            audio = create_audio(
                current_text,
                f"page_{current_page + 1}",
                detected_language
            )

        if audio:

            st.session_state.page_audio = audio

            st.success(
                "✅ Page voice generated successfully."
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

    st.subheader(
        "📝 Paragraph Voice"
    )

    if paragraphs:

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
                    key=f"paragraph_button_{current_page}_{i}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "Generating paragraph voice..."
                    ):

                        audio = create_audio(
                            paragraph,
                            f"page_{current_page + 1}_paragraph_{i + 1}",
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
                            key=f"download_paragraph_{current_page}_{i}",
                            use_container_width=True
                        )

    else:

        st.warning(
            "No paragraphs found on this page."
        )

    # ========================================================
    # SENTENCE VOICE
    # ========================================================

    st.divider()

    st.subheader(
        "🔤 Sentence Voice"
    )

    if sentences:

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
                    key=f"sentence_button_{current_page}_{i}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "Generating sentence voice..."
                    ):

                        audio = create_audio(
                            sentence,
                            f"page_{current_page + 1}_sentence_{i + 1}",
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
                            key=f"download_sentence_{current_page}_{i}",
                            use_container_width=True
                        )

    else:

        st.warning(
            "No sentences found on this page."
        )


# ============================================================
# ANALYTICS
# ============================================================

elif navigation == "📊 Analytics":

    st.header(
        "📊 Document Analytics"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

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
            "📑 Paragraphs",
            total_paragraphs
        )

    with c5:

        st.metric(
            "🔤 Sentences",
            total_sentences
        )

    st.divider()

    st.subheader(
        "📋 Document Information"
    )

    with st.container(border=True):

        st.write(
            f"📄 **File:** "
            f"{st.session_state.file_name}"
        )

        st.write(
            f"📑 **Pages:** "
            f"{total_pages}"
        )

        st.write(
            f"🔤 **Characters:** "
            f"{total_characters:,}"
        )

        st.write(
            f"📝 **Words:** "
            f"{total_words:,}"
        )

        st.write(
            f"📑 **Paragraphs:** "
            f"{total_paragraphs}"
        )

        st.write(
            f"🔤 **Sentences:** "
            f"{total_sentences}"
        )

        st.write(
            f"🌐 **Detected Language:** "
            f"{st.session_state.detected_language}"
        )


# ============================================================
# CLEAR ALL
# ============================================================
# IMPORTANT:
# Clear All is BELOW the main content
# and BEFORE the footer.
# It is NOT inside the sidebar.
# ============================================================

st.divider()

clear_col1, clear_col2, clear_col3 = st.columns(
    [1, 2, 1]
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

st.divider()

st.markdown(
    """
    <div class="footer-text">
        Every word you listen to can become
        knowledge you remember.
    </div>

    <div class="footer-brand">
        🎙️ Document Voice Studio
    </div>
    """,
    unsafe_allow_html=True
)
