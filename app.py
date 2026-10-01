# ============================================================
# 🎙️ DOCUMENT VOICE STUDIO
# PDF → TEXT → PAGE → PARAGRAPH → SENTENCE → VOICE
# ============================================================

# Install:
#
# pip install streamlit pypdf gTTS langdetect
#
# Run:
#
# streamlit run app.py


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
from langdetect import detect

import re
import os
import hashlib


# ============================================================
# PAGE CONFIGURATION
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

    /* ======================================================
       GENERAL
    ====================================================== */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    .sidebar-brand {
        font-size: 24px;
        font-weight: 750;
        margin-bottom: 2px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    .sidebar-motivation {
        padding: 16px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        font-size: 13px;
        line-height: 1.6;
    }


    /* ======================================================
       HEADER
    ====================================================== */

    .project-title {
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -1.2px;
        margin-bottom: 3px;
    }

    .project-subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 28px;
    }


    /* ======================================================
       UPLOAD CARD
    ====================================================== */

    .upload-card {
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-bottom: 25px;
    }


    /* ======================================================
       SECTION TITLES
    ====================================================== */

    .section-heading {
        font-size: 22px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ======================================================
       DOCUMENT CARD
    ====================================================== */

    .document-card {
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .document-name {
        font-size: 17px;
        font-weight: 650;
    }

    .document-info {
        color: #6b7280;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ======================================================
       STATISTICS
    ====================================================== */

    .stat-card {
        padding: 20px;
        border-radius: 17px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        min-height: 105px;
    }

    .stat-label {
        color: #6b7280;
        font-size: 13px;
    }

    .stat-number {
        font-size: 28px;
        font-weight: 750;
        margin-top: 6px;
    }


    /* ======================================================
       CONTENT CARD
    ====================================================== */

    .content-card {
        padding: 20px;
        border-radius: 17px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-bottom: 15px;
    }


    /* ======================================================
       FOOTER
    ====================================================== */

    .footer-line {
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        color: #6b7280;
        font-size: 14px;
    }

    .footer-brand {
        font-weight: 650;
        margin-top: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {

    "pages": [],

    "current_page": 0,

    "file_name": "",

    "file_id": None,

    "page_audio": None,

    "paragraph_audio": {},

    "sentence_audio": {},

    "detected_language": "en"
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CLEAR ALL
# ============================================================

def clear_all():

    st.session_state.pages = []

    st.session_state.current_page = 0

    st.session_state.file_name = ""

    st.session_state.file_id = None

    st.session_state.page_audio = None

    st.session_state.paragraph_audio = {}

    st.session_state.sentence_audio = {}

    st.session_state.detected_language = "en"

    # Remove uploaded file widget state
    if "document_uploader" in st.session_state:

        del st.session_state["document_uploader"]


# ============================================================
# EXTRACT PDF
# ============================================================

def extract_pdf(uploaded_file):

    pages = []

    reader = PdfReader(uploaded_file)

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(
                text.strip()
            )

        else:

            pages.append("")


    return pages


# ============================================================
# GET PARAGRAPHS
# ============================================================

def get_paragraphs(text):

    # First try normal paragraph separation
    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    paragraphs = [

        p.strip()

        for p in paragraphs

        if p.strip()

    ]

    # If PDF extraction produced no paragraph breaks,
    # treat the whole page as one paragraph.
    if not paragraphs and text.strip():

        paragraphs = [
            text.strip()
        ]

    return paragraphs


# ============================================================
# GET SENTENCES
# ============================================================

def get_sentences(text):

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

        detected = detect(
            text[:3000]
        )

        return detected

    except:

        return "en"


# ============================================================
# LANGUAGE MAPPING FOR gTTS
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


        tts.save(
            filename
        )


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


    st.markdown(
        "### 💡 Motivation"
    )


    st.markdown(
        """
        <div class="sidebar-motivation">

        <b>
        "Read less. Listen more.
        Learn better."
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    st.caption(
        "Document Voice Studio"
    )

    st.caption(
        "PDF → Text → Voice"
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
# PDF UPLOAD
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        """
        <div class="section-heading">
            📄 Upload Your Document
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="upload-card">

        <b>Upload a PDF document</b>

        <br><br>

        Drag and drop your PDF here,
        or choose a file from your computer.

        </div>
        """,
        unsafe_allow_html=True
    )


uploaded_file = st.file_uploader(

    "Browse files",

    type=["pdf"],

    key="document_uploader",

    label_visibility="visible"

)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    current_file_id = (

        uploaded_file.name,

        uploaded_file.size

    )


    if (
        st.session_state.file_id
        != current_file_id
    ):

        with st.spinner(
            "Reading your document..."
        ):

            try:

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


                # Detect language from document
                full_text_sample = " ".join(
                    pages
                )[:3000]


                st.session_state.detected_language = (
                    detect_language(
                        full_text_sample
                    )
                )


            except Exception as e:

                st.error(
                    f"Could not read PDF: {e}"
                )


# ============================================================
# IF NO DOCUMENT
# ============================================================

if not st.session_state.pages:

    if navigation == "🏠 Dashboard":

        st.info(
            "📄 Upload a PDF above to start "
            "using Document Voice Studio."
        )


        st.markdown(
            """
            <div class="content-card">

            <h3>How it works</h3>

            <p>
            <b>1.</b> Upload your PDF
            </p>

            <p>
            <b>2.</b> Read the document page by page
            </p>

            <p>
            <b>3.</b> Explore paragraphs and sentences
            </p>

            <p>
            <b>4.</b> Convert content into voice
            </p>

            <p>
            <b>5.</b> Download the generated audio
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.info(
            "📄 Please upload a PDF from the "
            "Dashboard first."
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="footer-line">

        "Give your words a voice."

        <div class="footer-brand">
            🎙️ Document Voice Studio
        </div>

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

current_text = pages[
    current_page
]


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


# ============================================================
# DOCUMENT CARD
# ============================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        "### YOUR DOCUMENT"
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
            {character_count:,} Characters
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # STATISTICS
    # ========================================================

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
            {character_count:,}
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
            {word_count:,}
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
            {paragraph_count}
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
            {sentence_count}
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
        "### 📖 Page Navigation"
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

            value=current_page + 1

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
# DOCUMENT PAGE
# ============================================================

if navigation == "📄 Document":

    st.markdown(
        f"## 📄 Page {current_page + 1}"
    )


    st.caption(
        f"Document: {st.session_state.file_name}"
    )


    st.text_area(

        "Page Content",

        value=current_text,

        height=450

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
            paragraph_count
        )


    with c4:

        st.metric(
            "Sentences",
            sentence_count
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
        "## 🎙️ Voice Studio"
    )


    st.caption(
        "Convert pages, paragraphs and sentences "
        "into downloadable audio."
    )


    # ========================================================
    # LANGUAGE
    # ========================================================

    detected_language = (
        st.session_state.detected_language
    )


    st.info(
        f"🌐 Detected document language: "
        f"**{detected_language}**"
    )


    # ========================================================
    # PAGE VOICE
    # ========================================================

    st.markdown(
        f"### 📖 Page {current_page + 1} Voice"
    )


    if st.button(
        "🎙️ Generate Page Voice",
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
        ) as file:

            st.download_button(

                "⬇️ Download Page Voice",

                data=file,

                file_name=os.path.basename(
                    st.session_state.page_audio
                ),

                mime="audio/mpeg",

                use_container_width=True,

                key="download_page_audio"

            )


    # ========================================================
    # PARAGRAPH VOICE
    # ========================================================

    st.divider()


    st.markdown(
        "### 📝 Paragraph Voice"
    )


    if not paragraphs:

        st.warning(
            "No paragraphs found."
        )


    for i, paragraph in enumerate(
        paragraphs
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"**Paragraph {i + 1}**"
            )


            st.write(
                paragraph
            )


            st.caption(
                f"{len(paragraph):,} characters "
                f"• "
                f"{len(paragraph.split()):,} words"
            )


            paragraph_key = (
                f"{current_page}_{i}"
            )


            if st.button(

                f"🎙️ Generate Paragraph {i + 1} Voice",

                key=f"paragraph_button_{current_page}_{i}",

                use_container_width=True

            ):

                filename = (

                    f"page_"
                    f"{current_page + 1}_"
                    f"paragraph_"
                    f"{i + 1}.mp3"

                )


                with st.spinner(
                    "Creating paragraph voice..."
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
                        f"Paragraph {i + 1} voice ready."
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

                        key=(
                            f"download_paragraph_"
                            f"{current_page}_"
                            f"{i}"
                        ),

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

        with st.container(
            border=True
        ):

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

                filename = (

                    f"page_"
                    f"{current_page + 1}_"
                    f"sentence_"
                    f"{i + 1}.mp3"

                )


                with st.spinner(
                    "Creating sentence voice..."
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
                        f"Sentence {i + 1} voice ready."
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

                        key=(
                            f"download_sentence_"
                            f"{current_page}_"
                            f"{i}"
                        ),

                        use_container_width=True

                    )


# ============================================================
# ANALYTICS
# ============================================================

elif navigation == "📊 Analytics":

    st.markdown(
        "## 📊 Document Analytics"
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
        get_paragraphs(
            full_text
        )
    )


    total_sentences = len(
        get_sentences(
            full_text
        )
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


    st.write(
        f"**File:** {st.session_state.file_name}"
    )


    st.write(
        f"**Total Pages:** {total_pages}"
    )


    st.write(
        f"**Total Characters:** "
        f"{total_characters:,}"
    )


    st.write(
        f"**Total Words:** "
        f"{total_words:,}"
    )


    st.write(
        f"**Total Paragraphs:** "
        f"{total_paragraphs}"
    )


    st.write(
        f"**Total Sentences:** "
        f"{total_sentences}"
    )


    st.write(
        f"**Detected Language:** "
        f"{st.session_state.detected_language}"
    )


# ============================================================
# CLEAR ALL
# ============================================================
# IMPORTANT:
# This button is BEFORE the footer and NOT in sidebar.

st.divider()


clear_col1, clear_col2, clear_col3 = st.columns(
    [2, 2, 2]
)


with clear_col2:

    if st.button(

        "🧹 Clear All",

        use_container_width=True,

        type="secondary"

    ):

        clear_all()

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-line">

        "Give your words a voice."

        <div class="footer-brand">
            🎙️ Document Voice Studio
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
