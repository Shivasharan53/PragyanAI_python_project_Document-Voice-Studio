# ============================================================
# DOCUMENT VOICE STUDIO
# Modern PDF → Voice Application
#
# Features:
# PDF Upload
# Page-by-Page Reading
# Page Statistics
# Paragraph Detection
# Sentence Detection
# Paragraph Voice
# Sentence Voice
# Audio Playback
# Audio Download
# Clear All
# ============================================================


# ============================================================
# INSTALL
# ============================================================

# Run these once in terminal:
#
# pip install streamlit pypdf gTTS
#
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
from pypdf import PdfReader
from gtts import gTTS

import re
import os


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

    /* ================================
       GLOBAL
    ================================= */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ================================
       MAIN TITLE
    ================================= */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
    }


    /* ================================
       DASHBOARD CARDS
    ================================= */

    .dashboard-card {

        padding: 20px;

        border-radius: 18px;

        background: #ffffff;

        border: 1px solid #e5e7eb;

        min-height: 120px;

        box-shadow:
            0 4px 15px rgba(
                0,
                0,
                0,
                0.04
            );
    }


    .card-title {

        font-size: 14px;

        color: #6b7280;

        margin-bottom: 8px;
    }


    .card-value {

        font-size: 30px;

        font-weight: 700;

        color: #111827;
    }


    /* ================================
       SECTION
    ================================= */

    .section-title {

        font-size: 24px;

        font-weight: 650;

        margin-top: 25px;

        margin-bottom: 15px;
    }


    /* ================================
       SIDEBAR
    ================================= */

    section[data-testid="stSidebar"] {

        border-right:
            1px solid #e5e7eb;
    }


    /* ================================
       AUDIO CARD
    ================================= */

    .audio-card {

        padding: 18px;

        border-radius: 16px;

        background: #f8fafc;

        border: 1px solid #e5e7eb;

        margin-bottom: 15px;
    }


    /* ================================
       INFO BOX
    ================================= */

    .project-box {

        padding: 20px;

        border-radius: 18px;

        background: #f8fafc;

        border: 1px solid #e5e7eb;

        margin-top: 20px;
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

    st.session_state.page_audio = None

    st.session_state.paragraph_audio = {}

    st.session_state.sentence_audio = {}

    if "document_uploader" in st.session_state:

        del st.session_state[
            "document_uploader"
        ]


# ============================================================
# EXTRACT PDF
# ============================================================

def extract_pdf(uploaded_file):

    pages = []

    reader = PdfReader(
        uploaded_file
    )

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(
                text.strip()
            )

        else:

            pages.append(
                ""
            )

    return pages


# ============================================================
# PARAGRAPH DETECTION
# ============================================================

def get_paragraphs(text):

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    paragraphs = [

        paragraph.strip()

        for paragraph in paragraphs

        if paragraph.strip()

    ]

    return paragraphs


# ============================================================
# SENTENCE DETECTION
# ============================================================

def get_sentences(text):

    sentences = re.split(
        r"(?<=[.!?।])\s+",
        text
    )

    sentences = [

        sentence.strip()

        for sentence in sentences

        if sentence.strip()

    ]

    return sentences


# ============================================================
# CREATE VOICE
# ============================================================

def create_voice(
    text,
    filename
):

    if not text.strip():

        return None

    try:

        # Detect language automatically

        audio = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        audio.save(
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
        "## 🎙️ Document Voice"
    )

    st.caption(
        "Modern Document Audio Studio"
    )

    st.divider()


    # ========================================================
    # NAVIGATION
    # ========================================================

    st.markdown(
        "### Navigation"
    )


    page_selection = st.radio(

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


    # ========================================================
    # DOCUMENT UPLOAD
    # ========================================================

    st.markdown(
        "### Document"
    )


    uploaded_file = st.file_uploader(

        "Upload your document",

        type=["pdf"],

        key="document_uploader",

        label_visibility="collapsed"

    )


    if uploaded_file:

        st.success(
            "✓ Document ready"
        )


    st.divider()


    # ========================================================
    # CLEAR ALL
    # ========================================================

    if st.button(

        "🧹 Clear All",

        use_container_width=True

    ):

        clear_all()

        st.rerun()


    st.divider()


    st.caption(
        "Document Voice Studio"
    )

    st.caption(
        "PDF → Text → Voice"
    )


# ============================================================
# PROCESS UPLOADED FILE
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

        try:

            st.session_state.pages = (

                extract_pdf(
                    uploaded_file
                )

            )

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


        except Exception as e:

            st.error(
                f"PDF error: {e}"
            )


# ============================================================
# EMPTY DASHBOARD
# ============================================================

if not st.session_state.pages:

    st.markdown(
        '<div class="main-title">'
        '🎙️ Document Voice Studio'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="main-subtitle">'
        'Transform your documents into readable '
        'and listenable content.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # WELCOME
    # ========================================================

    st.info(
        "📄 Upload a PDF from the sidebar "
        "to start your document."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            ### 📖 Read

            Read your document page by page.
            """
        )


    with col2:

        st.markdown(
            """
            ### 📝 Analyse

            Explore paragraphs and sentences.
            """
        )


    with col3:

        st.markdown(
            """
            ### 🎙️ Listen

            Convert content into voice.
            """
        )


    st.stop()


# ============================================================
# DOCUMENT DATA
# ============================================================

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
# DASHBOARD
# ============================================================

if page_selection == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '🏠 Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="main-subtitle">'
        f'{st.session_state.file_name}'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "📄 Pages",
            total_pages
        )


    with col2:

        st.metric(
            "🔤 Characters",
            character_count
        )


    with col3:

        st.metric(
            "📝 Words",
            word_count
        )


    with col4:

        st.metric(
            "📑 Paragraphs",
            paragraph_count
        )


    with col5:

        st.metric(
            "🔤 Sentences",
            sentence_count
        )


    st.markdown(
        '<div class="section-title">'
        '📖 Current Document'
        '</div>',
        unsafe_allow_html=True
    )


    st.info(
        f"Currently viewing "
        f"page {current_page + 1} "
        f"of {total_pages}."
    )


    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    with col1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True,
            disabled=current_page == 0
        ):

            st.session_state.current_page -= 1

            st.rerun()


    with col2:

        selected_page = st.number_input(

            "Page",

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

            st.rerun()


    with col3:

        if st.button(
            "Next ➡️",
            use_container_width=True,
            disabled=current_page == total_pages - 1
        ):

            st.session_state.current_page += 1

            st.rerun()


    # ========================================================
    # PAGE TEXT
    # ========================================================

    st.markdown(
        f"### 📖 Page {current_page + 1}"
    )


    st.text_area(

        "Page Content",

        value=current_text,

        height=350

    )


# ============================================================
# DOCUMENT PAGE
# ============================================================

elif page_selection == "📄 Document":

    st.markdown(
        '<div class="main-title">'
        '📄 Document Reader'
        '</div>',
        unsafe_allow_html=True
    )


    st.caption(
        f"Page {current_page + 1} "
        f"of {total_pages}"
    )


    # ========================================================
    # NAVIGATION
    # ========================================================

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    with col1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True,
            disabled=current_page == 0
        ):

            st.session_state.current_page -= 1

            st.rerun()


    with col2:

        selected_page = st.number_input(

            "Go to page",

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

            st.rerun()


    with col3:

        if st.button(
            "Next ➡️",
            use_container_width=True,
            disabled=current_page == total_pages - 1
        ):

            st.session_state.current_page += 1

            st.rerun()


    # ========================================================
    # PAGE TEXT
    # ========================================================

    st.subheader(
        f"📖 Page {current_page + 1}"
    )


    st.text_area(

        "Document Content",

        value=current_text,

        height=500

    )


    # ========================================================
    # STATISTICS
    # ========================================================

    st.subheader(
        "📊 Page Statistics"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Characters",
            character_count
        )


    with c2:

        st.metric(
            "Words",
            word_count
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


# ============================================================
# VOICE STUDIO
# ============================================================

elif page_selection == "🎙️ Voice Studio":

    st.markdown(
        '<div class="main-title">'
        '🎙️ Voice Studio'
        '</div>',
        unsafe_allow_html=True
    )


    st.caption(
        "Convert paragraphs and sentences into voice."
    )


    # ========================================================
    # PAGE VOICE
    # ========================================================

    st.subheader(
        f"📖 Page {current_page + 1} Voice"
    )


    if st.button(
        "🎙️ Generate Page Voice",
        use_container_width=True
    ):

        filename = (
            f"page_{current_page + 1}.mp3"
        )


        with st.spinner(
            "Generating page voice..."
        ):

            audio = create_voice(
                current_text,
                filename
            )


        if audio:

            st.session_state.page_audio = (
                audio
            )

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

                file_name=(
                    f"page_{current_page + 1}.mp3"
                ),

                mime="audio/mpeg",

                use_container_width=True

            )


    # ========================================================
    # PARAGRAPH VOICE
    # ========================================================

    st.divider()

    st.subheader(
        "📝 Paragraph Voice"
    )


    for index, paragraph in enumerate(
        paragraphs
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"### Paragraph {index + 1}"
            )


            st.write(
                paragraph
            )


            st.caption(
                f"{len(paragraph)} characters • "
                f"{len(paragraph.split())} words"
            )


            if st.button(

                f"🎙️ Generate Voice "
                f"for Paragraph {index + 1}",

                key=f"paragraph_{current_page}_{index}",

                use_container_width=True

            ):

                filename = (

                    f"page_"
                    f"{current_page + 1}_"
                    f"paragraph_"
                    f"{index + 1}.mp3"

                )


                with st.spinner(
                    "Generating paragraph voice..."
                ):

                    audio = create_voice(

                        paragraph,

                        filename

                    )


                if audio:

                    st.session_state.paragraph_audio[
                        f"{current_page}_{index}"
                    ] = audio


                    st.success(
                        "✅ Paragraph voice ready."
                    )


            audio_key = (
                f"{current_page}_{index}"
            )


            if audio_key in (
                st.session_state.paragraph_audio
            ):

                audio_file = (
                    st.session_state.paragraph_audio[
                        audio_key
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
                            f"download_para_"
                            f"{current_page}_"
                            f"{index}"
                        ),

                        use_container_width=True

                    )


    # ========================================================
    # SENTENCE VOICE
    # ========================================================

    st.divider()

    st.subheader(
        "🔤 Sentence Voice"
    )


    for index, sentence in enumerate(
        sentences
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"### Sentence {index + 1}"
            )


            st.write(
                sentence
            )


            if st.button(

                f"🎙️ Generate Voice "
                f"for Sentence {index + 1}",

                key=f"sentence_{current_page}_{index}",

                use_container_width=True

            ):

                filename = (

                    f"page_"
                    f"{current_page + 1}_"
                    f"sentence_"
                    f"{index + 1}.mp3"

                )


                with st.spinner(
                    "Generating sentence voice..."
                ):

                    audio = create_voice(

                        sentence,

                        filename

                    )


                if audio:

                    st.session_state.sentence_audio[
                        f"{current_page}_{index}"
                    ] = audio


                    st.success(
                        "✅ Sentence voice ready."
                    )


            audio_key = (
                f"{current_page}_{index}"
            )


            if audio_key in (
                st.session_state.sentence_audio
            ):

                audio_file = (
                    st.session_state.sentence_audio[
                        audio_key
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
                            f"{index}"
                        ),

                        use_container_width=True

                    )


# ============================================================
# ANALYTICS
# ============================================================

elif page_selection == "📊 Analytics":

    st.markdown(
        '<div class="main-title">'
        '📊 Document Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    st.caption(
        "Overview of your current document."
    )


    # ========================================================
    # TOTAL DOCUMENT TEXT
    # ========================================================

    full_document = "\n".join(
        pages
    )


    total_characters = len(
        full_document
    )


    total_words = len(
        full_document.split()
    )


    total_paragraphs = len(
        get_paragraphs(
            full_document
        )
    )


    total_sentences = len(
        get_sentences(
            full_document
        )
    )


    # ========================================================
    # ANALYTICS CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "📄 Total Pages",
            total_pages
        )


    with c2:

        st.metric(
            "🔤 Characters",
            total_characters
        )


    with c3:

        st.metric(
            "📝 Words",
            total_words
        )


    with c4:

        st.metric(
            "📑 Paragraphs",
            total_paragraphs
        )


    st.divider()


    st.metric(
        "🔤 Total Sentences",
        total_sentences
    )


    # ========================================================
    # DOCUMENT SUMMARY
    # ========================================================

    st.subheader(
        "📋 Document Summary"
    )


    st.write(
        f"**Document:** "
        f"{st.session_state.file_name}"
    )


    st.write(
        f"**Pages:** {total_pages}"
    )


    st.write(
        f"**Characters:** "
        f"{total_characters}"
    )


    st.write(
        f"**Words:** "
        f"{total_words}"
    )


    st.write(
        f"**Paragraphs:** "
        f"{total_paragraphs}"
    )


    st.write(
        f"**Sentences:** "
        f"{total_sentences}"
    )
