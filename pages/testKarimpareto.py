import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/testKarimpareto.py","Analyse CC"),
    Page("pages/testKarim.py","PU REC")
])
# Chargement et observation du fichier 

update = True

@st.cache_resource
def load_file(update):
    frmCC = pd.read_csv('frm_CC.csv')
    
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

st.dataframe(result[['code opérateur', 'nbre déclarations',	'percent']], use_container_width=True)

st.write('Nombre opérateurs concernés ', result.shape[0], ' représentant ', f"{result['cum_percent'][-1:].iloc[0]:.0%}",' des opérateurs')

csv = result[['code opérateur', 'nbre déclarations', 'percent']].to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='SortiefrmCC.csv',
    mime='text/csv'
)
