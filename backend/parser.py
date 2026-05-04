import pdfplumber
import re

import io

def extract_text_from_pdf(input_data) -> str:
    """
    Extract clean text from PDF using pdfplumber.
    input_data can be a file path (str) or raw bytes.
    """
    
    # If input is bytes, wrap it in BytesIO so pdfplumber can 'seek'
    if isinstance(input_data, bytes):
        input_data = io.BytesIO(input_data)

    text_parts = []
    with pdfplumber.open(input_data) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()

def normalize_text(text: str) -> str:
    # Remove PDF encoding artifacts
    text = re.sub(r'\(cid:\d+\)', ' ', text)

    # Remove non-ASCII junk
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Normalize spaces inside lines (NOT newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    # Clean excessive newlines
    text = re.sub(r'\n+', '\n', text)

    # Lower the text
    text = text.lower()
    
    return text

