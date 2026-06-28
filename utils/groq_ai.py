cat > /home/claude/groq_app/utils/groq_ai.py << 'EOF'
import streamlit as st
from groq import Groq


def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it in app settings.")
        st.stop()
    return Groq(api_key=api_key)


def ask_groq(prompt: str, max_tokens: int = 500) -> str:
    client = get_client()
    # Hard limit: keep prompt under 2000 chars to stay well within token limits
    prompt = prompt[:2000]
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # larger context window than llama3-8b
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return f"Error: {str(e)}"


def analyze_resume(resume_text: str) -> str:
    # Only send first 800 chars of resume
    resume_short = resume_text[:800]
    prompt = f"""Analyze this resume. Reply in markdown:

## Strengths
- (3 bullets max, 10 words each)

## Improve
- (2 bullets max)

## Best Roles
- (3 roles)

## Score
X/100 - one reason.

Resume: {resume_short}"""
    return ask_groq(prompt, max_tokens=400)


def ask_interview_question_prompt(role, difficulty, mode, num_questions, mode_instructions):
    prompt = f"""You are a technical interviewer.
Role: {role}, Difficulty: {difficulty}, Mode: {mode}

{mode_instructions}

Return ONLY the questions in the exact format. No commentary."""
    return ask_groq(prompt[:2000], max_tokens=1500)


def evaluate_interview(role, questions, answers):
    prompt = f"""Evaluate this interview for {role}.
Questions: {str(questions)[:400]}
Answers: {str(answers)[:400]}

Reply exactly:
Overall Score: x/10
Technical Accuracy: one line
Communication: one line
Strengths:
- bullet
Weaknesses:
- bullet
Mentor Note: one line"""
    return ask_groq(prompt, max_tokens=400)


def generate_roadmap(evaluation):
    prompt = f"""Based on: {evaluation[:400]}
Reply exactly:
Best Topic: one line
Weak Topic: one line
Skills To Improve:
- bullet
Recommended Projects:
- bullet
30-Day Plan:
- Week 1: 
- Week 2:
- Week 3:
- Week 4:"""
    return ask_groq(prompt, max_tokens=300)
EOF
