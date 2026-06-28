import streamlit as st
import anthropic


def get_client():
    """Initialize Anthropic client using Streamlit secrets."""
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("ANTHROPIC_API_KEY not found in Streamlit secrets. Please add it in app settings.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def analyze_resume(resume_text: str) -> str:
    """Analyze resume text using Claude and return formatted markdown."""
    client = get_client()

    prompt = f"""Analyze this resume and return a concise report in markdown format with these sections:

## ✅ Strengths
- List 3–5 key strengths as bullet points

## ⚠️ Areas to Improve
- List 2–4 weaknesses or gaps as bullet points

## 💡 Suggestions
- List 3–5 specific actionable improvements as bullet points

## 🎯 Best Fit Roles
- List 3–4 job roles this candidate is well-suited for

## 📊 Overall Score
Give a score out of 100 with a one-line justification.

Keep each bullet point short (1 sentence max). Be direct and constructive.

Resume:
{resume_text[:3000]}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_questions(role: str, level: str, q_type: str, count: int = 8) -> list[dict]:
    """Generate interview questions for a given role."""
    client = get_client()

    prompt = f"""Generate exactly {count} {q_type} interview questions for a {level} {role} position.
Return as a numbered list. Each line: just the question text, nothing else.
No explanations, no categories, just the questions."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )

    lines = response.content[0].text.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Strip leading number and punctuation
            q = line.split(".", 1)[-1].strip()
            if q:
                questions.append({"question": q})
    return questions


def evaluate_answer(question: str, answer: str, role: str = "") -> str:
    """Score and give feedback on an interview answer."""
    client = get_client()

    prompt = f"""Evaluate this interview answer for a {role or 'professional'} role.

Question: {question}
Answer: {answer}

Return feedback in this exact markdown format:

**Score: X/100**

**What worked well:**
(1-2 sentences)

**What to improve:**
(1-2 sentences)

**Pro tip:**
(1 sentence specific advice)

Be concise and constructive."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def mock_interview_question(role: str, previous_qa: list = None) -> str:
    """Generate a single mock interview question, optionally continuing a conversation."""
    client = get_client()

    context = ""
    if previous_qa:
        context = "\n".join([f"Q: {qa['q']}\nA: {qa['a']}" for qa in previous_qa[-2:]])
        context = f"\nPrevious exchange:\n{context}\nNow ask a follow-up or next question."

    prompt = f"""You are interviewing a candidate for a {role} position.
Ask ONE challenging but fair interview question.{context}
Return only the question text, nothing else."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()
