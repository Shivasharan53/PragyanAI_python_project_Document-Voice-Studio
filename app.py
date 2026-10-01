import streamlit as st
from pypdf import PdfReader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Document Voice Studio",
    page_icon="🎙️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎙️ Document Voice Studio")

st.write(
    "Upload a PDF and read it page by page."
)


# ============================================================
# PDF UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload your PDF",
    type=["pdf"]
)


# ============================================================
# SESSION STATE
# ============================================================

if "pages" not in st.session_state:

    st.session_state.pages = []

if "current_page" not in st.session_state:

    st.session_state.current_page = 0


# ============================================================
# READ PDF
# ============================================================

if uploaded_file is not None:

    # Check whether a new PDF was uploaded

    file_id = (
        uploaded_file.name,
        uploaded_file.size
    )

    if st.session_state.get("file_id") != file_id:

        reader = PdfReader(uploaded_file)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pages.append(text.strip())

            else:

                pages.append(
                    "⚠️ No readable text found on this page."
                )

        st.session_state.pages = pages

        st.session_state.current_page = 0

        st.session_state.file_id = file_id


# ============================================================
# DISPLAY DOCUMENT
# ============================================================

if st.session_state.pages:

    pages = st.session_state.pages

    total_pages = len(pages)

    current_page = st.session_state.current_page


    # ========================================================
    # PAGE INFORMATION
    # ========================================================

    st.subheader("📑 Document Viewer")

    st.write(
        f"📄 Total Pages: **{total_pages}**"
    )

    st.write(
        f"📖 Current Page: **{current_page + 1} / {total_pages}**"
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

        if selected_page - 1 != current_page:

            st.session_state.current_page = (
                selected_page - 1
            )

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

            st.rerun()


    # ========================================================
    # CURRENT PAGE TEXT
    # ========================================================

    st.subheader(
        f"📖 Page {current_page + 1}"
    )

    current_text = pages[current_page]


    if current_text:

        st.text_area(
            "Page Content",
            value=current_text,
            height=450
        )

    else:

        st.warning(
            "No readable text found on this page."
        )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.info(
        "👆 Upload a PDF above to start."
    )
