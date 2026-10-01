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

    /* ================================
       GLOBAL
       ================================ */

    .stApp {
        background-color: #0b0f14;
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

    p, label {
        color: #d1d5db !important;
    }

    hr {
        border-color: #293442 !important;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background-color: #11151c !important;
        border-right: 1px solid #29313d;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        color: #8995a5;
        font-size: 13px;
        margin-bottom: 20px;
    }

    .sidebar-heading {
        color: #8995a5;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.2px;
        margin-top: 8px;
        margin-bottom: 10px;
    }


    /* ================================
       MOTIVATION
       ================================ */

    .motivation-box {
        background: #171d26;
        border: 1px solid #303a48;
        border-radius: 14px;
        padding: 15px;
        margin-top: 8px;
    }

    .motivation-main {
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
        line-height: 1.5;
    }

    .motivation-small {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 6px;
        line-height: 1.5;
    }


    /* ================================
       MAIN HEADER
       ================================ */

    .main-title {
        font-size: 40px;
        font-weight: 850;
        color: #ffffff;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #8f9baa;
        margin-bottom: 28px;
    }


    /* ================================
       SECTION HEADER
       ================================ */

    .section-label {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 14px;
    }


    /* ================================
       UPLOADER
       ================================ */

    [data-testid="stFileUploader"] {
        background-color: #151a22 !important;
        border: 1px solid #303a48 !important;
        border-radius: 18px !important;
        padding: 10px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #151a22 !important;
        border: 1px dashed #526071 !important;
        border-radius: 14px !important;
        min-height: 180px !important;
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
        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
    }


    /* ================================
       BUTTONS
       ================================ */

    .stButton > button {
        background-color: #171d26 !important;
        color: #f8fafc !important;
        border: 1px solid #344050 !important;
        border-radius: 10px !important;
        min-height: 42px !important;
        font-weight: 650 !important;
    }

    .stButton > button:hover {
        background-color: #202a37 !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
    }

    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }


    /* ================================
       METRICS
       ================================ */

    [data-testid="stMetric"] {
        background-color: #151a22;
        border: 1px solid #293442;
        border-radius: 15px;
        padding: 17px;
    }

    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }


    /* ================================
       TEXT AREA
       ================================ */

    textarea {
        background-color: #151a22 !important;
        color: #ffffff !important;
        border: 1px solid #344050 !important;
        border-radius: 12px !important;
    }


    /* ================================
       NUMBER INPUT
       ================================ */

    div[data-testid="stNumberInput"] input {
        background-color: #151a22 !important;
        color: #ffffff !important;
        border: 1px solid #344050 !important;
    }


    /* ================================
       EXPANDERS
       ================================ */

    [data-testid="stExpander"] {
        background-color: #151a22 !important;
        border: 1px solid #293442 !important;
        border-radius: 12px !important;
    }


    /* ================================
       INFO / SUCCESS / WARNING
       ================================ */

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }


    /* ================================
       FOOTER
       ================================ */

    .footer-quote {
        text-align: center;
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 600;
        margin-top: 10px;
    }

    .footer-brand {
        text-align: center;
        color: #ffffff;
        font-weight: 750;
        font-size: 14px;
        margin-top: 8px;
    }

    .footer-small {
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        margin-top: 5px;
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

        if isinstance(value, dict):
            st.session_state[key] = {}

        elif isinstance(value, list):
            st.session_state[key] = []

        else:
            st.session_state[key] = value


# ============================================================
# LANGUAGE DETECTION WITHOUT LANGDETECT
# ============================================================

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "te": "Telugu",
    "ta": "Tamil",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "ne": "Nepali",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese",
    "th": "Thai",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "id": "Indonesian"
}


# ============================================================
# UNICODE LANGUAGE DETECTION
# ============================================================

