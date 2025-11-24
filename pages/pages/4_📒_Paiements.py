import streamlit as st
from database import init_data

init_data()

st.title("📒 Suivi des paiements")

for club in st.session_state.clubs:
    nom = club["nom"]
    st.subheader(f"Club : {nom}")

    total = sum([
        st.session_state.tarifs["PB"] if info["type"] == "PB"
        else info["couloirs"] * st.session_state.tarifs["couloir"]
        for info in club["jours"].values()
    ]) + st.session_state.tarifs["frais_fixes"]

    payé = st.session_state.paiements.get(nom, 0)
    reste = total - payé

    st.write(f"💵 Total : **{total} DA**")
    st.write(f"🧾 Payé : **{payé} DA**")
    st.write(f"❗ Reste : **{reste} DA**")

    montant = st.number_input("Ajouter un paiement", min_value=0, key=nom)

    if st.button(f"Enregistrer paiement – {nom}"):
        st.session_state.paiements[nom] = payé + montant
        st.success("Paiement enregistré !")
