import streamlit as st

st.set_page_config(page_title="Choose Interview", page_icon="🎯")
st.title("🎯 Choose Interview")

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

    for key in [
        "generated_questions", "answers", "correct_answers",
        "interview_questions", "interview_answers", "evaluation_report",
        "roadmap", "mcq_score", "questions_generated_for"
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.switch_page("pages/2_Interview.py")