def detect_language(text):

    if not text or not text.strip():
        return "en"

    sample = text[:10000]

    # Kannada
    if re.search(r"[\u0C80-\u0CFF]", sample):
        return "kn"

    # Telugu
    if re.search(r"[\u0C00-\u0C7F]", sample):
        return "te"

    # Tamil
    if re.search(r"[\u0B80-\u0BFF]", sample):
        return "ta"

    # Malayalam
    if re.search(r"[\u0D00-\u0D7F]", sample):
        return "ml"

    # Hindi / Devanagari
    if re.search(r"[\u0900-\u097F]", sample):
        return "hi"

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

    # Thai
    if re.search(r"[\u0E00-\u0E7F]", sample):
        return "th"

    # Japanese
    if re.search(r"[\u3040-\u30FF]", sample):
        return "ja"

    # Korean
    if re.search(r"[\uAC00-\uD7AF]", sample):
        return "ko"

    # Chinese
    if re.search(r"[\u4E00-\u9FFF]", sample):
        return "zh-CN"

    # Russian / Cyrillic
    if re.search(r"[\u0400-\u04FF]", sample):
        return "ru"

    # Default
    return "en"


# ============================================================
# GTTS LANGUAGE MAP
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
    "ar": "ar",
    "ru": "ru",
    "ja": "ja",
    "ko": "ko",
    "zh-CN": "zh-CN",
    "th": "th",
    "de": "de",
    "fr": "fr",
    "es": "es",
    "it": "it",
    "pt": "pt",
    "tr": "tr",
    "vi": "vi",
    "id": "id"
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

        st.session_state.document_uploader = None


# ============================================================
# EXTRACT PDF
# ============================================================

def extract_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    extracted_pages = []

    for page in reader.pages:

        try:

            text = page.extract_text()

            if text:

                extracted_pages.append(
                    text.strip()
                )

            else:

                extracted_pages.append("")

        except Exception:

            extracted_pages.append("")

    return extracted_pages


# ============================================================
# PARAGRAPHS
# ============================================================

def get_paragraphs(text):

    if not text or not text.strip():
        return []

    blocks = re.split(
        r"\n\s*\n",
        text
    )

    result = []

    for block in blocks:

        clean = re.sub(
            r"\s+",
            " ",
            block
        ).strip()

        if clean:

            result.append(clean)

    # If PDF extraction doesn't contain blank lines
    if not result:

        clean = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if clean:
            result = [clean]

    return result


# ============================================================
# SENTENCES
# ============================================================

