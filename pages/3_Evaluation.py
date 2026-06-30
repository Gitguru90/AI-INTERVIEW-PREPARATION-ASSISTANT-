import streamlit as st
import re
from utils.groq_ai import evaluate_interview, generate_roadmap, GroqCallError
from utils.header import render_header
from db import create_table, save_interview

create_table()

st.set_page_config(page_title="Evaluation", page_icon="📊")

render_header()

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Interview Evaluation")
st.markdown("⚡ Powered by **Groq**")

questions = st.session_state.get("interview_questions", st.session_state.get("generated_questions", ""))
answers = st.session_state.get("interview_answers", st.session_state.get("answers", {}))
role = st.session_state.get("role", "SDE Intern")

if not questions:
    st.warning("No interview data found. Please complete an interview first.")
    st.stop()

if "evaluation_report" not in st.session_state:
    with st.spinner("⚡ Evaluating with Groq AI..."):
        try:
            evaluation = evaluate_interview(role, questions, answers)
            roadmap = generate_roadmap(evaluation)
            st.session_state.evaluation_report = evaluation
            st.session_state.roadmap = roadmap
        except GroqCallError as e:
            st.error(f"Evaluation failed: {e}")
            if st.button("🔄 Retry"):
                st.rerun()
            st.stop()

evaluation = st.session_state.evaluation_report

st.subheader("📋 Evaluation Report")
st.markdown(evaluation)

score = 0.0
match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', evaluation)
if match:
    score = float(match.group(1))
else:
    st.caption("⚠️ Couldn't extract a numeric score from the report — defaulting to 0/10 for dashboard tracking.")

if score >= 7:
    st.balloons()
elif score >= 4:
    st.snow()

save_interview(role, score, evaluation)

if st.button("📈 View Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
