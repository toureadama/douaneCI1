import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testKarimAllou.py","PU REC"),
    Page("pages/testAlloupareto.py","Analyse Risques"),
    Page("pages/testAllouEspeces.py","Analyse Espèces")
])
# Chargement et observation du fichier 

update = True

@st.cache_resource
def load_file(update):
    df = pd.read_csv('sortie_viandes_abats.csv')
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

date_min = min(dpp['Date de la déclaration'])
date_max = max(dpp['Date de la déclaration'])

#debut = st.sidebar.date_input("Date de début:", min_value=date_min, max_value=date_max)
#fin   = st.sidebar.date_input("Date de fin:", min_value=date_min, max_value=date_max) 

prod = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    dpp['Position SH'].unique())

resultSH = dpp[dpp['Position SH']==prod]

descMarch = st.sidebar.selectbox(
    'Choisir la description de la marchandise',
    resultSH['DESCRIPTION MARCHANDISE'].unique())

resultDesMarch = resultSH[resultSH['DESCRIPTION MARCHANDISE']==descMarch]

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
