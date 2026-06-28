import streamlit as st
import re

from utils.gemini import ask_gemini
from db import create_table, save_interview

create_table()

st.title("📊 Interview Evaluation")

questions = st.session_state.get(
    "generated_questions",
    []
)

answers = st.session_state.get(
    "answers",
    {}
)

role = st.session_state.get(
    "role",
    "SDE Intern"
)

if "evaluation_report" not in st.session_state:

    with st.spinner("Evaluating Interview..."):

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

        evaluation = ask_gemini(
            evaluation_prompt
        )

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

        roadmap = ask_gemini(
            roadmap_prompt
        )

        st.session_state.evaluation_report = evaluation
        st.session_state.roadmap = roadmap

evaluation = st.session_state.evaluation_report

st.subheader("📋 Evaluation Report")
st.markdown(evaluation)

# Score Extract
score = 0

match = re.search(
    r'(\d+(\.\d+)?)\s*/\s*10',
    evaluation
)

if match:
    score = float(match.group(1))

if score >= 7:
    st.balloons()
elif score >= 4:
    st.snow()

# Save Interview
save_interview(
    role,
    score,
    evaluation
)

if st.button("📈 View Dashboard"):
    st.switch_page(
        "pages/4_Dashboard.py"
    )