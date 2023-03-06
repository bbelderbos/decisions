import requests
import streamlit as st
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)

API_URL = (
    "http://localhost:8000/decisions/" if DEBUG else "http://myapi:8000/decisions/"
)

st.markdown("# Add A New Decision")
decision_id = st.text_input("Decision ID")
date = st.date_input("Decision Date")
date_review = st.date_input("Review Date")
status = st.selectbox("Decision Status", ["Open", "Made", "Reviewed"])

reflection = st.text_area("Review - What happened and what I learned")
rating = st.slider("Review: How do you rate the decision?", 0, 10, 5)

if st.button("Submit"):
    st.write("Congrats on reviewing a decision!")
    data = {
        "time_made": str(date),
        "time_reviewed": str(date_review),
        "status": status,
        "review": reflection,
        "rating": rating,
    }
    decision_url = API_URL + decision_id + "/"
    response = requests.put(decision_url, json=data)
    st.write(response.status_code)
    st.write(response.json())
