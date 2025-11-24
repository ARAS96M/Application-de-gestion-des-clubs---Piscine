import streamlit as st
import pandas as pd
from database import init_data

init_data()

st.title("💰 Calcul des montants total par club")

data = []

for club in st.session_state.clubs:
    total = 0

    for jour, info in club["jours"].items():
        if info["type"] == "PB":
            total += st.session_state.tarifs["PB"]
        else:
            total += info["couloirs"] * st.session_state.tarifs["couloir"]

    total += st.session_state.tarifs["frais_fixes"]

    data.append({
        "Club": club["nom"],
        "Total à payer": total
    })

df = pd.DataFrame(data)
st.dataframe(df)
