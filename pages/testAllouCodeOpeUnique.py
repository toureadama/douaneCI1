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
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur")
])
# Chargement et observation du fichier 

update = False

@st.cache_resource
def load_file(update):
    df = pd.read_csv('sortie_viandes_abats.csv', sep=";") # sortie_va
    
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

#st.write(dpp.columns)

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