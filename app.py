import os
import re

import streamlit as st
import pandas as pd
import pytesseract

from PIL import Image
from pypdf import PdfReader
from docx import Document

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer

from google import genai
load_dotenv()

st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="📚",
    layout="wide"
)
def extract_from_txt(file):
    content = file.read()

    if isinstance(content, bytes):
        content = content.decode(
            "utf-8",
            errors="ignore"
        )

    return content


def extract_from_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_from_docx(file):
    document = Document(file)

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_from_csv(file):
    df = pd.read_csv(file)

    return df.to_string(index=False)


def extract_from_xlsx(file):

    excel_file = pd.ExcelFile(file)

    text = []

    for sheet in excel_file.sheet_names:

        df = pd.read_excel(
            file,
            sheet_name=sheet
        )

        text.append(
            f"Sheet: {sheet}"
        )

        text.append(
            df.to_string(index=False)
        )

    return "\n".join(text)


def extract_from_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(
        image
    )

    return text


def extract_text(file):

    filename = file.name.lower()

    if filename.endswith(".txt"):

        return extract_from_txt(file)

    elif filename.endswith(".pdf"):

        return extract_from_pdf(file)

    elif filename.endswith(".docx"):

        return extract_from_docx(file)

    elif filename.endswith(".csv"):

        return extract_from_csv(file)

    elif filename.endswith(".xlsx"):

        return extract_from_xlsx(file)

    elif filename.endswith(
        (".png", ".jpg", ".jpeg")
    ):

        return extract_from_image(file)

    else:

        raise ValueError(
            "Unsupported file type."
        )
def clean_text(text):

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def split_into_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def extract_keywords(
    text,
    number=10
):

    if not text.strip():
        return []

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=number
        )

        matrix = vectorizer.fit_transform(
            [text]
        )

        words = vectorizer.get_feature_names_out()

        return list(words)

    except Exception:

        return []


def create_summary(
    text,
    sentence_count=5
):

    sentences = split_into_sentences(
        text
    )

    if len(sentences) <= sentence_count:

        return " ".join(sentences)

    return " ".join(
        sentences[:sentence_count]
    )
def generate_ai_notes(
    text,
    topic,
    student_level
):

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are an expert educational notes generator.

Create clear, accurate and easy-to-understand
study notes from the material provided below.

Topic:
{topic}

Student Level:
{student_level}

Source Material:
{text}

Create the notes using the following structure:

# {topic}

## 1. Overview
Give a simple introduction to the topic.

## 2. Important Concepts
Explain the main concepts clearly.

## 3. Key Points
Give important points using bullet points.

## 4. Detailed Explanation
Explain the topic in simple language.

## 5. Important Terms
List important terms and their meanings.

## 6. Examples
Give suitable examples.

## 7. Quick Revision
Give a short revision section.

## 8. Possible Exam Questions
Give 5 important questions that may
be asked in an examination.

Requirements:

- Use simple language.
- Make the notes suitable for students.
- Use headings and bullet points.
- Do not unnecessarily repeat information.
- Do not invent information that is not supported
  by the source material.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
st.title(
    "📚 AI Notes Generator"
)

st.write(
    "Generate simple and structured study notes "
    "from your learning materials using AI."
)
st.sidebar.title(
    "⚙️ Settings"
)

student_level = st.sidebar.selectbox(
    "Select Student Level",
    [
        "School Student",
        "Intermediate Student",
        "B.Tech Student",
        "College Student"
    ]
)

topic = st.sidebar.text_input(
    "Enter Topic",
    placeholder="Example: Artificial Intelligence"
)
st.header(
    "📥 Input Material"
)

input_method = st.radio(
    "Choose Input Method",
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

            with st.spinner(
                "Extracting text..."
            ):

                text = extract_text(
                    uploaded_file
                )

            if text.strip():

                st.success(
                    "Text extracted successfully!"
                )

            else:

                st.warning(
                    "No text could be extracted "
                    "from this file."
                )

        except Exception as error:

            st.error(
                f"Error while reading file: {error}"
            )
else:

    text = st.text_area(
        "Enter your study material",
        height=300,
        placeholder=(
            "Paste your study material here..."
        )
    )
if text.strip():

    cleaned_text = clean_text(
        text
    )
    st.header(
        "📄 Extracted Content"
    )

    with st.expander(
        "View Extracted Text"
    ):

        st.write(
            cleaned_text
        )
    st.header(
        "📊 Text Analysis"
    )

    words = cleaned_text.split()

    sentences = split_into_sentences(
        cleaned_text
    )

    keywords = extract_keywords(
        cleaned_text,
        10
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Word Count",
            len(words)
        )


    with col2:

        st.metric(
            "Sentence Count",
            len(sentences)
        )


    with col3:

        st.metric(
            "Keywords",
            len(keywords)
        )
    if keywords:

        st.subheader(
            "🔑 Important Keywords"
        )

        st.write(
            ", ".join(keywords)
        )
    st.header(
        "📝 Quick Summary"
    )

    summary = create_summary(
        cleaned_text,
        5
    )

    st.write(
        summary
    )
    st.header(
        "🤖 AI Generated Notes"
    )

    if st.button(
        "✨ Generate AI Notes",
        type="primary"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a topic "
                "in the sidebar."
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

                st.session_state[
                    "generated_notes"
                ] = notes

                st.success(
                    "AI notes generated successfully!"
                )

            except Exception as error:

                st.error(
                    f"AI generation failed: {error}"
                )
if "generated_notes" in st.session_state:

    st.header(
        "📚 Generated Study Notes"
    )

    st.markdown(
        st.session_state[
            "generated_notes"
        ]
    )
    st.download_button(
        label="⬇️ Download Notes",
        data=st.session_state[
            "generated_notes"
        ],
        file_name="AI_Notes.txt",
        mime="text/plain"
    )