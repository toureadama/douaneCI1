import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testKarimAllou.py","PU REC"),
    Page("pages/testAlloupareto.py","Analyse Valeurs"),
    Page("pages/testAllouEspeces.py","Analyse Espèces"),
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur")
])
# Chargement et observation du fichier 

update = False

@st.cache_resource
def load_file(update):
    df = pd.read_csv('sortie_viandes_abats.csv')
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

dpp['Date de la déclaration'] = pd.to_datetime(dpp['Date de la déclaration'])

date_min = min(dpp['Date de la déclaration'])
date_max = max(dpp['Date de la déclaration'])

debut = st.sidebar.date_input("Date de début:", value=date_min)
fin   = st.sidebar.date_input("Date de fin:", value=date_max)

dpp = dpp[(dpp['Date de la déclaration'] >= pd.to_datetime(debut)) & 
          (dpp['Date de la déclaration'] <= pd.to_datetime(fin))]
