import streamlit as st
import pandas as pd
from st_pages import Page, show_pages

from io import BytesIO
import xlsxwriter

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
resultDesMarch = resultDesMarch[['NUMENR', 'DATENR', 'BURENR', 'DECLARANT', 'OPERATEUR',
                                 'FOURNISSEUR_IMP_CLIENT_EXP', 'ORIGINE', 'SH_FCVR',
                                 'LIBELLE_SH_FCVR_SELON_LE_TARIF', 'DESCRIPTION_PRODUIT_FCVR', 'PU',
                                 'PU REC', 'NUMENR REC', 'FOURNISSEUR REC']]

st.dataframe(resultDesMarch, use_container_width=True)
st.write('Nombre de champs concernés:', resultDesMarch.shape[0])

# Extraction sous Excel

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    resultDesMarch.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)