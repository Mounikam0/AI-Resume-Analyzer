import streamlit as st
import requests
import json

# ------------------------
# Page configuration
# ------------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="centered")

# ------------------------
# Gradient background and card styling
# ------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(to bottom, #fadcd5, #4b2138);
        color: #4b2138;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Cards */
    .card {
        background-color: rgba(250,220,213,0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 3px 3px 20px rgba(75,33,56,0.3);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 5px 5px 25px rgba(75,33,56,0.5);
    }

    /* Headers inside cards */
    .card h4 {
        color: #4b2138;
        font-weight: 600;
        font-size: 20px;
    }

    /* Score styling */
    .score {
        font-size: 28px;
        font-weight: 700;
        color: #3e0f2f; /* Slightly darker for contrast */
        background: linear-gradient(90deg, #4b2138, #fadcd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Buttons */
    button, .stButton>button {
        background-color: #fadcd5;
        color: #4b2138;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: 600;
        font-size: 16px;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    button:hover, .stButton>button:hover {
        background-color: #f7c8c0;
        transform: translateY(-2px);
    }

    /* File uploader */
    .stFileUploader>div>div>input {
        color: #4b2138;
    }

    /* Main header */
    .stTitle, h1, h2, h3 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 700;
        color: #3e0f2f;
    }

    /* Body text */
    .stMarkdown, p {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 400;
        color: #4b2138;
        font-size: 16px;
    }

    /* 🌟 AI Suggestion Box Fix (newly added) */
    .stMarkdown div, .stMarkdown pre, .stMarkdown p {
        color: #4b2138 !important;
        background-color: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 10px;
        line-height: 1.6;
    }
    </style>

    """,
    unsafe_allow_html=True
)

# ------------------------
# Header
# ------------------------
st.title("🚀 AI Resume Analyzer")
st.markdown(
    "Upload your resume and select a role to see your skill match and AI suggestions. "
    "Let's help you **fly higher in your career!**"
)

# ------------------------
# Load roles from skills_db.json
# ------------------------
with open("C:/Users/mouni/Desktop/personal projects/Resume_analyser/skills_db.json", "r", encoding="utf-8") as f:
    skills_db = json.load(f)
roles = list(skills_db.keys())

# ------------------------
# Resume upload and role selection
# ------------------------
uploaded_file = st.file_uploader("Choose your PDF resume", type="pdf")
role = st.selectbox("Select your role", roles)

# ------------------------
# Analyze button
# ------------------------
if st.button("Analyze"):
    if not uploaded_file:
        st.error("Please upload a PDF file!")
    elif not role:
        st.error("Please select a role!")
    else:
        with st.spinner("Analyzing your resume and generating AI suggestions..."):
            try:
                # Call backend
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files={"file": uploaded_file},
                    data={"role": role}
                )

                if response.status_code == 200:
                    result = response.json()
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # ------------------------
                        # Display results
                        # ------------------------
                        st.markdown(
                            f'<div class="card"><span class="score">Skill Match Score: {result["score"]}%</span></div>',
                            unsafe_allow_html=True
                        )

                        st.markdown('<div class="card"><h4>✅ Found Skills</h4></div>', unsafe_allow_html=True)
                        st.write(result["found"] if result["found"] else "None found")

                        st.markdown('<div class="card"><h4>⚠️ Missing Skills</h4></div>', unsafe_allow_html=True)
                        st.write(result["missing"] if result["missing"] else "None missing")

                        st.markdown('<div class="card"><h4>💡 AI Suggestions</h4></div>', unsafe_allow_html=True)
                        st.write(result["suggestion"])
                else:
                    st.error(f"Error: {response.json()}")

            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
