import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages
import xlsxwriter


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
    df = pd.read_csv('mens_sortie_viandes_abats.csv', sep=";")
    
    return df

dpp = load_file(update)

dpp = dpp.loc[:, ~dpp.columns.str.contains('^Unnamed')]

codop = st.sidebar.selectbox(
    'Choisir le code opérateur',
    dpp['CODE_OPERATEUR'].unique())

resultcodop = dpp[dpp['CODE_OPERATEUR']==codop]
resultcodop = resultcodop.drop_duplicates()

st.dataframe(resultcodop, use_container_width=True)

st.write("Nombre de déclarations trouvées :", f"{resultcodop.shape[0]}")

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    resultcodop.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)