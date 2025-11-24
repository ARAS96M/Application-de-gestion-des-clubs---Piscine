import streamlit as st
from database import init_data

init_data()

st.title("🏊‍♂️ Création d’un club")

nom = st.text_input("Nom du club")

jours = st.multiselect("Jours d’utilisation :", ["Dimanche", "Mardi", "Jeudi"])

details = {}

for j in jours:
    st.subheader(j)
    type_util = st.radio(f"Type d’utilisation – {j}", ["PB", "Couloir"], key=j+"type")

    if type_util == "PB":
        details[j] = {"type": "PB", "couloirs": 0}

    if type_util == "Couloir":
        nb = st.number_input(f"Nombre de couloirs ({j})", min_value=1, value=1)
        details[j] = {"type": "Couloir", "couloirs": nb}

if st.button("Créer le club"):
    st.session_state.clubs.append({
        "nom": nom,
        "jours": details
    })
    st.success("Club créé avec succès !")
