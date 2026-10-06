import pandas as pd
import pytesseract

from PIL import Image
from pypdf import PdfReader
from docx import Document


def extract_from_txt(file):
    content = file.read()

    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")

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

        text.append(f"Sheet: {sheet}")
        text.append(df.to_string(index=False))

    return "\n".join(text)


def extract_from_image(file):
    image = Image.open(file)

    text = pytesseract.image_to_string(image)

    return text


def extract_text(file):
    """
    Extract text from supported file types.
    """

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

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_from_image(file)

    else:
        raise ValueError(
            "Unsupported file type. "
            "Please upload TXT, PDF, DOCX, CSV, XLSX, PNG, JPG or JPEG."
        )