import pandas as pd
import streamlit as st

from database import PREVISION_COLUMNS, get_current_week, init_data, upsert_previsions

init_data()

st.title("🗓️ Saisie Prévisions (Créneau Horaire)")

current_week = get_current_week()
default_s = current_week + 1

colw1, colw2 = st.columns(2)
semaine_s = colw1.number_input("Semaine S", min_value=1, max_value=53, value=default_s, step=1)
semaine_sp1 = colw2.number_input("Semaine S+1", min_value=1, max_value=53, value=default_s + 1, step=1)

region = st.selectbox("Région assistante", sorted(st.session_state.clients_ref["Région"].unique()))

clients_region = st.session_state.clients_ref[st.session_state.clients_ref["Région"] == region].copy()

existing = st.session_state.previsions
existing_week = existing[(existing["Semaine"] == int(semaine_s)) & (existing["Région"] == region)]

base = clients_region.merge(
    existing_week[
        [
            "Code client",
            "Date de prise de Commande S",
            "MT Commande prévue S",
            "Date de prise de Commande S+1",
            "MT Commande prévue S+1",
        ]
    ],
    on="Code client",
    how="left",
)

for col in [
    "Date de prise de Commande S",
    "Date de prise de Commande S+1",
]:
    base[col] = pd.to_datetime(base[col], errors="coerce")

for col in ["MT Commande prévue S", "MT Commande prévue S+1"]:
    base[col] = pd.to_numeric(base[col], errors="coerce").fillna(0)

st.caption("Renseignez uniquement les clients prévus pour la semaine S et S+1.")
edited = st.data_editor(
    base,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Date de prise de Commande S": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "Date de prise de Commande S+1": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "MT Commande prévue S": st.column_config.NumberColumn(min_value=0, step=1000),
        "MT Commande prévue S+1": st.column_config.NumberColumn(min_value=0, step=1000),
    },
)

if st.button("💾 Enregistrer les prévisions"):
    to_save = edited.copy()
    to_save["Semaine"] = int(semaine_s)

    ordered = to_save[
        [
            "Semaine",
            "Code client",
            "Raison Sociale",
            "Région",
            "Portefeuille",
            "Wilaya",
            "Date de prise de Commande S",
            "MT Commande prévue S",
            "Date de prise de Commande S+1",
            "MT Commande prévue S+1",
        ]
    ]

    filtered = ordered[
        (ordered["MT Commande prévue S"] > 0)
        | (ordered["MT Commande prévue S+1"] > 0)
        | (ordered["Date de prise de Commande S"].notna())
        | (ordered["Date de prise de Commande S+1"].notna())
    ].copy()

    filtered["Semaine"] = filtered["Semaine"].astype(int)
    upsert_previsions(filtered[PREVISION_COLUMNS])
    st.success(
        f"Prévisions enregistrées pour la région {region} | S={int(semaine_s)} et S+1={int(semaine_sp1)}"
    )
