import requests
import streamlit as st
from utils import API_URL, get_decision_data

st.markdown("# Archive")
col1, col2 = st.columns([2, 1])

col2.write("#")

df = get_decision_data()

button = col2.button("Unarchive")

decision_name = col1.selectbox("Select a decision", df[df["Archive"]]["Decision"])

if button:
    if not df.empty:
        id = df[df["Decision"] == decision_name]["ID"].values[0]
        post_url = f"{API_URL}{id}/unarchive"
        response = requests.put(post_url)

        # st.write(response.status_code)
        # st.write(response.json())

df = get_decision_data()
st.table(
    df[df["Archive"]][
        ["Decision", "Decision Date", "Decision Status", "Decision Review Date"]
    ]
)
