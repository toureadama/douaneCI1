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
    df = pd.read_csv('especes.csv')
    
    return df

df = load_file(update)

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

esp = st.sidebar.selectbox(
    'Choisir la description de marchandise',
    df['DESCRIPTION MARCHANDISE'].unique())

result = df[df['DESCRIPTION MARCHANDISE']==esp]

res_max = result['TC'].max()

result['DC'] = result.loc[:, 'DT'].copy()

for i in range(result.shape[0]): 
    result['DC'].iloc[i] = res_max * result['Valeur CAF'].iloc[i] - result['DT'].iloc[i]

result = result[['DESCRIPTION MARCHANDISE', 'N°Déclaration', 'Date de la déclaration',
                 'Déclarant', 'Opérateur', 'Origine', 'Position SH', 'Libelle SH', 'DT',
                 'Valeur CAF', 'TC', 'Poids net', 'DC']]

result['TC'] = result['TC'].map('{:.1%}'.format)
result['DC'] = result['DC'].map('{:.0f}'.format)
result['Position SH'] = result['Position SH'].map('{:.0f}'.format)

# Traitement des fraudes en valeur
st.write('Tableau pour analyser les déclarations Espèces')


st.dataframe(result.sort_values(by='TC', ascending=False), use_container_width=True)
st.write('Nombre de champs concernés:', result.shape[0])

# Extraction sous Excel

csv = result.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='Sortie.csv',
    mime='text/csv'
)
