import datetime as dt
import pandas as pd
import streamlit as st

from database import ACTUAL_COLUMNS, append_actual_orders, get_current_week, init_data

init_data()

st.title("📥 Suivi des commandes réalisées")

selected_week = st.number_input(
    "Semaine à suivre", min_value=1, max_value=53, value=get_current_week(), step=1
)

st.subheader("Ajouter une commande réalisée")
clients = st.session_state.clients_ref.copy()
selected_client = st.selectbox(
    "Client", options=clients["Code client"], format_func=lambda c: f"{c} - {clients[clients['Code client'] == c]['Raison Sociale'].iloc[0]}"
)

client_row = clients[clients["Code client"] == selected_client].iloc[0]

c1, c2 = st.columns(2)
order_date = c1.date_input("Date commande", value=dt.date.today())
amount = c2.number_input("Montant réalisé", min_value=0.0, step=1000.0)

if st.button("➕ Ajouter la commande"):
    row = pd.DataFrame(
        [
            {
                "Date commande": order_date,
                "Semaine": int(selected_week),
                "Code client": client_row["Code client"],
                "Raison Sociale": client_row["Raison Sociale"],
                "Région": client_row["Région"],
                "Portefeuille": client_row["Portefeuille"],
                "Wilaya": client_row["Wilaya"],
                "Montant réalisé": amount,
            }
        ]
    )
    append_actual_orders(row[ACTUAL_COLUMNS])
    st.success("Commande ajoutée.")

st.divider()
st.subheader("Comparaison prévu vs réalisé")

previsions = st.session_state.previsions
actuals = st.session_state.commandes_reelles

week_prev = previsions[previsions["Semaine"] == int(selected_week)].copy()
week_real = actuals[actuals["Semaine"] == int(selected_week)].copy()

if week_prev.empty:
    st.warning("Aucune prévision disponible pour cette semaine.")
else:
    prev_agg = week_prev.groupby(["Code client", "Raison Sociale", "Région", "Portefeuille"], as_index=False)[
        "MT Commande prévue S"
    ].sum()
    real_agg = week_real.groupby(["Code client"], as_index=False)["Montant réalisé"].sum()

    comp = prev_agg.merge(real_agg, on="Code client", how="left")
    comp["Montant réalisé"] = comp["Montant réalisé"].fillna(0)
    comp["Statut client"] = comp["Montant réalisé"].apply(
        lambda x: "🟢 Prévu commandé" if x > 0 else "🔴 Non prévu/non commandé"
    )
    comp["Taux réalisation %"] = (
        (comp["Montant réalisé"] / comp["MT Commande prévue S"].replace(0, pd.NA)) * 100
    ).round(1).fillna(0)

    st.dataframe(comp, use_container_width=True)

    st.download_button(
        "Télécharger comparaison semaine",
        comp.to_csv(index=False).encode("utf-8"),
        file_name=f"comparaison_semaine_{int(selected_week)}.csv",
        mime="text/csv",
    )
