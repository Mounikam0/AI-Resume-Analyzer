from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from services.pdf_parser import extract_text_from_pdf
from services.analyzer import analyze_resume_with_ai, match_job_description, generate_tailored_resume
from typing import Optional
import json

load_dotenv()

app = FastAPI(title="AI Resume Analyzer API - Enhanced")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Pydantic models
class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str

class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    location: Optional[str] = None
    summary: str
    experience: list
    education: list
    skills: list
    certifications: Optional[list] = []

class TailorRequest(BaseModel):
    resume_data: dict
    job_description: str

@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API - Enhanced", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai_configured": bool(GEMINI_API_KEY)}

@app.post("/api/analyze")
async def analyze_resume(file: UploadFile = File(...), job_description: Optional[str] = None):
    """
    Analyze uploaded resume PDF
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        analysis_result = await analyze_resume_with_ai(resume_text, job_description)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "extracted_text": resume_text[:500] + "...",  # First 500 chars
            "analysis": analysis_result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/match-job")
async def match_job(request: JobMatchRequest):
    """
    Match resume against job description
    """
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        match_result = await match_job_description(request.resume_text, request.job_description)
        
        return JSONResponse(content={
            "success": True,
            "match": match_result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

@app.post("/api/tailor-resume")
async def tailor_resume(request: TailorRequest):
    """
    Generate tailored resume suggestions for specific job
    """
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        tailored = await generate_tailored_resume(request.resume_data, request.job_description)
        
        return JSONResponse(content={
            "success": True,
            "tailored_resume": tailored
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tailoring failed: {str(e)}")

@app.post("/api/improve-section")
async def improve_section(section_text: str, section_type: str):
    """
    Get AI suggestions to improve a specific resume section
    """
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
        As a professional resume writer, improve this {section_type} section:
        
        Current text:
        {section_text}
        
        Provide 3 improved versions with:
        - Strong action verbs
        - Quantifiable achievements
        - Professional tone
        - ATS-friendly keywords
        
        Return as JSON:
        {{
            "suggestions": ["version1", "version2", "version3"],
            "tips": ["tip1", "tip2", "tip3"]
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Clean response
        response_text = response.text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        result = json.loads(response_text.strip())
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Improvement failed: {str(e)}")

@app.post("/api/generate-resume")
async def generate_resume(resume_data: ResumeData):
    """
    Generate formatted resume from data
    """
    try:
        # Here you would generate PDF or formatted HTML
        # For now, return success
        return JSONResponse(content={
            "success": True,
            "message": "Resume generated successfully",
            "data": resume_data.dict()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)