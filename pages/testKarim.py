import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testKarim.py","PU REC"),
])
# Chargement et observation du fichier 

update = True

@st.cache_resource
def load_file(update):
    df = pd.read_csv('mens_sortie_viandes_abats.csv')
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

prod = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    dpp['Position SH'].unique())

resultSH = dpp[dpp['Position SH']==prod]

descMarch = st.sidebar.selectbox(
    'Choisir la description de la marchandise',
    resultSH['DESCRIPTION MARCHANDISE'].unique())

resultDesMarch = resultSH[resultSH['DESCRIPTION MARCHANDISE']==descMarch]
resultDesMarch = resultDesMarch[['Origine', 'PU REC', 'N°Déclaration REC']].drop_duplicates()

st.write('Données de comparaison')
st.dataframe(resultDesMarch, use_container_width=True)


