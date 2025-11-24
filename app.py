import streamlit as st
from database import init_data

st.set_page_config(page_title="Suivi Paiements Piscine", layout="wide")

init_data()

st.title("🏊 Application de gestion des clubs - Piscine")
st.write("Bienvenue ! Utilisez le menu de gauche pour gérer les paramètres, créer un club, calculer les montants et suivre les paiements.")
