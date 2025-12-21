import pdfplumber
import io
from typing import Optional

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF using pdfplumber
    """
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF parsing error: {e}")
        return ""

def extract_contact_info(text: str) -> dict:
    """
    Extract basic contact information using regex
    """
    import re
    
    contact_info = {
        "email": None,
        "phone": None,
        "linkedin": None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        contact_info["email"] = emails[0]
    
    # Phone pattern
    phone_pattern = r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        contact_info["phone"] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if linkedins:
        contact_info["linkedin"] = linkedins[0]
    
    return contact_info