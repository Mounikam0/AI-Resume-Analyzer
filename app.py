import streamlit as st
import json
import io
import os
import time
import spacy
import subprocess
from pdfminer.high_level import extract_text
from rapidfuzz import fuzz
import plotly.graph_objects as go
from frontend import render_global_styles, render_header, render_footer


# ---------------------------
# 🔧 App Configuration
# ---------------------------
st.set_page_config(page_title="AI Resume & Skill Gap Analyzer",
                   page_icon="🤖", layout="wide")

render_global_styles()
render_header()

# Load NLP model and skills database
nlp = spacy.load("en_core_web_sm")

current_dir = os.path.dirname(os.path.abspath(__file__))
skills_db_path = os.path.join(current_dir, "skills_db.json")

with open(skills_db_path, "r", encoding="utf-8") as f:
    SKILLS_DB = json.load(f)


# ---------------------------
# 🧠 Helper Functions
# ---------------------------
def extract_text_from_pdf(file_bytes):
    try:
        return extract_text(io.BytesIO(file_bytes))
    except Exception as e:
        st.error(f"PDF text extraction failed: {e}")
        return ""


def extract_skills_from_text(text, role_skills, fuzzy_threshold=80):
    found = set()
    text_lower = text.lower()
    for skill in role_skills:
        if skill.lower() in text_lower:
            found.add(skill)
        elif fuzz.partial_ratio(skill.lower(), text_lower) >= fuzzy_threshold:
            found.add(skill)
    return sorted(list(found))


def analyze_resume(text, selected_role):
    role_info = SKILLS_DB.get(selected_role)
    if not role_info:
        return {"error": "Role not found"}
    role_skills = role_info["skills"]
    found = extract_skills_from_text(text, role_skills)
    missing = [s for s in role_skills if s not in found]
    score = int((len(found) / len(role_skills)) * 100) if role_skills else 0
    return {
        "role": selected_role,
        "found_skills": found,
        "missing_skills": missing,
        "score": score,
        "suggestions": {
            s: role_info.get("resources", {}).get(s.lower(), []) for s in missing
        },
    }


def generate_ai_suggestions_ollama(found, missing, role):
    if not missing:
        return "✅ Great! You already have most of the key skills for this role."

    prompt = f"""You are an expert career advisor helping someone prepare for a {role} job.
Found skills: {', '.join(found)}
Missing skills: {', '.join(missing)}

Suggest 3 practical, motivational ways to learn the missing skills quickly.
Keep it concise, friendly, and professional.
"""
    try:
        subprocess.run(["ollama", "serve"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import ollama
        res = ollama.chat(
            model="tinyllama:latest",
            messages=[
                {"role": "system", "content": "You are a professional AI career coach."},
                {"role": "user", "content": prompt}
            ]
        )
        return res["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Offline AI unavailable: {e}"


# ---------------------------
# 🧭 Sidebar
# ---------------------------
with st.sidebar:
    if os.path.exists("logo.png") and os.path.getsize("logo.png") > 0:
        st.image("logo.png", width=140)
    else:
        st.markdown("<h2 style='color:#002B5B;'>AI Resume Analyzer</h2>", unsafe_allow_html=True)

    st.markdown("**Your personal skill-gap coach.**")
    st.markdown("---")
    ai_mode = st.selectbox("AI Mode", ["Offline (Ollama)", "None (no AI)"])
    st.markdown("---")
    st.info("💡 Tip: Try with a real resume (PDF format only).")


# ---------------------------
# 📂 Tabs Layout
# ---------------------------
tab1, tab2, tab3 = st.tabs(["🧾 Upload Resume", "📊 Analysis Results", "💡 AI Suggestions"])


# --- Tab 1: Upload ---
with tab1:
    st.markdown("""
    <div class='stCard fade-in'>
        <h3>📄 Upload Your Resume</h3>
        <p>Upload your resume in PDF format and select your target job role.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Resume", type=["pdf"])
    role = st.selectbox("🎯 Target Job Role", list(SKILLS_DB.keys()))

    if st.button("🔍 Analyze Resume"):
        if not uploaded:
            st.warning("Please upload a resume first.")
        else:
            with st.spinner("Analyzing your resume..."):
                text = extract_text_from_pdf(uploaded.read())
                if not text.strip():
                    st.error("Couldn't extract text. Try another PDF.")
                else:
                    result = analyze_resume(text, role)
                    st.session_state["analysis"] = result
                    st.success("✅ Analysis complete! Check the next tab.")
                    st.balloons()


# --- Tab 2: Analysis Results ---
with tab2:
    result = st.session_state.get("analysis")
    if not result:
        st.info("Please analyze a resume first.")
    else:
        st.markdown(f"<h3>📊 Analysis for: {result['role']}</h3>", unsafe_allow_html=True)

        # Score animation
        st.progress(result["score"] / 100)
        st.markdown(f"<h4>🏁 Resume Match Score: {result['score']}%</h4>", unsafe_allow_html=True)

        # Bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Matched", x=["Skills"], y=[len(result["found_skills"])], marker_color="green"))
        fig.add_trace(go.Bar(name="Missing", x=["Skills"], y=[len(result["missing_skills"])], marker_color="crimson"))
        fig.update_layout(barmode="group", title="Skill Comparison", height=350)
        st.plotly_chart(fig, width="stretch")


        # Found Skills
        st.markdown("### ✅ Found Skills")
        if result["found_skills"]:
            st.write(", ".join(result["found_skills"]))
        else:
            st.warning("No matching skills detected.")

        # Missing Skills
        st.markdown("### ❌ Missing Skills & Resources")
        if result["missing_skills"]:
            for s in result["missing_skills"]:
                st.markdown(f"**{s}**")
                links = result["suggestions"].get(s, [])
                if links:
                    for l in links:
                        st.markdown(f"🔗 [Learn here]({l})")
                else:
                    st.text("No resource found. Search tutorials online.")
        else:
            st.success("🎉 All required skills are listed!")

        # Download Report
        st.download_button(
            "📥 Download Report",
            data=json.dumps(result, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )


# --- Tab 3: AI Suggestions ---
with tab3:
    result = st.session_state.get("analysis")
    if not result:
        st.info("Analyze a resume to get AI suggestions.")
    elif ai_mode == "None (no AI)":
        st.warning("AI mode is off. Change it in the sidebar.")
    else:
        st.markdown("### 💡 Personalized AI Suggestions")
        with st.spinner("🤖 Generating AI insights..."):
            text = generate_ai_suggestions_ollama(
                result["found_skills"], result["missing_skills"], result["role"]
            )
        if text.startswith("⚠️"):
            st.error(text)
        else:
            st.markdown(f"<div class='stCard fade-in'>{text}</div>", unsafe_allow_html=True)


render_footer()
