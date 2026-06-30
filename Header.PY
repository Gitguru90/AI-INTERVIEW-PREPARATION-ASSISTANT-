import base64
from pathlib import Path
import streamlit as st

LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo.png"


@st.cache_data
def _get_logo_base64() -> str:
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_header(name: str = "Kiran Tomar"):
    """Renders a fixed logo + name badge in the top-right corner of the page."""
    try:
        logo_b64 = _get_logo_base64()
    except FileNotFoundError:
        logo_b64 = None

    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" class="header-logo" />'
        if logo_b64 else ""
    )

    st.markdown(
        f"""
        <style>
        .top-right-badge {{
            position: fixed;
            top: 12px;
            right: 20px;
            z-index: 9999;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 999px;
            padding: 6px 14px 6px 6px;
        }}
        .header-logo {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            object-fit: cover;
        }}
        .header-name {{
            color: rgba(255, 255, 255, 0.85);
            font-weight: 600;
            font-size: 14px;
            white-space: nowrap;
        }}
        </style>
        <div class="top-right-badge">
            {logo_html}
            <span class="header-name">{name}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
