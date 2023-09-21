import streamlit as st
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/ControleNiveau1.py","Contrôle 1er niveau")
])

update = True

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_all_file(update):
    df_moy = pd.read_csv('sortie_moy.csv')
    return df_moy

df_moy = load_all_file(update) 

df_moy = df_moy.loc[:, ~df_moy.columns.str.contains('^Unnamed')]

PosTarif = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    df_moy['Produit'].unique())




