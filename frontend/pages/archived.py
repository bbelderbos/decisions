import pandas as pd
import streamlit as st
from utils import get_decision_data

API_URL = "http://localhost:8000/decisions/"

st.markdown("# Archived Decisions")
df = get_decision_data()

st.markdown("# Decisions")
st.table(df)

