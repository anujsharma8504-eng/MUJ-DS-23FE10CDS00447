"""
Utility helpers: PDF text extraction.
"""

from pypdf import PdfReader


def extract_text_from_pdf(file) -> str:
    """
    Extract all text from a PDF file-like object.

    Args:
        file: A file-like object (e.g. from Streamlit's file_uploader)
              or a path string.

    Returns:
        The concatenated text of all pages, or an empty string on failure.
    """
    try:
        reader = PdfReader(file)
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages).strip()
    except Exception as e:
        print(f"[utils] Failed to extract PDF text: {e}")
        return ""