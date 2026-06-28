from PyPDF2 import PdfReader
from docx import Document


def extract_text(file):
    """
    Extracts text from an uploaded resume file.
    Supports both PDF and DOCX, based on the file's name extension.
    """

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_from_pdf(file)

    elif filename.endswith(".docx"):
        return _extract_from_docx(file)

    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."


def _extract_from_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def _extract_from_docx(file):
    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"

    return text