def get_sentences(text):

    if not text or not text.strip():
        return []

    cleaned = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    sentences = re.split(
        r"(?<=[.!?।！？])\s+",
        cleaned
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# ============================================================
# CREATE AUDIO
# ============================================================

def create_audio(text, filename, language):

    if not text or not text.strip():

        return None

    try:

        lang = LANGUAGE_MAP.get(
            language,
            "en"
        )

        tts = gTTS(
            text=text,
            lang=lang,
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
# DOCUMENT ID
# ============================================================

def make_file_id(uploaded_file):

    file_bytes = uploaded_file.getvalue()

    file_hash = hashlib.md5(
        file_bytes
    ).hexdigest()

    return (
        uploaded_file.name,
        uploaded_file.size,
        file_hash
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>🎙️ Document Voice</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sidebar-subtitle'>Document-Audio Studio</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "<div class='sidebar-heading'>NAVIGATION</div>",
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

    st.markdown(
        "<div class='sidebar-heading'>💡 DAILY THOUGHT</div>",
        unsafe_allow_html=True
    )

    # IMPORTANT:
    # This uses normal Streamlit text.
    # No raw HTML div is used here.

    with st.container(border=True):

        st.markdown(
            "**Every word you listen to can become knowledge you remember.**"
        )

        st.caption(
            "Listen • Learn • Remember • Grow"
        )

    st.divider()

    st.caption("🎙️ Document Voice Studio")
    st.caption("PDF → Text → Voice")


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    "# 🎙️ Document Voice Studio"
)

st.markdown(
    "### Transform your documents into voice"
)

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        "## 📄 Upload Your Document"
    )

    st.caption(
        "Upload a PDF and explore it page by page, paragraph by paragraph, and sentence by sentence."
    )

    uploaded_file = st.file_uploader(
        "Drag and drop your PDF here",
        type=["pdf"],
        key="document_uploader"
    )

    # --------------------------------------------------------
    # PROCESS PDF
    # --------------------------------------------------------

    if uploaded_file is not None:

        new_file_id = make_file_id(
            uploaded_file
        )

        if (
            st.session_state.file_id
            != new_file_id
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
    # CURRENT DOCUMENT
    # --------------------------------------------------------

    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        full_text = "\n".join(pages)

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

        st.markdown(
            "## 📘 Current Document"
        )

        st.info(
            f"📄 Currently viewing page "
            f"{st.session_state.current_page + 1} "
            f"of {total_pages}"
        )

        # ----------------------------------------------------
        # DOCUMENT ANALYTICS
        # ----------------------------------------------------

        st.markdown(
            "### 📊 Document Analytics"
        )

        a1, a2, a3 = st.columns(3)

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


        a4, a5 = st.columns(2)

        with a4:

            st.metric(
                "📑 Paragraphs",
                len(all_paragraphs)
            )

        with a5:

            st.metric(
                "🔤 Sentences",
                len(all_sentences)
            )


        # ----------------------------------------------------
        # DOCUMENT INFORMATION
        # ----------------------------------------------------

        st.markdown(
            "### 📋 Document Information"
        )

        info1, info2 = st.columns(2)

        with info1:

            st.write(
                f"**📄 File Name:** {st.session_state.file_name}"
            )

            st.write(
                f"**📑 Total Pages:** {total_pages}"
            )

            st.write(
                f"**🔤 Characters:** {total_characters:,}"
            )

        with info2:

            st.write(
                f"**📝 Words:** {total_words:,}"
            )

            st.write(
                f"**📑 Paragraphs:** {len(all_paragraphs)}"
            )

            st.write(
                f"**🔤 Sentences:** {len(all_sentences)}"
            )


        # ----------------------------------------------------
        # PAGE NAVIGATION
        # ----------------------------------------------------

        st.markdown(
            "### 📖 Page Navigation"
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

        current_text = pages[current_page]

        current_paragraphs = get_paragraphs(
            current_text
        )

        current_sentences = get_sentences(
            current_text
        )

        st.markdown(
            f"### 📄 Page {current_page + 1}"
        )

        st.text_area(
            "Page Content",
            value=current_text,
            height=300,
            disabled=True,
            key="dashboard_page_content"
        )


        # ----------------------------------------------------
        # PAGE STATISTICS
        # ----------------------------------------------------

        st.markdown(
            "### 📊 Page Statistics"
        )

        p1, p2, p3, p4 = st.columns(4)

        with p1:

            st.metric(
                "🔤 Characters",
                f"{len(current_text):,}"
            )

        with p2:

            st.metric(
                "📝 Words",
                f"{len(current_text.split()):,}"
            )

        with p3:

            st.metric(
                "📑 Paragraphs",
                len(current_paragraphs)
            )

        with p4:

            st.metric(
                "🔤 Sentences",
                len(current_sentences)
            )


        # ----------------------------------------------------
        # PAGE VOICE
        # ----------------------------------------------------

        st.markdown(
            "### 🎙️ Page Voice"
        )

        detected = st.session_state.detected_language

        st.caption(
            f"Detected document language: "
            f"**{LANGUAGE_NAMES.get(detected, detected)}**"
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
                    detected
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
            "### 📝 Paragraphs"
        )

        if current_paragraphs:

            for i, paragraph in enumerate(
                current_paragraphs
            ):

                with st.expander(
                    f"📑 Paragraph {i + 1}",
                    expanded=False
                ):

                    st.write(
                        paragraph
                    )

                    paragraph_key = (
                        f"{current_page}_{i}"
                    )

                    if st.button(
                        f"🎙️ Generate Paragraph {i + 1} Voice",
                        key=f"dash_para_{current_page}_{i}",
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
                                key=f"dash_para_download_{current_page}_{i}"
                            )

        else:

            st.warning(
                "No paragraphs were found on this page."
            )


        # ----------------------------------------------------
        # SENTENCES
        # ----------------------------------------------------

        st.markdown(
            "### 🔤 Sentences"
        )

        if current_sentences:

            for i, sentence in enumerate(
                current_sentences
            ):

                with st.expander(
                    f"🔤 Sentence {i + 1}",
                    expanded=False
                ):

                    st.write(
                        sentence
                    )

                    sentence_key = (
                        f"{current_page}_{i}"
                    )

                    if st.button(
                        f"🎙️ Generate Sentence {i + 1} Voice",
                        key=f"dash_sentence_{current_page}_{i}",
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
                                key=f"dash_sentence_download_{current_page}_{i}"
                            )

        else:

            st.warning(
                "No sentences were found on this page."
            )


        # ----------------------------------------------------
        # DASHBOARD HOW IT WORKS
        # ----------------------------------------------------

        st.markdown(
            "### 💡 How It Works"
        )

        with st.expander(
            "📘 Learn how to use Document Voice Studio",
            expanded=False
        ):

            st.write(
                "**01 — Upload your PDF**"
            )

            st.write(
                "Upload any text-based PDF using the upload area above."
            )

            st.write(
                "**02 — View your document**"
            )

            st.write(
                "The application extracts the PDF text and displays the document page by page."
            )

            st.write(
                "**03 — Check document analytics**"
            )

            st.write(
                "View total pages, characters, words, paragraphs, and sentences."
            )

            st.write(
                "**04 — Navigate pages**"
            )

            st.write(
                "Use Previous, Next, or the page number to move through the document."
            )

            st.write(
                "**05 — Generate page voice**"
            )

            st.write(
                "Convert the complete current page into speech."
            )

            st.write(
                "**06 — Generate paragraph voice**"
            )

            st.write(
                "Open a paragraph and generate a separate voice file."
            )

            st.write(
                "**07 — Generate sentence voice**"
            )

            st.write(
                "Generate voice for individual sentences."
            )

            st.write(
                "**08 — Download audio**"
            )

            st.write(
                "Use the download buttons to save generated MP3 files."
            )


    else:

        st.info(
            "📄 Upload a PDF above to start using Document Voice Studio."
        )

        st.markdown(
            "### 💡 How It Works"
        )

        with st.expander(
            "📘 Getting started",
            expanded=True
        ):

            st.write(
                "**01 — Upload your PDF document**"
            )

            st.write(
                "**02 — View your document page by page**"
            )

            st.write(
                "**03 — Read individual paragraphs**"
            )

            st.write(
                "**04 — Convert pages, paragraphs and sentences into voice**"
            )

            st.write(
                "**05 — Play and download your generated audio**"
            )


# ============================================================
# DOCUMENT PAGE
# ============================================================

elif navigation == "📄 Document":

    st.markdown(
        "## 📄 Document"
    )

    st.caption(
        "Read and explore your uploaded document page by page."
    )

    st.markdown(
        "### 💡 How to Use Document"
    )

    with st.expander(
        "📘 Document instructions",
        expanded=True
    ):

        st.write(
            "**01 — Go to Dashboard and upload a PDF.**"
        )

        st.write(
            "**02 — Return to Document to read the extracted text.**"
        )

        st.write(
            "**03 — Use Page Navigation to move between pages.**"
        )

        st.write(
            "**04 — Check page statistics for characters, words, paragraphs and sentences.**"
        )

        st.write(
            "**05 — Expand paragraphs and sentences to read individual sections.**"
        )

    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        current_page = (
            st.session_state.current_page
        )

        current_text = pages[current_page]

        paragraphs = get_paragraphs(
            current_text
        )

        sentences = get_sentences(
            current_text
        )

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

        st.markdown(
            "### 📊 Page Statistics"
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

        st.markdown(
            "### 📖 Page Navigation"
        )

        c1, c2, c3 = st.columns(
            [1, 2, 1]
        )

        with c1:

            if st.button(
                "← Previous",
                use_container_width=True,
                disabled=current_page == 0,
                key="document_previous"
            ):

                st.session_state.current_page -= 1

                st.rerun()

        with c2:

            selected_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=current_page + 1,
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

        with c3:

            if st.button(
                "Next →",
                use_container_width=True,
                disabled=current_page == total_pages - 1,
                key="document_next"
            ):

                st.session_state.current_page += 1

                st.rerun()

    else:

        st.info(
            "📄 No document loaded. Go to Dashboard and upload a PDF first."
        )


# ============================================================
# VOICE STUDIO
# ============================================================

elif navigation == "🎙️ Voice Studio":

    st.markdown(
        "## 🎙️ Voice Studio"
    )

    st.caption(
        "Turn pages, paragraphs and sentences into downloadable speech."
    )

    st.markdown(
        "### 💡 How to Use Voice Studio"
    )

    with st.expander(
        "📘 Voice Studio instructions",
        expanded=True
    ):

        st.write(
            "**01 — Upload your PDF from Dashboard.**"
        )

        st.write(
            "**02 — Select the page you want to listen to.**"
        )

        st.write(
            "**03 — Generate Page Voice for the complete page.**"
        )

        st.write(
            "**04 — Generate Paragraph Voice for an individual paragraph.**"
        )

        st.write(
            "**05 — Generate Sentence Voice for an individual sentence.**"
        )

        st.write(
            "**06 — Play the generated audio directly in the application.**"
        )

        st.write(
            "**07 — Download the MP3 using the download button.**"
        )

    if st.session_state.pages:

        pages = st.session_state.pages

        total_pages = len(pages)

        current_page = (
            st.session_state.current_page
        )

        current_text = pages[current_page]

        paragraphs = get_paragraphs(
            current_text
        )

        sentences = get_sentences(
            current_text
        )

        language = (
            st.session_state.detected_language
        )

        st.info(
            f"🌐 Detected language: "
            f"**{LANGUAGE_NAMES.get(language, language)}**"
        )

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        st.markdown(
            "### 📖 Page Navigation"
        )

        c1, c2, c3 = st.columns(
            [1, 2, 1]
        )

        with c1:

            if st.button(
                "← Previous",
                use_container_width=True,
                disabled=current_page == 0,
                key="voice_previous"
            ):

                st.session_state.current_page -= 1

                st.session_state.page_audio = None

                st.rerun()

        with c2:

            selected_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=current_page + 1,
                key="voice_page_number"
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

        with c3:

            if st.button(
                "Next →",
                use_container_width=True,
                disabled=current_page == total_pages - 1,
                key="voice_next"
            ):

                st.session_state.current_page += 1

                st.session_state.page_audio = None

                st.rerun()


        # ----------------------------------------------------
        # PAGE VOICE
        # ----------------------------------------------------

        st.markdown(
            f"### 📖 Page {current_page + 1} Voice"
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
                    language
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
            ) as file:

                st.download_button(
                    "⬇️ Download Page Voice",
                    data=file,
                    file_name=os.path.basename(
                        st.session_state.page_audio
                    ),
                    mime="audio/mpeg",
                    use_container_width=True,
                    key="voice_download_page"
                )


        # ----------------------------------------------------
        # PARAGRAPH VOICE
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            "### 📝 Paragraph Voice"
        )

        for i, paragraph in enumerate(
            paragraphs
        ):

            with st.expander(
                f"📑 Paragraph {i + 1}"
            ):

                st.write(
                    paragraph
                )

                paragraph_key = (
                    f"{current_page}_{i}"
                )

                if st.button(
                    f"🎙️ Generate Paragraph {i + 1} Voice",
                    use_container_width=True,
                    key=f"voice_paragraph_{current_page}_{i}"
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
                            language
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
                            key=f"voice_download_paragraph_{current_page}_{i}"
                        )


        # ----------------------------------------------------
        # SENTENCE VOICE
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            "### 🔤 Sentence Voice"
        )

        for i, sentence in enumerate(
            sentences
        ):

            with st.expander(
                f"🔤 Sentence {i + 1}"
            ):

                st.write(
                    sentence
                )

                sentence_key = (
                    f"{current_page}_{i}"
                )

                if st.button(
                    f"🎙️ Generate Sentence {i + 1} Voice",
                    use_container_width=True,
                    key=f"voice_sentence_{current_page}_{i}"
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
                            language
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
                            key=f"voice_download_sentence_{current_page}_{i}"
                        )

    else:

        st.info(
            "📄 Upload a PDF from Dashboard before using Voice Studio."
        )


# ============================================================
# ANALYTICS
# ============================================================

elif navigation == "📊 Analytics":

    st.markdown(
        "## 📊 Document Analytics"
    )

    st.caption(
        "Understand the size and structure of your document."
    )

    st.markdown(
        "### 💡 How to Use Analytics"
    )

    with st.expander(
        "📘 Analytics instructions",
        expanded=True
    ):

        st.write(
            "**01 — Upload a PDF from Dashboard.**"
        )

        st.write(
            "**02 — Analytics automatically calculates document statistics.**"
        )

        st.write(
            "**03 — Review pages, characters, words, paragraphs and sentences.**"
        )

        st.write(
            "**04 — Use Document Information to understand the complete file.**"
        )

    if st.session_state.pages:

        pages = st.session_state.pages

        full_text = "\n".join(
            pages
        )

        total_pages = len(pages)

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

        # ----------------------------------------------------
        # TOP METRICS
        # ----------------------------------------------------

        st.markdown(
            "### 📈 Document Analytics"
        )

        c1, c2, c3 = st.columns(3)

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


        c4, c5 = st.columns(2)

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


        # ----------------------------------------------------
        # DOCUMENT INFORMATION
        # ----------------------------------------------------

        st.markdown(
            "### 📋 Document Information"
        )

        st.write(
            f"**📄 File Name:** {st.session_state.file_name}"
        )

        st.write(
            f"**📄 Total Pages:** {total_pages}"
        )

        st.write(
            f"**🔤 Total Characters:** {total_characters:,}"
        )

        st.write(
            f"**📝 Total Words:** {total_words:,}"
        )

        st.write(
            f"**📑 Total Paragraphs:** {total_paragraphs}"
        )

        st.write(
            f"**🔤 Total Sentences:** {total_sentences}"
        )

        detected = (
            st.session_state.detected_language
        )

        st.write(
            f"**🌐 Detected Language:** "
            f"{LANGUAGE_NAMES.get(detected, detected)}"
        )


        # ----------------------------------------------------
        # PAGE-BY-PAGE ANALYTICS
        # ----------------------------------------------------

        st.markdown(
            "### 📄 Page-by-Page Statistics"
        )

        for i, page in enumerate(pages):

            page_words = len(
                page.split()
            )

            page_paragraphs = len(
                get_paragraphs(page)
            )

            page_sentences = len(
                get_sentences(page)
            )

            with st.expander(
                f"📄 Page {i + 1}"
            ):

                x1, x2, x3, x4 = st.columns(4)

                with x1:

                    st.metric(
                        "Characters",
                        len(page)
                    )

                with x2:

                    st.metric(
                        "Words",
                        page_words
                    )

                with x3:

                    st.metric(
                        "Paragraphs",
                        page_paragraphs
                    )

                with x4:

                    st.metric(
                        "Sentences",
                        page_sentences
                    )

    else:

        st.info(
            "📄 Upload a PDF from Dashboard to view analytics."
        )


# ============================================================
# CLEAR ALL
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

        st.success(
            "✅ All document data and generated audio have been cleared."
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

# IMPORTANT:
# Footer is intentionally made with Streamlit components.
# No HTML div is used, so <div class="footer-quote">
# can NEVER appear as visible text.

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px 10px 5px 10px;
    ">
        <div style="
            color:#cbd5e1;
            font-size:15px;
            font-weight:600;
        ">
            Every word you listen to can become knowledge you remember.
        </div>

        <div style="
            color:#ffffff;
            font-size:14px;
            font-weight:750;
            margin-top:8px;
        ">
            🎙️ Document Voice Studio
        </div>

        <div style="
            color:#6b7280;
            font-size:12px;
            margin-top:5px;
        ">
            Listen • Learn • Remember • Grow
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
