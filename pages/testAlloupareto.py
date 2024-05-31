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
    frm = pd.read_csv('frm.csv', sep=";")
    
    return frm

frm = load_file(update)

frm = frm.loc[:, ~frm.columns.str.contains('^Unnamed')]

par = st.sidebar.number_input(
        'Renseigner le niveau de pareto (%)', min_value=0, max_value=100, value=20)

result = frm[frm['pareto'] <= par/100]
resultEsp = frm[frm['pareto'] > par/100].sort_values(by='nbre déclarations', ascending=True)

# Traitement des fraudes en valeur
st.write('Tableau pour analyser les déclarations Valeurs')


result['Position SH'] = result['Position SH'].map('{:.0f}'.format)
result['percent']     = result['percent'].map('{:.2f}'.format)

st.dataframe(result[['DESCRIPTION MARCHANDISE', 'Position SH', 'Libelle SH', 'nbre déclarations',	'percent']], use_container_width=True)

st.write('Nombre de marchandises concernées ', result.shape[0], ' représentant ', f"{result['cum_percent'][-1:].iloc[0]:.0%}",' des déclarations totales')

csv = result[['DESCRIPTION MARCHANDISE', 'Position SH', 'Libelle SH', 'nbre déclarations',	'percent']]

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    csv.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)
