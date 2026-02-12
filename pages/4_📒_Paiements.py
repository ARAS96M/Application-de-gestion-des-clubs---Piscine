import pandas as pd
import streamlit as st

from database import get_current_week, init_data

init_data()

st.title("📊 Tableau de bord prévisionnel vs réalisé")

selected_week = st.number_input(
    "Semaine dashboard", min_value=1, max_value=53, value=get_current_week(), step=1
)

previsions = st.session_state.previsions
actuals = st.session_state.commandes_reelles

week_prev = previsions[previsions["Semaine"] == int(selected_week)].copy()
week_real = actuals[actuals["Semaine"] == int(selected_week)].copy()

if week_prev.empty:
    st.info("Pas de prévisions pour cette semaine.")
    st.stop()

prev_clients = (
    week_prev.groupby(["Région", "Portefeuille"], as_index=False)
    .agg(nb_prevus=("Code client", "nunique"), mt_prevu=("MT Commande prévue S", "sum"))
)

real_clients = (
    week_real.groupby(["Région", "Portefeuille"], as_index=False)
    .agg(nb_realises=("Code client", "nunique"), mt_realise=("Montant réalisé", "sum"))
)

summary = prev_clients.merge(real_clients, on=["Région", "Portefeuille"], how="left")
summary[["nb_realises", "mt_realise"]] = summary[["nb_realises", "mt_realise"]].fillna(0)
summary["taux_clients_%"] = (
    (summary["nb_realises"] / summary["nb_prevus"].replace(0, pd.NA)) * 100
).round(1).fillna(0)
summary["taux_mt_%"] = (
    (summary["mt_realise"] / summary["mt_prevu"].replace(0, pd.NA)) * 100
).round(1).fillna(0)

k1, k2, k3 = st.columns(3)
k1.metric("Total prévu semaine", f"{summary['mt_prevu'].sum():,.0f}".replace(",", " "))
k2.metric("Total réalisé semaine", f"{summary['mt_realise'].sum():,.0f}".replace(",", " "))

global_rate = 0
if summary["mt_prevu"].sum() > 0:
    global_rate = (summary["mt_realise"].sum() / summary["mt_prevu"].sum()) * 100
k3.metric("Taux global", f"{global_rate:.1f}%")

st.subheader("Détail par région / portefeuille")
st.dataframe(summary.sort_values(["Région", "Portefeuille"]), use_container_width=True)

region_view = summary.groupby("Région", as_index=False).agg(
    mt_prevu=("mt_prevu", "sum"),
    mt_realise=("mt_realise", "sum"),
    nb_prevus=("nb_prevus", "sum"),
    nb_realises=("nb_realises", "sum"),
)
region_view["taux_mt_%"] = (
    (region_view["mt_realise"] / region_view["mt_prevu"].replace(0, pd.NA)) * 100
).round(1).fillna(0)

st.subheader("Synthèse régionale")
st.dataframe(region_view, use_container_width=True)
