import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages
import xlsxwriter

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/testKarimpareto.py","Analyse CC"),
    Page("pages/testKarim.py","PU REC"),
    Page("pages/ControleNiveau1RFCVKarim.py","Contrôle 1er niveau RFCV")
])

# Chargement et observation du fichier 

update = True

@st.cache_resource
def load_file(update):
    frmCC = pd.read_csv('frm_CC.csv', sep=";")
    
    return frmCC

frmCC = load_file(update)

frmCC = frmCC.loc[:, ~frmCC.columns.str.contains('^Unnamed')]

par = st.sidebar.number_input(
        'Renseigner le niveau de pareto (%)', min_value=0, max_value=100, value=20)

result = frmCC[frmCC['pareto'] <= par/100]

# Extraction sous Excel

result['percent'] = result['percent'].map('{:.2f}'.format)
#result['cum_percent'] = result['cum_percent'].map('{:.2f}'.format)
#result['pareto']      = result['pareto'].map('{:.2f}'.format)

st.dataframe(result[['CODE_OPERATEUR', 'nbre déclarations',	'percent']], use_container_width=True)

st.write('Nombre opérateurs concernés ', result.shape[0], ' représentant ', f"{result['cum_percent'][-1:].iloc[0]:.0%}",' des opérateurs')

csv = result[['CODE_OPERATEUR', 'nbre déclarations', 'percent']]

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    csv.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)