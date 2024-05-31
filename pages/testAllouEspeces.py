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

update = True

@st.cache_resource
def load_file(update):
    df = pd.read_csv('especes.csv', sep=";")
    
    return df

df = load_file(update)

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

esp = st.sidebar.selectbox(
    'Choisir la description de marchandise',
    df['DESCRIPTION_PRODUIT_FCVR'].unique())

result = df[df['DESCRIPTION_PRODUIT_FCVR']==esp]

res_max = result['TC'].max()

result['DC'] = result.loc[:, 'DT'].copy()

for i in range(result.shape[0]): 
    result['DC'].iloc[i] = res_max * result['VALCAF'].iloc[i] - result['DT'].iloc[i]

result['TC'] = result['TC'].map('{:.1%}'.format)
result['DC'] = result['DC'].map('{:.0f}'.format)
result['SH_FCVR'] = result['SH_FCVR'].map('{:.0f}'.format)

# Traitement des fraudes en valeur
st.write('Tableau pour analyser les déclarations Espèces')


st.dataframe(result.sort_values(by='TC', ascending=False), use_container_width=True)
st.write('Nombre de champs concernés:', result.shape[0])

# Extraction sous Excel

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    result.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)