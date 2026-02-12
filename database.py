import datetime as dt
import pandas as pd
import streamlit as st

PREVISION_COLUMNS = [
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

ACTUAL_COLUMNS = [
    "Date commande",
    "Semaine",
    "Code client",
    "Raison Sociale",
    "Région",
    "Portefeuille",
    "Wilaya",
    "Montant réalisé",
]


def get_current_week() -> int:
    return dt.date.today().isocalendar().week


def _default_clients() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["C0001", "AIDI ET COMPAGNIE SNC", "DRC", "DRC5", "Alger"],
            ["C0002", "TOUATI MOHAMED", "DRC", "DRC2", "Blida"],
            ["C0003", "KAMEL ZAKARIA YOUCEF", "DRE", "DRE4", "Constantine"],
            ["C0004", "LAIBI HAMZA", "DRE", "DRE3", "Sétif"],
            ["C0005", "LEADER PEINTURE ORAN", "DRO", "DRO1", "Oran"],
            ["C0006", "EL SAWEB QUINCAILLERIE", "DRO", "DRO4", "Tlemcen"],
        ],
        columns=["Code client", "Raison Sociale", "Région", "Portefeuille", "Wilaya"],
    )


def init_data() -> None:
    if "clients_ref" not in st.session_state:
        st.session_state.clients_ref = _default_clients()

    if "previsions" not in st.session_state:
        st.session_state.previsions = pd.DataFrame(columns=PREVISION_COLUMNS)

    if "commandes_reelles" not in st.session_state:
        st.session_state.commandes_reelles = pd.DataFrame(columns=ACTUAL_COLUMNS)


def normalize_client_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    required = ["Code client", "Raison Sociale", "Région", "Portefeuille", "Wilaya"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes: {', '.join(missing)}")

    clean = df[required].copy()
    clean["Code client"] = clean["Code client"].astype(str).str.strip()
    clean = clean.drop_duplicates(subset=["Code client"], keep="last")
    return clean


def upsert_previsions(new_rows: pd.DataFrame) -> None:
    existing = st.session_state.previsions.copy()
    if existing.empty:
        st.session_state.previsions = new_rows
        return

    keys = ["Semaine", "Code client"]
    keep_existing = existing.merge(new_rows[keys], on=keys, how="left", indicator=True)
    keep_existing = keep_existing[keep_existing["_merge"] == "left_only"].drop(columns=["_merge"])

    st.session_state.previsions = pd.concat([keep_existing, new_rows], ignore_index=True)


def append_actual_orders(new_rows: pd.DataFrame) -> None:
    st.session_state.commandes_reelles = pd.concat(
        [st.session_state.commandes_reelles, new_rows], ignore_index=True
    )
