from PyPDF2 import PdfReader

def extract_pdf_text(file_path):
    try:
        reader = PdfReader(file_path)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        from .logger import logger
        logger.error(f"Failed to extract PDF text: {e}")
        return ""

def split_text(content, parts=3):
    if not content:
        return []
    content = f"""<start_context>
    ### CEMENTING MANUAL
    {content}
    <end_context>"""
    length = len(content)
    chunk_size = max(1, length // parts)
    return [content[i*chunk_size:(i+1)*chunk_size] for i in range(parts)]