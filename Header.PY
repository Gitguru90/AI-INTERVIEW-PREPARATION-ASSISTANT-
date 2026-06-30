import base64
from pathlib import Path
import streamlit as st

LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo.png"


@st.cache_data
def _get_logo_base64() -> str | None:
    if not LOGO_PATH.exists():
        return None
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_header(name: str = "Kiran Tomar"):
    """Renders a logo + name badge, right-aligned at the top of the page content.

    Uses normal document flow (st.columns) instead of CSS position:fixed, since
    fixed overlays get covered by Streamlit's own toolbar (hamburger menu /
    Deploy button) which sits at a higher stacking layer in that same corner.
    """
    logo_b64 = _get_logo_base64()

    spacer, badge_col = st.columns([5, 1])
    with badge_col:
        if logo_b64:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; justify-content:flex-end; gap:8px;">
                    <img src="data:image/png;base64,{logo_b64}"
                         style="width:32px; height:32px; border-radius:50%; object-fit:cover;" />
                    <span style="color:rgba(255,255,255,0.85); font-weight:600; font-size:14px; white-space:nowrap;">
                        {name}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Visible fallback so a missing/misnamed file is obvious instead of
            # silently rendering nothing.
            st.markdown(
                f"""
                <div style="text-align:right; color:rgba(255,165,0,0.9); font-size:12px;">
                    ⚠️ Logo not found at assets/logo.png<br/>{name}
                </div>
                """,
                unsafe_allow_html=True,
            )
