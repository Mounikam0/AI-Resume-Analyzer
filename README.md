🤖 AI Resume Analyzer Pro

An AI-powered tool that analyzes resumes, checks ATS compatibility, and matches resumes with job descriptions using Google Gemini 2.5.

✨ What It Does
📊 Resume Analysis

Upload a resume in PDF format

Get ATS compatibility insights

Feedback on structure, formatting, and content

Highlights missing skills and keywords

🎯 Job Matching

Compare your resume with a job description

Get a match percentage (0–100)

Shows matched vs missing skills

Actionable suggestions to improve your resume

🛠️ Tech Stack

Frontend

HTML, CSS, JavaScript

TailwindCSS

Font Awesome

Backend

Python 3.11+

FastAPI

Google Gemini 2.5

pdfplumber / PyPDF2

🔧 How to Run Locally
Requirements

Python 3.11 or above

Google Gemini API Key

Backend Setup

Open terminal and run:
# Clone project
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API Key
echo GEMINI_API_KEY=your_api_key_here > .env

# Start backend
python main.py

Backend runs at: http://localhost:8000

Frontend Setup

Open a second terminal:
cd frontend
python -m http.server 8080

Frontend runs at:http://localhost:8080

Then open the browser and visit:
http://localhost:8080

