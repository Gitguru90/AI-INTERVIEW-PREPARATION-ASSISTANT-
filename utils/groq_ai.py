import streamlit as st
from groq import Groq

# Groq deprecated mixtral-8x7b-32768. Use a currently supported model.
# Swap to "llama-3.3-70b-versatile" if you want stronger output and don't mind
# slightly slower responses.
MODEL = "llama-3.1-8b-instant"


def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error(
            "GROQ_API_KEY not found. Add it to .streamlit/secrets.toml "
            "(or your deployment's Secrets settings) as:\nGROQ_API_KEY = \"your-key-here\""
        )
        st.stop()
    return Groq(api_key=api_key)


class GroqCallError(Exception):
    """Raised when a Groq call fails, so callers can branch on it explicitly
    instead of accidentally rendering an error string as if it were content."""
    pass


def ask_groq(prompt: str, max_tokens: int = 500, max_chars: int = 4000) -> str:
    client = get_client()
    prompt = prompt[:max_chars]
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        if not content or not content.strip():
            raise GroqCallError("Groq returned an empty response.")
        return content
    except GroqCallError:
        raise
    except Exception as e:
        # Don't swallow this into a string that gets rendered as content.
        raise GroqCallError(str(e)) from e


def analyze_resume(resume_text: str) -> str:
    resume_short = resume_text[:1500]
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
    return ask_groq(prompt, max_tokens=500)


def ask_interview_question_prompt(role, difficulty, mode, num_questions, mode_instructions):
    prompt = f"""You are a technical interviewer.
Role: {role}, Difficulty: {difficulty}, Mode: {mode}
{mode_instructions}
Return ONLY the questions in the exact format. No commentary, no preamble, no markdown headers."""
    return ask_groq(prompt, max_tokens=1800)


def evaluate_interview(role, questions, answers):
    prompt = f"""Evaluate this interview for {role}.
Questions: {str(questions)[:800]}
Answers: {str(answers)[:800]}
Reply exactly in this format:
Overall Score: x/10
Technical Accuracy: one line
Communication: one line
Strengths:
- bullet
Weaknesses:
- bullet
Mentor Note: one line"""
    return ask_groq(prompt, max_tokens=500)


def generate_roadmap(evaluation):
    prompt = f"""Based on this evaluation: {evaluation[:800]}
Reply exactly in this format:
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
    return ask_groq(prompt, max_tokens=400)
