import streamlit as st
from utils.groq_ai import ask_interview_question_prompt, GroqCallError
from utils.header import render_header

st.set_page_config(page_title="Interview Round", page_icon="🎤")

render_header()

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🎤 AI Interview")
st.markdown("⚡ Powered by **Groq**")

if "role" not in st.session_state:
    st.warning("Please start interview from Choose Interview page.")
    st.stop()

role = st.session_state["role"]
mode = st.session_state["mode"]
difficulty = st.session_state["difficulty"]

if "duration" not in st.session_state:
    st.warning("Please select interview duration from Choose Interview page.")
    st.stop()

duration = st.session_state["duration"]

DURATION_QUESTION_MAP = {15: 5, 30: 10, 60: 15}  # reduced counts for token limits


def _parse_duration_minutes(value):
    if isinstance(value, (int, float)):
        return int(value)
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return int(digits) if digits else 15


duration_minutes = _parse_duration_minutes(duration)
num_questions = DURATION_QUESTION_MAP.get(duration_minutes, 5)

current_signature = (role, mode, difficulty, duration_minutes)

if (
    "generated_questions" not in st.session_state
    or st.session_state.get("questions_generated_for") != current_signature
):
    if mode == "MCQ":
        mode_instructions = f"""Generate exactly {num_questions} MCQs.
Format:
QUESTION: ...
A) ...
B) ...
C) ...
D) ...
ANSWER: A"""

    elif mode == "Descriptive":
        mode_instructions = f"""Generate exactly {num_questions} descriptive questions.
Format:
QUESTION: ..."""

    elif mode == "Coding":
        mode_instructions = f"""Generate exactly {num_questions} coding questions.
Format:
CODING: ..."""

    elif mode == "Mixed":
        num_mcq = max(1, num_questions // 3)
        num_desc = max(1, num_questions // 3)
        num_coding = max(1, num_questions - num_mcq - num_desc)
        mode_instructions = f"""Generate {num_mcq} MCQs, {num_desc} descriptive, {num_coding} coding questions.
MCQ format:
QUESTION: ...
A) ... B) ... C) ... D) ...
ANSWER: A
Descriptive: QUESTION: ...
Coding: CODING: ..."""
    else:
        mode_instructions = f"Generate {num_questions} questions."

    with st.spinner("⚡ Generating questions with Groq..."):
        try:
            st.session_state.generated_questions = ask_interview_question_prompt(
                role, difficulty, mode, num_questions, mode_instructions
            )
            st.session_state.questions_generated_for = current_signature
            st.session_state.answers = {}
            st.session_state.correct_answers = {}
            st.session_state.pop("question_generation_error", None)
        except GroqCallError as e:
            st.session_state["question_generation_error"] = str(e)

if st.session_state.get("question_generation_error"):
    st.error(f"Couldn't generate questions: {st.session_state['question_generation_error']}")
    if st.button("🔄 Retry"):
        st.session_state.pop("question_generation_error", None)
        st.session_state.pop("questions_generated_for", None)
        st.rerun()
    st.stop()

questions_text = st.session_state.get("generated_questions", "")

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = {}

st.write(f"### {role} | {mode} | {difficulty}")
st.write(f"### Duration: {duration_minutes} min | Questions: {num_questions}")
st.divider()

any_rendered = False

if mode == "MCQ":
    blocks = questions_text.split("QUESTION:")
    q_no = 1
    for block in blocks[1:]:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        question = lines[0]
        options = []
        answer_key = ""
        for line in lines[1:]:
            if line.startswith(("A)", "B)", "C)", "D)")):
                options.append(line)
            elif line.startswith("ANSWER:"):
                answer_key = line.replace("ANSWER:", "").strip()
        st.subheader(f"Question {q_no}")
        if options:
            selected = st.radio(question, options, key=f"mcq_{q_no}")
            st.session_state.answers[q_no] = selected
            st.session_state.correct_answers[q_no] = answer_key
            any_rendered = True
        else:
            st.write(question)
        st.divider()
        q_no += 1

elif mode == "Descriptive":
    questions = [
        line.replace("QUESTION:", "").strip()
        for line in questions_text.split("\n")
        if "QUESTION:" in line
    ]
    for i, q in enumerate(questions, start=1):
        st.subheader(f"Question {i}")
        st.write(q)
        answer = st.text_area("Your Answer", key=f"desc_{i}")
        st.session_state.answers[i] = answer
        st.divider()
        any_rendered = True

elif mode == "Coding":
    questions = [
        line.replace("CODING:", "").strip()
        for line in questions_text.split("\n")
        if line.strip().startswith("CODING:")
    ]
    for i, q in enumerate(questions, start=1):
        st.subheader(f"Coding Problem {i}")
        st.write(q)
        code = st.text_area("Write Your Code", height=200, key=f"code_{i}")
        st.session_state.answers[i] = code
        st.divider()
        any_rendered = True

elif mode == "Mixed":
    lines = [line.strip() for line in questions_text.split("\n") if line.strip()]
    q_no = 1
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("QUESTION:"):
            question = line.replace("QUESTION:", "").strip()
            options = []
            answer_key = ""
            j = i + 1
            while j < len(lines):
                if lines[j].startswith(("A)", "B)", "C)", "D)")):
                    options.append(lines[j])
                    j += 1
                elif lines[j].startswith("ANSWER:"):
                    answer_key = lines[j].replace("ANSWER:", "").strip()
                    j += 1
                    break
                else:
                    break
            if len(options) == 4:
                st.subheader(f"MCQ {q_no}")
                selected = st.radio(question, options, key=f"mixed_mcq_{q_no}")
                st.session_state.answers[q_no] = selected
                st.session_state.correct_answers[q_no] = answer_key
            else:
                st.subheader(f"Question {q_no}")
                answer = st.text_area(question, key=f"mixed_desc_{q_no}")
                st.session_state.answers[q_no] = answer
            st.divider()
            any_rendered = True
            q_no += 1
            i = j
        elif line.startswith("CODING:"):
            problem = line.replace("CODING:", "").strip()
            st.subheader(f"Coding Challenge {q_no}")
            code = st.text_area(problem, height=200, key=f"mixed_code_{q_no}")
            st.session_state.answers[q_no] = code
            st.divider()
            any_rendered = True
            q_no += 1
            i += 1
        else:
            i += 1

# If parsing failed to find any well-formed question (e.g. the model didn't
# follow the format), show the raw output instead of a blank page.
if not any_rendered:
    st.error("Couldn't parse the generated questions into the expected format. Raw output below:")
    st.code(questions_text or "(empty)")
    if st.button("🔄 Regenerate Questions"):
        st.session_state.pop("questions_generated_for", None)
        st.rerun()
    st.stop()

if st.button("✅ Submit Interview"):
    if mode in ["MCQ", "Mixed"]:
        score = 0
        total = len(st.session_state.correct_answers)
        for key in st.session_state.correct_answers:
            user = st.session_state.answers.get(key, "")
            correct = st.session_state.correct_answers[key]
            if str(user).startswith(correct):
                score += 1
        percentage = round((score / total) * 100, 2) if total > 0 else 0
        st.session_state.mcq_score = percentage
    st.session_state.interview_questions = questions_text
    st.session_state.interview_answers = dict(st.session_state.answers)
    st.switch_page("pages/3_Evaluation.py")
