
import io
import fitz

def extract_text_from_pdf(file: io.BufferedReader) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    :param file: File object representing the uploaded PDF.
    :return: Extracted text as a string.
    """
    pdf_reader = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    
    for page_num in range(len(pdf_reader)): 
        page = pdf_reader.load_page(page_num)
        text += page.get_text("text")

    return text