import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testAlloupareto.py","Analyse Risques"),
    Page("pages/testKarim.py","PU REC")
])
# Chargement et observation du fichier 

update = False

@st.cache_resource
def load_file(update):
    frm = pd.read_csv('frm.csv')
    
    return frm

frm = load_file(update)

frm = frm.loc[:, ~frm.columns.str.contains('^Unnamed')]

par = st.sidebar.number_input(
        'Renseigner le niveau de pareto (%)', min_value=0, max_value=100, value=20)

result = frm[frm['pareto'] <= par/100]
resultEsp = frm[frm['pareto'] > par/100].sort_values(by='nbre déclarations', ascending=True)

# Traitement des fraudes en valeur
st.write('Tableau pour analyser les déclarations Valeurs')

# Extraction sous Excel

result['Position SH'] = result['Position SH'].map('{:.0f}'.format)
result['percent']     = result['percent'].map('{:.2f}'.format)
#result['cum_percent'] = result['cum_percent'].map('{:.2f}'.format)
#result['pareto']      = result['pareto'].map('{:.2f}'.format)

st.dataframe(result[['DESCRIPTION MARCHANDISE', 'Position SH', 'nbre déclarations',	'percent']], use_container_width=True)

st.write('Nombre de marchandises concernées ', result.shape[0], ' représentant ', f"{result['cum_percent'][-1:].iloc[0]:.0%}",' des déclarations totales')

csv = result[['DESCRIPTION MARCHANDISE', 'Position SH', 'nbre déclarations',	'percent']].to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='SortieFrm.csv',
    mime='text/csv'
)

# Traitement des fraudes en espèces

resultEsp['Position SH'] = resultEsp['Position SH'].map('{:.0f}'.format)

st.write('Tableau pour analyser les déclarations Espèces')
st.dataframe(resultEsp[['DESCRIPTION MARCHANDISE', 'Position SH', 'Libelle SH', 'nbre déclarations']], use_container_width=True)

csv2 = resultEsp.to_csv(index=False).encode('utf-8')

# download button 2 to download dataframe as csv
download2 = st.download_button(
    label="Exporter sous CSV",
    data=csv2,
    file_name='SortieEsp.csv',
    mime='text/csv'
)