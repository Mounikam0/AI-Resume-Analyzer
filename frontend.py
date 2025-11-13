import streamlit as st

def render_global_styles():
    st.markdown("""
    <style>
    /* ===== Global Theme ===== */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
        color: #1e293b;
    }

    /* ===== Cards ===== */
    .stCard {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.2s ease-in-out;
    }
    .stCard:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }

    /* ===== Buttons ===== */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(90deg, #1e40af, #2563eb);
        transform: scale(1.03);
    }

    /* ===== Headings ===== */
    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 700;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: #f1f5f9;
        border-right: 2px solid #e2e8f0;
    }

    /* ===== Animations ===== */
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ===== Footer ===== */
    .footer {
        margin-top: 30px;
        font-size: 13px;
        color: #64748b;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style='text-align:center; margin-bottom:30px;' class='fade-in'>
        <h1 style='color:#1e3a8a;'>🤖 AI Resume & Skill Gap Analyzer</h1>
        <p style='color:#475569; font-size:16px;'>Your smart career companion for skill improvement</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class='footer'>
        © 2025 AI Resume Analyzer — Designed with 💙 for smart learners.
    </div>
    """, unsafe_allow_html=True)
