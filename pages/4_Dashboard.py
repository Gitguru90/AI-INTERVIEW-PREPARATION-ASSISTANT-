import streamlit as st
import pandas as pd

from db import get_all_interviews

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈"
)

st.title("📈 Performance Dashboard")

rows = get_all_interviews()

if len(rows) == 0:

    st.warning(
        "No interview history found."
    )

    st.stop()

df = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Role",
        "Score",
        "Evaluation"
    ]
)

interviews_completed = len(df)

average_score = round(
    df["Score"].mean(),
    2
)

best_score = round(
    df["Score"].max(),
    2
)

st.divider()

# -------------------------
# METRICS
# -------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Interviews Completed",
        interviews_completed
    )

with col2:
    st.metric(
        "Average Score",
        f"{average_score}/10"
    )

with col3:
    st.metric(
        "Best Score",
        f"{best_score}/10"
    )

st.divider()

# -------------------------
# SAVED ROADMAP
# -------------------------

roadmap = st.session_state.get(
    "roadmap",
    "Complete an interview first to generate a roadmap."
)

st.subheader(
    "🎯 AI Learning Roadmap"
)

st.write(roadmap)

st.divider()

# -------------------------
# PERFORMANCE TREND
# -------------------------

st.subheader(
    "📊 Performance Trend"
)

graph_df = pd.DataFrame({
    "Interview": range(
        1,
        len(df) + 1
    ),
    "Score": df["Score"]
})

st.line_chart(
    graph_df.set_index(
        "Interview"
    )
)

st.divider()

# -------------------------
# INTERVIEW HISTORY
# -------------------------

st.subheader(
    "📋 Interview History"
)

history_df = df[[
    "Role",
    "Score"
]]

st.dataframe(
    history_df,
    use_container_width=True
)

st.divider()

st.success(
    "Dashboard loaded successfully."
)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Interviews",
        interviews_completed
    )

with col2:
    st.metric(
        "Average Score",
        f"{average_score}/10"
    )

with col3:
    st.metric(
        "Best Score",
        f"{best_score}/10"
    )