from pdfminer.high_level import extract_text
from rapidfuzz import fuzz

def extract_text_from_pdf_bytes(file_bytes):
    """Extract text from PDF bytes."""
    try:
        return extract_text(file_bytes)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")

def analyze_text_for_role(text, role_skills, fuzzy_threshold=80):
    """Analyze text for matching skills based on a role."""
    found_skills = set()
    text_lower = text.lower()

    # Direct matches
    for skill in role_skills:
        if skill.lower() in text_lower:
            found_skills.add(skill)

    # Fuzzy matches
    for skill in role_skills:
        if skill in found_skills:
            continue
        score = fuzz.partial_ratio(skill.lower(), text_lower)
        if score >= fuzzy_threshold:
            found_skills.add(skill)

    return sorted(list(found_skills))