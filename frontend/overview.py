import pandas as pd
import streamlit as st

API_URL = "http://localhost:8000/decisions/"

st.markdown("# Executive Summary 📈")
st.sidebar.markdown("# Executive Summary 📈")

col1, col2, col3 = st.columns(3)
col1.metric(label="Crucial decisions made during last 4 weeks", value="4", delta="2")
col2.metric(label="Open crucial decisions", value="2", delta="-1")
col3.metric(
    label="Average duration for crucial decisions", value="10 days", delta="-5 days"
)

df = pd.DataFrame(
    {
        "Decision": ["Lunch", "Decision 2", "Decision 3", "Decision 4"],
        "Decision Date": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04"],
        "Decision Status": ["Open", "Open", "Closed", "Closed"],
        "Decision Review Date": [
            "2021-03-01",
            "2021-03-02",
            "2021-03-03",
            "2021-03-04",
        ],
    }
)

st.markdown("# Decisions")
st.table(df)
