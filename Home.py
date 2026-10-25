
import streamlit as st
from utils.groq_ai import analyze_resume, GroqCallError
from utils.resume_parser import extract_text

# Page configuration
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #6366F1, #EC4899, #F59E0B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.powered-badge {
    text-align: center;
    color: #d1d5db;
    font-size: 14px;
}

.card {
    background: rgba(255,255,255,0.07);
    padding: 24px 12px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.12);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.stButton > button {
    background: linear-gradient(90deg, #6366F1, #EC4899);
    color: white;
    border: none;
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 12px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<p class="main-title">🎤 AI Interview Preparation Assistant</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="powered-badge">⚡ Powered by Groq AI</p>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("🎤 AI Interview")
    st.write("Practice • Analyze • Improve")
    st.divider()
    st.markdown("⚡ **Powered by Groq**")
    st.caption("AI-powered interview preparation")

# Introduction
st.write("Practice interviews, improve your skills, and track your progress.")

# Feature cards
features = [
    ("🧠", "Resume Analysis"),
    ("📝", "MCQ Interviews"),
    ("💬", "Descriptive Interviews"),
    ("💻", "Coding Interviews"),
    ("✅", "AI Evaluation"),
    ("📈", "Progress Dashboard"),
]

cols = st.columns(3)

for i, (emoji, label) in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="card">
                <div style="font-size:32px;">{emoji}</div>
                <div style="font-weight:600;margin-top:10px;color:white;">
                    {label}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

# Resume upload
st.subheader("📄 Upload Resume")

resume = st.file_uploader(
    "Upload your Resume (PDF/DOCX)",
    type=["pdf", "docx"],
    key="resume_uploader"
)

if resume is not None:
    st.success("Resume uploaded successfully!")

    file_signature = (resume.name, resume.size)

    if st.session_state.get("resume_signature") != file_signature:
        st.session_state.pop("resume_analysis", None)
        st.session_state["resume_signature"] = file_signature

    if "resume_analysis" not in st.session_state:
        if st.button("🔍 Analyze My Resume", type="primary"):
            with st.spinner("Analyzing your resume with AI..."):
                try:
                    resume_text = extract_text(resume)

                    if not resume_text or not resume_text.strip():
                        st.error(
                            "No readable text found. Please upload "
                            "a text-based PDF or DOCX file."
                        )
                    else:
                        result = analyze_resume(resume_text)

                        if result:
                            st.session_state["resume_analysis"] = result
                            st.rerun()
                        else:
                            st.warning(
                                "The AI returned an empty result. "
                                "Please try again."
                            )

                except GroqCallError as e:
                    st.error(f"Resume analysis failed: {e}")

                except Exception as e:
                    st.error(
                        "An unexpected error occurred. "
                        "Please check the Streamlit app logs."
                    )
                    print(f"Resume analysis error: {e}")

    if "resume_analysis" in st.session_state:
        st.subheader("📊 AI Resume Analysis")
        st.markdown(st.session_state["resume_analysis"])

        if st.button("🔄 Analyze Another Resume"):
            st.session_state.pop("resume_analysis", None)
            st.session_state.pop("resume_signature", None)
            st.rerun()

st.divider()
st.info("Use the sidebar to navigate to the interview pages.")
