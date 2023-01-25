import streamlit as st

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
