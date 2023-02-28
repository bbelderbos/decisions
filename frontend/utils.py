import pandas as pd
import requests
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)

API_URL = (
    "http://localhost:8000/decisions/" if DEBUG else "http://myapi:8000/decisions/"
)


def get_decision_data():
    resp = requests.get(API_URL)
    data = resp.json()
    if not data:
        df = pd.DataFrame(
            columns=[
                "ID",
                "Decision",
                "Decision Date",
                "Decision Status",
                "Decision Review Date",
                "Archive",
            ]
        )
    else:
        df = pd.DataFrame(
            {
                "ID": [row["id"] for row in data],
                "Decision": [row["name"] for row in data],
                "Decision Date": [row["time_made"] for row in data],
                "Decision Status": [row["status"] for row in data],
                "Decision Review Date": [row["time_reviewed"] for row in data],
                "Archive": [row["archived"] for row in data],
            }
        )
    return df

