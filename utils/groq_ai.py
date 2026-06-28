import streamlit as st
from groq import Groq


def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it in app settings.")
        st.stop()
    return Groq(api_key=api_key)


def ask_groq(prompt: str, max_tokens: int = 800) -> str:
    """General-purpose Groq call — used by all pages."""
    client = get_client()
    # Trim prompt to stay within Groq's 8192 token context limit
    prompt = prompt[:4000]
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def analyze_resume(resume_text: str) -> str:
    # Trim resume to 1500 chars to avoid token limit
    resume_short = resume_text[:1500]
    prompt = f"""Analyze this resume briefly. Return markdown with these sections:

## ✅ Strengths
- 3 bullet points max

## ⚠️ Areas to Improve
- 2 bullet points max

## 💡 Suggestions
- 3 bullet points max

## 🎯 Best Fit Roles
- 3 roles max

## 📊 Overall Score
Score out of 100 with one line reason.

Keep every bullet under 12 words. Be direct.

Resume:
{resume_short}
"""
    return ask_groq(prompt, max_tokens=500)


def generate_questions(role: str, level: str, q_type: str, count: int = 8) -> list:
    prompt = f"""Generate {count} {q_type} interview questions for a {level} {role}.
Numbered list only. No explanations."""
    response = ask_groq(prompt, max_tokens=600)
    lines = response.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            q = line.split(".", 1)[-1].strip()
            if q:
                questions.append({"question": q})
    return questions


def evaluate_answer(question: str, answer: str, role: str = "") -> str:
    prompt = f"""Evaluate this interview answer for {role or 'a professional'} role.

Question: {question[:300]}
Answer: {answer[:500]}

Reply in this format:
**Score: X/100**
**What worked:** (1 sentence)
**Improve:** (1 sentence)
**Tip:** (1 sentence)"""
    return ask_groq(prompt, max_tokens=300)


def mock_interview_question(role: str, previous_qa: list = None) -> str:
    prompt = f"Ask ONE interview question for a {role} position. Return only the question."
    return ask_groq(prompt, max_tokens=100).strip()
