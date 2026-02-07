import pypdf
import pytesseract
from PIL import Image
import io

# Configure Tesseract path if needed, though simpler to rely on PATH or environment
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract.exe'

def extract_text_from_pdf(file_stream):
    """Extracts text from a PDF file stream."""
    try:
        reader = pypdf.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def extract_text_from_image(file_stream):
    """Extracts text from an image file stream using OCR."""
    try:
        image = Image.open(file_stream)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise Exception(f"Error performing OCR on image: {str(e)}")

def process_resume_upload(uploaded_file):
    """
    Determines file type and extracts text.
    Returns: Extracted text (str)
    """
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        return extract_text_from_image(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or Image.")


def is_resume(text):
    """
    Heuristic check to see if text looks like a resume.
    """
    keywords = [
        "experience", "education", "skills", "projects", "summary", "profile",
        "curriculum vitae", "resume", "work history", "contact", "languages", 
        "certifications", "achievements", "employment", "professional summary"
    ]
    
    text_lower = text.lower()
    match_count = sum(1 for keyword in keywords if keyword in text_lower)
    
    # Threshold: must contain at least 2 common resume keywords
    return match_count >= 2
