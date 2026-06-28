import streamlit as st
from groq import Groq


def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it in app settings.")
        st.stop()
    return Groq(api_key=api_key)


def ask_groq(prompt: str, max_tokens: int = 1000) -> str:
    """General-purpose Groq call — used by all pages."""
    client = get_client()
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def analyze_resume(resume_text: str) -> str:
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
    return ask_groq(prompt, max_tokens=800)


def generate_questions(role: str, level: str, q_type: str, count: int = 8) -> list:
    prompt = f"""Generate exactly {count} {q_type} interview questions for a {level} {role} position.
Return as a numbered list. Each line: just the question text, nothing else.
No explanations, no categories, just the questions."""
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
    return ask_groq(prompt, max_tokens=400)


def mock_interview_question(role: str, previous_qa: list = None) -> str:
    context = ""
    if previous_qa:
        context = "\n".join([f"Q: {qa['q']}\nA: {qa['a']}" for qa in previous_qa[-2:]])
        context = f"\nPrevious exchange:\n{context}\nNow ask a follow-up or next question."
    prompt = f"""You are interviewing a candidate for a {role} position.
Ask ONE challenging but fair interview question.{context}
Return only the question text, nothing else."""
    return ask_groq(prompt, max_tokens=150).strip()
