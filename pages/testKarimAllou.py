import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages
import xlsxwriter

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testKarimAllou.py","PU REC"),
    Page("pages/testAlloupareto.py","Analyse Valeurs"),
    Page("pages/testAllouEspeces.py","Analyse Espèces"),
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/ControleNiveau1RFCV.py","Contrôle 1er niveau RFCV")
])

# Chargement et observation du fichier 

update = False

@st.cache_resource
def load_file(update):
    df = pd.read_csv('mens_sortie_viandes_abats.csv', sep=";")
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

prod = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    dpp['SH_FCVR'].unique())

resultSH = dpp[dpp['SH_FCVR']==prod]

descMarch = st.sidebar.selectbox(
    'Choisir la description de la marchandise',
    resultSH['DESCRIPTION_PRODUIT_FCVR'].unique())

resultDesMarch = resultSH[resultSH['DESCRIPTION_PRODUIT_FCVR']==descMarch]
resultDesMarch = resultDesMarch[['ORIGINE', 'PU REC', 'NUMENR REC']].drop_duplicates()

st.write('Données de comparaison')
st.dataframe(resultDesMarch, use_container_width=True)

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    resultDesMarch.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)
