import pandas as pd
import requests
import streamlit as st
from utils import get_decision_data

API_URL = "http://localhost:8000/decisions/"

st.markdown("# Executive Summary 📈")
st.sidebar.markdown("# Executive Summary 📈")

col1, col2, col3 = st.columns(3)
col1.metric(label="Crucial decisions made during last 4 weeks", value="4", delta="2")
col2.metric(label="Open crucial decisions", value="2", delta="-1")
col3.metric(
    label="Average duration for crucial decisions", value="10 days", delta="-5 days"
)

df = get_decision_data()


st.markdown("# Decisions")
# st.table(df)


col1, col2 = st.columns([2, 1])
col2.write("#")
button = col2.button("Archive")

decision_name = col1.selectbox(
    "Select a decision", df[df["Archive"] == False]["Decision"]
)

if button:
    if not df.empty:
        id = df[df["Decision"] == decision_name]["ID"].values[0]
        put_url = f"{API_URL}{id}/archive"
        response = requests.put(put_url)
        # st.write(response.status_code)
        # st.write(response.json())

df = get_decision_data()

st.table(
    df[df["Archive"] == False][
        ["Decision", "Decision Date", "Decision Status", "Decision Review Date"]
    ]
)
