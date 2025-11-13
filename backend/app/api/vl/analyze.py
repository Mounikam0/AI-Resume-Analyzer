from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from app.services.parser import extract_text_from_pdf_bytes, analyze_text_for_role
from app.services.ollama_client import generate_ai_suggestions

router = APIRouter()

@router.post("/upload")
async def upload_and_analyze(file: UploadFile = File(...), role: str = Form(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF supported")
    file_bytes = await file.read()
    text = extract_text_from_pdf_bytes(file_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    analysis = analyze_text_for_role(text, role)   # reuse your analyze_resume logic
    return {"analysis": analysis}

@router.post("/ai_suggestions")
async def ai_suggestions(role: str, found: Optional[str] = None, missing: Optional[str] = None):
    # missing, found can be comma-separated lists
    found_list = found.split(",") if found else []
    missing_list = missing.split(",") if missing else []
    return {"ai": generate_ai_suggestions(found_list, missing_list, role)}
