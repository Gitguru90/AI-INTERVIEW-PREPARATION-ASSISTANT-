import streamlit as st
from utils.resume_parser import extract_text
from utils.gemini import analyze_resume

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

/* Animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Animated glowing title */
.main-title{
    font-size:48px;
    font-weight:800;
    text-align:center;
    background: linear-gradient(90deg, #6366F1, #EC4899, #F59E0B, #6366F1);
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 4s linear infinite, popIn 0.8s ease-out;
}

@keyframes shine {
    to { background-position: 300% center; }
}

@keyframes popIn {
    0% { opacity: 0; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1); }
}

/* Glassmorphism cards */
.card{
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    padding:20px;
    border-radius:18px;
    text-align:center;
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover{
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 10px 30px rgba(99,102,241,0.4);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6366F1, #EC4899);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 18px rgba(236,72,153,0.6);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 12px;
    border: 1px solid rgba(99,102,241,0.3);
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <p class="main-title">
    🎤 AI Interview Preparation Assistant
    </p>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("🎤 AI Interview")
    st.write("Practice • Analyze • Improve")

st.markdown("Practice interviews, improve your skills, and track your progress.")
st.write("")

features = [
    ("🧠", "Resume Analysis"),
    ("📝", "MCQ Interviews"),
    ("💬", "Descriptive Interviews"),
    ("💻", "Coding Interviews"),
    ("✅", "AI Evaluation"),
    ("📈", "Progress Dashboard"),
]

cols = st.columns(3)
for i, (icon, label) in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f"""<div class="card">
                <div style="font-size:32px;">{icon}</div>
                <div style="font-weight:600;margin-top:8px;">{label}</div>
            </div>""",
            unsafe_allow_html=True
        )
        st.write("")

st.divider()

# Resume Upload
st.subheader("📄 Upload Resume")

resume = st.file_uploader(
    "Upload your Resume (PDF/DOCX)",
    type=["pdf", "docx"]
)

if resume is not None:

    st.success("Resume Uploaded Successfully!")

    # Extract text from PDF/DOCX
    resume_text = extract_text(resume)

    # Send to Gemini — analyze_resume itself needs to be updated
    # to return short bullet points (see utils/gemini.py fix needed)
    analysis = analyze_resume(resume_text)

    st.subheader("📊 AI Resume Analysis")
    st.markdown(analysis)

st.divider()

st.info("Use the sidebar to start your interview.")