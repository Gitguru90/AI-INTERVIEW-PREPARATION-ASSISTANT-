import streamlit as st
import pandas as pd
from db import get_all_interviews

st.set_page_config(page_title="Dashboard", page_icon="📈")

st.markdown("""
<style>
.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1e3a8a); background-size: 400% 400%; animation: gradientShift 15s ease infinite; }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
[data-testid="stMetric"] { background: rgba(255,255,255,0.05); border-radius: 14px; padding: 12px; border: 1px solid rgba(99,102,241,0.3); }
.stButton > button { background: linear-gradient(90deg, #6366F1, #EC4899); color: white; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 600; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Performance Dashboard")
st.markdown("⚡ Powered by **Groq**")

rows = get_all_interviews()

if len(rows) == 0:
    st.warning("No interview history found. Complete an interview first!")
    st.stop()

df = pd.DataFrame(rows, columns=["ID", "Role", "Score", "Evaluation"])
df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

interviews_completed = len(df)
average_score = round(df["Score"].mean(), 2)
best_score = round(df["Score"].max(), 2)

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Interviews Completed", interviews_completed)
with col2:
    st.metric("Average Score", f"{average_score}/10")
with col3:
    st.metric("Best Score", f"{best_score}/10")

st.divider()

roadmap = st.session_state.get("roadmap", "Complete an interview first to generate a roadmap.")
st.subheader("🎯 AI Learning Roadmap")
st.write(roadmap)

st.divider()
st.subheader("📊 Performance Trend")
graph_df = pd.DataFrame({
    "Interview": range(1, len(df) + 1),
    "Score": df["Score"]
})
st.line_chart(graph_df.set_index("Interview"))

st.divider()
st.subheader("📋 Interview History")
st.dataframe(df[["Role", "Score"]], use_container_width=True)
