import streamlit as st
from database import init_data

init_data()
st.title("📌 Paramètres – Base de données")

st.subheader("Saisir / Modifier les tarifs")

st.session_state.tarifs["PB"] = st.number_input("Tarif Piscine Libre (PB)", value=st.session_state.tarifs["PB"])
st.session_state.tarifs["couloir"] = st.number_input("Tarif par couloir", value=st.session_state.tarifs["couloir"])
st.session_state.tarifs["frais_fixes"] = st.number_input("Frais fixes par club", value=st.session_state.tarifs["frais_fixes"])

st.success("Tarifs mis à jour !")
