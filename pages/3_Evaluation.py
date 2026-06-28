import streamlit as st
import re
from utils.groq_ai import ask_groq
from db import create_table, save_interview

create_table()

st.set_page_config(page_title="Evaluation", page_icon="📊")

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 18px rgba(236,72,153,0.6); }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Interview Evaluation")
st.markdown("⚡ Powered by **Groq + Llama 3**")

questions = st.session_state.get("generated_questions", [])
answers = st.session_state.get("answers", {})
role = st.session_state.get("role", "SDE Intern")

if "evaluation_report" not in st.session_state:
    with st.spinner("⚡ Evaluating your interview with Groq AI..."):

        evaluation_prompt = f"""
You are a strict, no-fluff interview evaluator.
Role: {role}
Questions:
{questions}
Answers:
{answers}
Respond in SHORT bullet points only. No long paragraphs, no repetition,
no filler sentences. Max 1 line per bullet. Use this exact structure:

Overall Score: x/10
Technical Accuracy: <one short line>
Communication: <one short line>
Problem Solving: <one short line>
Strengths:
- <max 3 bullets, each under 12 words>
Weaknesses:
- <max 3 bullets, each under 12 words>
Mentor Note: <one short sentence, max 15 words>
"""
        evaluation = ask_groq(evaluation_prompt, max_tokens=600)

        roadmap_prompt = f"""
Based on this interview evaluation:
{evaluation}
Respond in SHORT bullet points only. No paragraphs. Use this exact structure:

Best Topic: <one short line>
Weak Topic: <one short line>
Skills To Improve:
- <max 3 bullets, each under 10 words>
Recommended Projects:
- <max 2 bullets, each under 12 words>
30-Day Plan:
- Week 1: <under 10 words>
- Week 2: <under 10 words>
- Week 3: <under 10 words>
- Week 4: <under 10 words>
"""
        roadmap = ask_groq(roadmap_prompt, max_tokens=400)

        st.session_state.evaluation_report = evaluation
        st.session_state.roadmap = roadmap

evaluation = st.session_state.evaluation_report

st.subheader("📋 Evaluation Report")
st.markdown(evaluation)

score = 0
match = re.search(r'(\d+(\.\d+)?)\s*/\s*10', evaluation)
if match:
    score = float(match.group(1))

if score >= 7:
    st.balloons()
elif score >= 4:
    st.snow()

save_interview(role, score, evaluation)

if st.button("📈 View Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
