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
    # Chargement des codes SH et libéllés 
    df_code = pd.read_excel("TEC_CEDEAO_SH_2017_LR_TAXES.xlsx")
    return df_moy, df_code

df_moy, df_code = load_all_file(update) 

df_moy  = df_moy.loc[:, ~df_moy.columns.str.contains('^Unnamed')]
df_code = df_code.loc[:, ~df_code.columns.str.contains('^Unnamed')]

PosTarif = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    df_moy['Produit'].unique())

if PosTarif :
    Origin = st.sidebar.selectbox(
        'Choisir la provenance du produit',
        df_moy[df_moy['Produit']==PosTarif]['Origine'].unique())

st.write(f"Quelques statistiques unitaires récentes sur cette position tarifaire de cette origine.")

st.write(df_moy[(df_moy["Produit"] == PosTarif) 
                & (df_moy["Origine"] == Origin)][['Sous_Produit', 'PU_moy', 
                                                  'PU_min', 'PU_max', 'PU_med']])

PdsNet = st.number_input(
    'Renseigner le poids net (kgs)', 0)

ValFOB_moy = df_moy[
    (df_moy["Produit"] == PosTarif) 
    & (df_moy["Origine"] == Origin)]['PU_moy'].iloc[0] * PdsNet

ValFOB_min = df_moy[
    (df_moy["Produit"] == PosTarif) 
    & (df_moy["Origine"] == Origin)]['PU_min'].iloc[0] * PdsNet

ValFOB_max = df_moy[
    (df_moy["Produit"] == PosTarif) 
    & (df_moy["Origine"] == Origin)]['PU_max'].iloc[0] * PdsNet

st.write(f"La valeur FOB doit être d'environ:")
st.subheader(f"**:blue[{ValFOB_moy:,.0f}]** FCFA")

#st.write(f"Elle doit être comprise entre **:blue[{ValFOB_min:,.0f}]** FCFA et **:blue[{ValFOB_max:,.0f}]** FCFA")

PosTarif_code = st.selectbox(
    'Choisir la position tarifaire',
    df_code['CODE_SH'].unique())

st.write(df_code[(df_code["CODE_SH"] == PosTarif_code)])