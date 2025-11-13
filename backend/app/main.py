from fastapi import FastAPI, UploadFile, Form
from pdfminer.high_level import extract_text
from fastapi.middleware.cors import CORSMiddleware
import json, io, ollama, os

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Fix: Use absolute path so FastAPI can always find skills_db.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILLS_DB_PATH = os.path.join(BASE_DIR, "skills_db.json")

# Load skill database
with open(SKILLS_DB_PATH, "r", encoding="utf-8") as f:
    SKILLS_DB = json.load(f)

@app.post("/analyze")
async def analyze_resume(file: UploadFile, role: str = Form(...)):
    content = await file.read()
    text = extract_text(io.BytesIO(content))

    role_info = SKILLS_DB.get(role)
    if not role_info:
        return {"error": f"Role '{role}' not found in skills database."}

    found = [s for s in role_info["skills"] if s.lower() in text.lower()]
    missing = [s for s in role_info["skills"] if s not in found]
    score = int((len(found)/len(role_info["skills"])) * 100)

    prompt = f"You are a career coach. The user is preparing for {role}. Missing: {', '.join(missing)}"
    try:
        res = ollama.chat(model="tinyllama:latest", messages=[{"role":"user","content":prompt}])
        suggestion = res["message"]["content"]
    except Exception:
        suggestion = "⚠️ AI unavailable. Please retry."

    return {
        "role": role,
        "score": score,
        "found": found,
        "missing": missing,
        "suggestion": suggestion
    }
