from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# Works locally (.env) AND on Streamlit Cloud (st.secrets)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

genai.configure(api_key=api_key)

# Disabling "thinking" removes Gemini 2.5 Flash's internal reasoning
# step before it starts answering — the single biggest speed win here,
# since we just need formatted output, not deep reasoning.
# Note: thinking_config support depends on your installed SDK version.
# If this raises an error on your machine, run:
#   pip install -U google-generativeai
# NOTE: thinking_config / ThinkingConfig is not supported by your
# currently installed google-generativeai version, so it's omitted here.
# If you upgrade with: pip install -U google-generativeai
# you can re-add thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
# to GenerationConfig below for an extra speed boost.
GENERATION_CONFIG = genai.types.GenerationConfig(
    max_output_tokens=2048,
)

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config=GENERATION_CONFIG,
)


def ask_gemini(prompt, max_output_tokens=2048):
    try:
        config = GENERATION_CONFIG
        if max_output_tokens != 2048:
            config = genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
            )

        response = model.generate_content(
            prompt,
            generation_config=config,
            request_options={"timeout": 60},
        )
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"


def ask_gemini_stream(prompt, max_output_tokens=2048):
    """
    Generator version — yields text chunks as they arrive so the UI
    can render progressively with st.write_stream() instead of
    waiting for the full response.
    """
    try:
        config = GENERATION_CONFIG
        if max_output_tokens != 2048:
            config = genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
            )

        response = model.generate_content(
            prompt,
            generation_config=config,
            stream=True,
            request_options={"timeout": 60},
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Gemini Error: {str(e)}"


def analyze_resume(resume_text):

    # Trim very long resumes — sending fewer input tokens speeds up
    # the call noticeably and rarely loses anything useful.
    trimmed_text = resume_text[:6000]

    prompt = f"""
You are a resume reviewer. Be extremely concise.

Respond ONLY in short bullet points, max 8 words per bullet, no paragraphs.
Use exactly this structure:

Resume Score: x/100

Strengths:
- (max 3 bullets)

Weak Areas:
- (max 3 bullets)

Missing Skills:
- (max 3 bullets)

Improvement Suggestions:
- (max 3 bullets)

Resume:
{trimmed_text}
"""

    return ask_gemini(prompt, max_output_tokens=1024)