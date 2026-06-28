import streamlit as st
from utils.groq_ai import ask_groq

st.set_page_config(page_title="Interview Round", page_icon="🎤")

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 18px rgba(236,72,153,0.6); }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🎤 AI Interview")
st.markdown("⚡ Powered by **Groq + Llama 3**")

# -------------------------
# Safety Check
# -------------------------

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

# -------------------------
# Map duration -> question count
# -------------------------

DURATION_QUESTION_MAP = {15: 10, 30: 25, 60: 45}

def _parse_duration_minutes(value):
    if isinstance(value, (int, float)):
        return int(value)
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return int(digits) if digits else 15

duration_minutes = _parse_duration_minutes(duration)
num_questions = DURATION_QUESTION_MAP.get(duration_minutes, 10)

# -------------------------
# Generate Questions Once
# -------------------------

current_signature = (role, mode, difficulty, duration_minutes)

if (
    "generated_questions" not in st.session_state
    or st.session_state.get("questions_generated_for") != current_signature
):
    if mode == "MCQ":
        mode_instructions = f"""
Generate exactly {num_questions} MCQs.

Format (repeat for each question):

QUESTION: ...
A) ...
B) ...
C) ...
D) ...
ANSWER: A
"""
    elif mode == "Descriptive":
        mode_instructions = f"""
Generate exactly {num_questions} descriptive questions.

Format (repeat for each question):

QUESTION: ...
"""
    elif mode == "Coding":
        mode_instructions = f"""
Generate exactly {num_questions} coding questions.

Format (repeat for each question):

CODING: ...
"""
    elif mode == "Mixed":
        num_mcq = max(1, round(num_questions * 0.4))
        num_desc = max(1, round(num_questions * 0.4))
        num_coding = max(1, num_questions - num_mcq - num_desc)
        mode_instructions = f"""
Generate a mixed set of exactly {num_questions} questions total:
- {num_mcq} MCQ questions
- {num_desc} Descriptive questions
- {num_coding} Coding questions

Use this format for MCQs:
QUESTION: ...
A) ...
B) ...
C) ...
D) ...
ANSWER: A

Use this format for Descriptive:
QUESTION: ...

Use this format for Coding:
CODING: ...
"""
    else:
        mode_instructions = f"Generate exactly {num_questions} questions relevant to the role."

    prompt = f"""You are an expert technical interviewer.
Role: {role}
Difficulty: {difficulty}
Mode: {mode}
Total Questions Required: {num_questions}

IMPORTANT:
{mode_instructions}

Return ONLY the questions in the exact format described above.
Do not add any extra commentary, headings, or explanations.
"""

    with st.spinner("⚡ Generating questions with Groq AI..."):
        st.session_state.generated_questions = ask_groq(prompt, max_tokens=2000)
        st.session_state.questions_generated_for = current_signature
        st.session_state.answers = {}
        st.session_state.correct_answers = {}

questions_text = st.session_state.generated_questions

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = {}

st.write(f"### Role: {role}")
st.write(f"### Mode: {mode} | Difficulty: {difficulty}")
st.write(f"### Duration: {duration_minutes} min  |  Questions: {num_questions}")
st.divider()

# ==================================================
# MCQ MODE
# ==================================================

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
        selected = st.radio(question, options, key=f"mcq_{q_no}")
        st.session_state.answers[q_no] = selected
        st.session_state.correct_answers[q_no] = answer_key
        st.divider()
        q_no += 1

# ==================================================
# DESCRIPTIVE MODE
# ==================================================

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

# ==================================================
# CODING MODE
# ==================================================

elif mode == "Coding":
    questions = [
        line.replace("CODING:", "").strip()
        for line in questions_text.split("\n")
        if line.strip().startswith("CODING:")
    ]
    if not questions:
        st.error("No coding questions generated.")
        st.code(questions_text)
    else:
        for i, q in enumerate(questions, start=1):
            st.subheader(f"Coding Problem {i}")
            st.write(q)
            code = st.text_area("Write Your Code", height=250, key=f"code_{i}")
            st.session_state.answers[i] = code
            st.divider()

# ==================================================
# MIXED MODE
# ==================================================

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
            q_no += 1
            i = j
        elif line.startswith("CODING:"):
            problem = line.replace("CODING:", "").strip()
            st.subheader(f"Coding Challenge {q_no}")
            code = st.text_area(problem, height=250, key=f"mixed_code_{q_no}")
            st.session_state.answers[q_no] = code
            st.divider()
            q_no += 1
            i += 1
        else:
            i += 1

# ==================================================
# SUBMIT
# ==================================================

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
