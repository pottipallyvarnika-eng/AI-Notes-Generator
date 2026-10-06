import streamlit as st

from utils.file_processor import extract_text
from utils.text_processor import (
    clean_text,
    extract_keywords,
    simple_summary
)
from utils.ai_generator import generate_ai_notes


st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Notes Generator")

st.write(
    "Generate clear and structured study notes from "
    "PDF, DOCX, TXT, Excel, CSV and image files."
)


# Sidebar
st.sidebar.header("⚙️ Settings")

student_level = st.sidebar.selectbox(
    "Student Level",
    [
        "School Student",
        "Intermediate Student",
        "B.Tech Student",
        "College Student"
    ]
)

topic = st.sidebar.text_input(
    "Topic",
    placeholder="Example: Artificial Intelligence"
)


# Input section
st.header("📥 Input Material")

input_method = st.radio(
    "Choose input method:",
    [
        "Upload File",
        "Enter Text"
    ]
)


text = ""


if input_method == "Upload File":

    uploaded_file = st.file_uploader(
        "Upload your study material",
        type=[
            "txt",
            "pdf",
            "docx",
            "csv",
            "xlsx",
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if uploaded_file:

        try:

            with st.spinner("Extracting text..."):

                text = extract_text(uploaded_file)

            st.success("Text extracted successfully!")

        except Exception as e:

            st.error(f"Error: {e}")


else:

    text = st.text_area(
        "Enter your study material",
        height=300,
        placeholder="Paste your study material here..."
    )


# Process text
if text.strip():

    cleaned_text = clean_text(text)

    st.header("📄 Extracted Content")

    with st.expander("View extracted text"):

        st.write(cleaned_text)


    # Basic analysis
    st.header("📊 Text Analysis")

    col1, col2, col3 = st.columns(3)

    word_count = len(cleaned_text.split())

    sentence_count = len(
        cleaned_text.split(".")
    )

    keywords = extract_keywords(
        cleaned_text,
        number=10
    )


    with col1:
        st.metric(
            "Words",
            word_count
        )

    with col2:
        st.metric(
            "Sentences",
            sentence_count
        )

    with col3:
        st.metric(
            "Keywords",
            len(keywords)
        )


    if keywords:

        st.subheader("🔑 Important Keywords")

        st.write(
            ", ".join(keywords)
        )


    # Basic summary
    st.header("📝 Quick Summary")

    summary = simple_summary(
        cleaned_text,
        sentence_count=5
    )

    st.write(summary)


    # AI notes
    st.header("🤖 AI Notes")

    if st.button(
        "Generate AI Notes",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Please enter a topic in the sidebar."
            )

        else:

            try:

                with st.spinner(
                    "AI is generating your notes..."
                ):

                    notes = generate_ai_notes(
                        cleaned_text,
                        topic,
                        student_level
                    )

                st.session_state["notes"] = notes

                st.success(
                    "AI notes generated successfully!"
                )

            except Exception as e:

                st.error(
                    f"AI generation failed: {e}"
                )


# Display generated notes
if "notes" in st.session_state:

    st.header("📚 Generated Notes")

    st.markdown(
        st.session_state["notes"]
    )


    # Download
    st.download_button(
        label="⬇️ Download Notes",
        data=st.session_state["notes"],
        file_name="AI_Notes.txt",
        mime="text/plain"
    )