import pandas as pd
import streamlit as st

from database import init_data, normalize_client_dataframe

init_data()

st.title("📌 Paramètres - Référentiel clients")
st.caption("Chargez la liste fixe clients depuis une extraction SQL (CSV/Excel exporté en CSV).")

with st.expander("Format attendu"):
    st.write("Colonnes obligatoires : Code client, Raison Sociale, Région, Portefeuille, Wilaya")

uploaded = st.file_uploader("Importer un fichier clients (.csv)", type=["csv"])

if uploaded is not None:
    try:
        imported_df = pd.read_csv(uploaded)
        clean_df = normalize_client_dataframe(imported_df)
        st.session_state.clients_ref = clean_df
        st.success(f"{len(clean_df)} clients importés avec succès.")
    except Exception as exc:
        st.error(f"Erreur d'import : {exc}")

st.subheader("Référentiel actuel")
region_filter = st.multiselect(
    "Filtrer les régions", options=sorted(st.session_state.clients_ref["Région"].unique())
)

df_view = st.session_state.clients_ref.copy()
if region_filter:
    df_view = df_view[df_view["Région"].isin(region_filter)]

st.dataframe(df_view, use_container_width=True)

st.download_button(
    "Télécharger le référentiel (CSV)",
    data=st.session_state.clients_ref.to_csv(index=False).encode("utf-8"),
    file_name="clients_referentiel.csv",
    mime="text/csv",
)
