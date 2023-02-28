import pandas as pd
import requests
import streamlit as st
from utils import get_decision_data

API_URL = "http://localhost:8000/decisions/"

st.markdown("# Archived Decisions")
df = get_decision_data()

st.markdown("# Decisions")
st.table(df[df["Archive"] == True])
col1, col2 = st.columns([2, 1])
col2.write("#")
button = col2.button("Unarchive")

decision_name = col1.selectbox(
    "Select a decision", df[df["Archive"] == True]["Decision"]
)
if button:
    if not df.empty:
        id = df[df["Decision"] == decision_name]["ID"].values[0]
        put_url = f"{API_URL}{id}/unarchive"
        response = requests.put(put_url)
        # st.write(response.status_code)
        # st.write(response.json())
