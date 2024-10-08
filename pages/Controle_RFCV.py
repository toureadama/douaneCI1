import pandas as pd
from datetime import datetime
import streamlit as st
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Controle_RFCV.py","Contrôle"), # FOBUn2.py
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur"), # FOBUn3.py
    Page("pages/testEspecesRFCV.py","Frêt") # FOBUn.py
])

update = True

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_file(update):
    
    df = pd.read_csv("sortie_ViAb_enquete.csv", sep=';', low_memory=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['DATENR'] = df['DATENR'].apply(lambda x:datetime.strptime(x, "%Y/%m/%d"))
       
    return df

df = load_file(update)


date_min = min(df['DATENR'])
date_max = max(df['DATENR'])


debut = st.sidebar.date_input("Date de début:", value=date_min)
fin   = st.sidebar.date_input("Date de fin:", value=date_max)

df = df[(df['DATENR'] >= pd.to_datetime(debut)) & 
        (df['DATENR'] <= pd.to_datetime(fin))]

SH = st.sidebar.selectbox(
    'Renseigner la position SH',
    df['SH_FCVR'].unique(), index=0)

if SH:
    origine = st.sidebar.selectbox(
        'Choisir la provenance',
        df[df['SH_FCVR']==SH]['ORIGINE'].unique())

    
data = df[(df['SH_FCVR']==SH) & (df['ORIGINE']==origine)]

data['PU moyen'] = data['PU'].copy()
data['NB Déclarations'] = data['PU'].copy()

data['PU REF']   = data['PU'].copy()
data['NUMENR max'] = data['NUMENR'].copy()
data['FOURNISSEUR max'] = data['FOURNISSEUR_IMP_CLIENT_EXP'].copy()

for val in data.index: #range(data.shape[0]):
    TAB = data[data['DESCRIPTION_PRODUIT_FCVR']==data.loc[val, 'DESCRIPTION_PRODUIT_FCVR']]
    
    data.loc[val, 'NB Déclarations'] = TAB.shape[0]
    
    MOYEN = TAB['PU'].mean()
    MAX   = TAB['PU'].max()
    
    idx_mean = TAB.loc[TAB['PU']==MOYEN].index
    
    idx_max = TAB.loc[TAB['PU']==MAX].index
    data.loc[val, 'PU_REC'] = TAB.loc[idx_max[0], 'PU']
    data.loc[val, 'NUMENR_REC'] = TAB.loc[idx_max[0], 'NUMENR']
    data.loc[val, 'FOURNISSEUR_REC'] = TAB.loc[idx_max[0], 'FOURNISSEUR_IMP_CLIENT_EXP']

data.drop_duplicates(subset=['DESCRIPTION_PRODUIT_FCVR'], inplace=True, ignore_index=True)

data.sort_values(by='DESCRIPTION_PRODUIT_FCVR', inplace=True, ignore_index=True)

data = data[['DESCRIPTION_PRODUIT_FCVR', 'NB Déclarations', 'PU moyen',
             'PU_REC', 'NUMENR_REC', 'FOURNISSEUR_REC']]
st.dataframe(data=data)

# Extraction sous Excel

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    data.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)