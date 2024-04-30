import streamlit as st
import pandas as pd
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
update = True

@st.cache_resource
def load_file(update):
    df = pd.read_csv('sortie_viandes_abats.csv', sep=";")
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

dpp['DATENR'] = pd.to_datetime(dpp['DATENR'])

date_min = min(dpp['DATENR'])
date_max = max(dpp['DATENR'])

debut = st.sidebar.date_input("Date de début:", value=date_min)
fin   = st.sidebar.date_input("Date de fin:", value=date_max)

dpp = dpp[(dpp['DATENR'] >= pd.to_datetime(debut)) & 
          (dpp['DATENR'] <= pd.to_datetime(fin))]

prod = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    dpp['SH_FCVR'].unique())

resultSH = dpp[dpp['SH_FCVR']==prod]

descMarch = st.sidebar.selectbox(
    'Choisir la description de la marchandise',
    resultSH['DESCRIPTION_PRODUIT_FCVR'].unique())

resultDesMarch = resultSH[resultSH['DESCRIPTION_PRODUIT_FCVR']==descMarch]

st.dataframe(resultDesMarch, use_container_width=True)
st.write('Nombre de champs concernés:', resultDesMarch.shape[0])

# Extraction sous Excel

csv = resultDesMarch.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='Sortie.csv',
    mime='text/csv'
)
