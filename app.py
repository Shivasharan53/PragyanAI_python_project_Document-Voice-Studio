# ============================================================
# DOCUMENT VOICE STUDIO
# PDF + PAGE VIEWER + STATISTICS + PARAGRAPHS + SENTENCES
# + MULTILINGUAL TRANSLATION + CLEAR ALL
# ============================================================

import streamlit as st
from pypdf import PdfReader
from deep_translator import GoogleTranslator
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Document Voice Studio",
    page_icon="🎙️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.title {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "pages" not in st.session_state:
    st.session_state.pages = []

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "file_id" not in st.session_state:
    st.session_state.file_id = None

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "translated_page_id" not in st.session_state:
    st.session_state.translated_page_id = None


# ============================================================
# CLEAR ALL FUNCTION
# ============================================================

def clear_all():

    # Clear document
    st.session_state.pages = []

    # Reset page
    st.session_state.current_page = 0

    # Reset uploaded file tracking
    st.session_state.file_id = None

    # Clear translation
    st.session_state.translated_text = ""

    st.session_state.translated_page_id = None

    # Remove uploader state
    if "pdf_uploader" in st.session_state:
        del st.session_state["pdf_uploader"]


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🎙️ Document Voice Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Read, analyse and translate your documents.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

LANGUAGES = {

    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Nepali": "ne",

    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN"
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Document Controls")


    # ========================================================
    # PDF UPLOAD
    # ========================================================

    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"],
        key="pdf_uploader"
    )


    st.divider()


    # ========================================================
    # LANGUAGE
    # ========================================================

    st.subheader("🌐 Translation Language")

    target_language_name = st.selectbox(
        "Choose target language",
        list(LANGUAGES.keys())
    )

    target_language = LANGUAGES[
        target_language_name
    ]


    st.divider()


    # ========================================================
    # CLEAR ALL BUTTON
    # ========================================================

    st.subheader("🧹 Reset")


    clear_button = st.button(
        "🧹 Clear All",
        use_container_width=True,
        type="secondary"
    )


    if clear_button:

        clear_all()

        st.rerun()


# ============================================================
# PDF EXTRACTION FUNCTION
# ============================================================

def extract_pdf(file):

    pages = []

    try:

        reader = PdfReader(file)

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pages.append(
                    text.strip()
                )

            else:

                pages.append(
                    "⚠️ No readable text found on this page."
                )

        return pages

    except Exception as e:

        st.error(
            f"PDF extraction error: {e}"
        )

        return []


# ============================================================
# PARAGRAPH FUNCTION
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
# SENTENCE FUNCTION
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
# TRANSLATION FUNCTION
# ============================================================

def translate_text(
    text,
    target_language
):

    if not text.strip():

        return ""


    try:

        translator = GoogleTranslator(
            source="auto",
            target=target_language
        )


        # ----------------------------------------------------
        # Split large text into smaller chunks
        # ----------------------------------------------------

        words = text.split()

        chunks = []

        current_chunk = ""


        for word in words:

            if (
                len(current_chunk)
                + len(word)
                > 3500
            ):

                if current_chunk:

                    chunks.append(
                        current_chunk
                    )

                current_chunk = word

            else:

                if current_chunk:

                    current_chunk += " "

                current_chunk += word


        if current_chunk:

            chunks.append(
                current_chunk
            )


        # ----------------------------------------------------
        # Translate chunks
        # ----------------------------------------------------

        translated_chunks = []


        for chunk in chunks:

            translated = translator.translate(
                chunk
            )

            translated_chunks.append(
                translated
            )


        return " ".join(
            translated_chunks
        )


    except Exception as e:

        st.error(
            f"Translation error: {e}"
        )

        return ""


# ============================================================
# PROCESS UPLOADED PDF
# ============================================================

if uploaded_file is not None:

    current_file_id = (
        uploaded_file.name,
        uploaded_file.size
    )


    # --------------------------------------------------------
    # New PDF detected
    # --------------------------------------------------------

    if (
        st.session_state.file_id
        != current_file_id
    ):

        st.session_state.pages = (
            extract_pdf(
                uploaded_file
            )
        )


        st.session_state.current_page = 0

        st.session_state.file_id = (
            current_file_id
        )


        # Clear old translation
        st.session_state.translated_text = ""

        st.session_state.translated_page_id = None


# ============================================================
# MAIN DOCUMENT APPLICATION
# ============================================================

