import requests
import streamlit as st

API_URL = "http://localhost:8000/decisions/"

st.markdown("# Add A New Decision")

name = st.text_input("Decision Name")

state_emotional = st.multiselect(
    "Emotional State", ["Happy", "Sad", "Neutral", "Calm", "Anxious"]
)


situation = st.text_area("Situation / Context")
problem = st.text_area("The problem statement or frame")
variables = st.text_area("The variables that govern the situation include")
complications = st.text_area("The complications/complexities as I see them")
alternatives = st.text_area(
    "Alternatives that were seriously considered and not chosen were"
)
outcomes = st.text_area("Explain the range of outcomes")
predictions = st.text_area("What I expect to happen with actual probabilities")
result = st.text_area("Outcome")

if st.button("Submit"):
    st.write("Congrats on making a decision!")
    data = {
        "name": str(name),
        "state_emotional": str(state_emotional),
        "situation": str(situation),
        "problem_statement": str(problem),
        "variables": str(variables),
        "complications": str(complications),
        "alternatives": str(alternatives),
        "outcome_ranges": str(outcomes),
        "expected_with_probabilities": str(predictions),
        "outcome": str(result),
    }

    response = requests.post(API_URL, json=data)
    st.write(response.status_code)
    st.write(response.json())
