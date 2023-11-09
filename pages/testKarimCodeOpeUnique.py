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

update = False

@st.cache_resource
def load_file(update):
    df = pd.read_csv('mens_sortie_viandes_abats.csv')
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

codop = st.sidebar.selectbox(
    'Choisir le code opérateur',
    dpp['Code opérateur'].unique())

resultcodop = dpp[dpp['Code opérateur']==codop]
resultcodop = resultcodop[['DESCRIPTION MARCHANDISE', 'Origine', 'PU REC', 'N°Déclaration REC']].drop_duplicates()
st.dataframe(resultcodop, use_container_width=True)

st.write("Nombre de déclarations trouvées :", f"{resultcodop.shape[0]}")

csv = resultcodop.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='SortieFrm.csv',
    mime='text/csv'
)