if st.session_state.pages:

    pages = st.session_state.pages

    total_pages = len(pages)


    current_page = (
        st.session_state.current_page
    )


    current_text = pages[
        current_page
    ]


    # ========================================================
    # DOCUMENT VIEWER
    # ========================================================

    st.subheader("📑 Document Viewer")


    st.write(
        f"📄 Total Pages: **{total_pages}**"
    )


    st.write(
        f"📖 Current Page: "
        f"**{current_page + 1} / {total_pages}**"
    )


    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    # --------------------------------------------------------
    # PREVIOUS
    # --------------------------------------------------------

    with col1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True,
            disabled=current_page == 0
        ):

            st.session_state.current_page -= 1

            st.session_state.translated_text = ""

            st.rerun()


    # --------------------------------------------------------
    # PAGE NUMBER
    # --------------------------------------------------------

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

            st.session_state.translated_text = ""

            st.rerun()


    # --------------------------------------------------------
    # NEXT
    # --------------------------------------------------------

    with col3:

        if st.button(
            "Next ➡️",
            use_container_width=True,
            disabled=current_page == total_pages - 1
        ):

            st.session_state.current_page += 1

            st.session_state.translated_text = ""

            st.rerun()


    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.subheader(
        f"📖 Page {current_page + 1}"
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    character_count = len(
        current_text
    )


    word_count = len(
        current_text.split()
    )


    paragraphs = get_paragraphs(
        current_text
    )


    sentences = get_sentences(
        current_text
    )


    paragraph_count = len(
        paragraphs
    )


    sentence_count = len(
        sentences
    )


    # ========================================================
    # STATISTICS DASHBOARD
    # ========================================================

    st.subheader(
        "📊 Page Statistics"
    )


    col1, col2, col3, col4, col5 = st.columns(
        5
    )


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


    # ========================================================
    # ORIGINAL TEXT
    # ========================================================

    st.subheader(
        "📖 Original Page Content"
    )


    st.text_area(
        "Original Text",
        value=current_text,
        height=350
    )


    # ========================================================
    # PARAGRAPH EXPLORER
    # ========================================================

    st.subheader(
        "📝 Paragraph Explorer"
    )


    for index, paragraph in enumerate(
        paragraphs
    ):

        with st.expander(
            f"📝 Paragraph {index + 1}"
        ):

            st.write(
                paragraph
            )

            st.caption(
                f"{len(paragraph)} characters • "
                f"{len(paragraph.split())} words"
            )


    # ========================================================
    # SENTENCE EXPLORER
    # ========================================================

    st.subheader(
        "🔤 Sentence Explorer"
    )


    for index, sentence in enumerate(
        sentences
    ):

        with st.expander(
            f"🔤 Sentence {index + 1}"
        ):

            st.write(
                sentence
            )

            st.caption(
                f"{len(sentence)} characters • "
                f"{len(sentence.split())} words"
            )


    # ========================================================
    # TRANSLATION
    # ========================================================

    st.subheader(
        "🌐 Translation"
    )


    st.write(
        f"Selected language: "
        f"**{target_language_name}**"
    )


    translate_button = st.button(
        f"🌐 Translate Page → "
        f"{target_language_name}",
        type="primary",
        use_container_width=True
    )


    # ========================================================
    # TRANSLATE
    # ========================================================

    if translate_button:

        with st.spinner(
            f"Translating page into "
            f"{target_language_name}..."
        ):

            translated = translate_text(
                current_text,
                target_language
            )


        if translated:

            st.session_state.translated_text = (
                translated
            )

            st.session_state.translated_page_id = (
                current_page
            )

            st.success(
                "✅ Translation completed."
            )


    # ========================================================
    # SHOW TRANSLATION
    # ========================================================

    if (
        st.session_state.translated_text
        and
        st.session_state.translated_page_id
        == current_page
    ):

        st.subheader(
            f"🌐 {target_language_name} Translation"
        )


        st.text_area(
            "Translated Text",
            value=(
                st.session_state.translated_text
            ),
            height=350
        )


        # ----------------------------------------------------
        # TRANSLATED PARAGRAPHS
        # ----------------------------------------------------

        translated_paragraphs = (
            get_paragraphs(
                st.session_state.translated_text
            )
        )


        translated_sentences = (
            get_sentences(
                st.session_state.translated_text
            )
        )


        st.write(
            f"📝 Translated Paragraphs: "
            f"**{len(translated_paragraphs)}**"
        )


        st.write(
            f"🔤 Translated Sentences: "
            f"**{len(translated_sentences)}**"
        )


        # ----------------------------------------------------
        # TRANSLATED PARAGRAPH EXPLORER
        # ----------------------------------------------------

        st.subheader(
            "📝 Translated Paragraph Explorer"
        )


        for index, paragraph in enumerate(
            translated_paragraphs
        ):

            with st.expander(
                f"📝 Paragraph {index + 1}"
            ):

                st.write(
                    paragraph
                )


        # ----------------------------------------------------
        # TRANSLATED SENTENCE EXPLORER
        # ----------------------------------------------------

        st.subheader(
            "🔤 Translated Sentence Explorer"
        )


        for index, sentence in enumerate(
            translated_sentences
        ):

            with st.expander(
                f"🔤 Sentence {index + 1}"
            ):

                st.write(
                    sentence
                )


else:

    # ========================================================
    # EMPTY STATE
    # ========================================================

    st.info(
        "👆 Upload a PDF from the sidebar to start."
    )
