import streamlit as st

st.set_page_config(page_title="Choose Interview", page_icon="🎯")

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 18px rgba(236,72,153,0.6); }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 Choose Interview")
st.markdown("⚡ Powered by **Groq + Llama 3** — responses in ~1 second")
st.divider()

role = st.selectbox("Select Role", [
    "SDE Intern", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "Python Developer", "AI Engineer",
    "Machine Learning Engineer", "Data Analyst", "Data Scientist",
    "Cybersecurity Analyst"
])
mode = st.radio("Interview Mode", ["MCQ", "Descriptive", "Coding", "Mixed"])
difficulty = st.radio("Difficulty", ["Easy", "Medium", "Hard"])
duration = st.selectbox("Duration", ["15 min", "30 min", "60 min"])

st.divider()

if st.button("🚀 Start Interview"):
    st.session_state.role = role
    st.session_state.mode = mode
    st.session_state.difficulty = difficulty
    st.session_state.duration = duration

    # Clear out any leftover state from a previous interview attempt so the
    # next page doesn't show stale questions/answers/scores.
    for key in [
        "generated_questions", "answers", "correct_answers",
        "interview_questions", "interview_answers", "evaluation_report",
        "roadmap", "mcq_score", "questions_generated_for",
        "question_generation_error",
    ]:
        st.session_state.pop(key, None)

    st.switch_page("pages/2_Interview.py")
