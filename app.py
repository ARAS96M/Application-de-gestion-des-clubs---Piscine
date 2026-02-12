import streamlit as st
from database import init_data, get_current_week

st.set_page_config(page_title="Créneau Horaire - Expédition", layout="wide")

init_data()

current_week = get_current_week()
next_week = current_week + 1

st.title("📦 Créneau Horaire - Programme Expédition")
st.markdown(
    """
Cette application permet de :
- préparer les **prévisions hebdomadaires** (S et S+1) par client,
- suivre les **commandes réellement prises** pendant la semaine,
- comparer automatiquement le **prévu vs réalisé**,
- piloter la performance par **région** et **portefeuille**.
"""
)

col1, col2, col3 = st.columns(3)
col1.metric("Semaine actuelle", current_week)
col2.metric("Semaine de planification (S)", next_week)
col3.metric("Semaine de planification (S+1)", next_week + 1)

st.info("Utilisez les pages du menu à gauche : 1) Paramètres, 2) Saisie Prévisions, 3) Suivi Réalisé, 4) Tableau de bord.")
