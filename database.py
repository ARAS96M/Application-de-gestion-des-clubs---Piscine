import streamlit as st
import pandas as pd

def init_data():
    if "tarifs" not in st.session_state:
        st.session_state.tarifs = {
            "PB": 0,
            "couloir": 0,
            "frais_fixes": 0
        }

    if "clubs" not in st.session_state:
        st.session_state.clubs = []

    if "paiements" not in st.session_state:
        st.session_state.paiements = {}
