import streamlit as st
import pandas as pd
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Controle_RFCV.py","Contrôle"),
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur")
])

update = False

@st.cache_resource
def load_all_file(update):
    df = pd.read_csv('df_RFCV.csv', sep=";")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    return df

df = load_all_file(update) 

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

Operateur = st.sidebar.selectbox(
    'Code Opérateur',
    df['CODE_OPERATEUR'].unique(), index=0)

if Operateur:
    Descriptif = st.sidebar.selectbox(
        'Choisir le descriptif de marchandise',
        df[df['CODE_OPERATEUR']==Operateur]['DESCRIPTION_PRODUIT_FCVR'].unique())

    if Descriptif :
        Origin = st.sidebar.selectbox(
            'Origine du produit',
            df[(df['CODE_OPERATEUR']==Operateur) & (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif)]['ORIGINE'].unique())

data = df[(df['CODE_OPERATEUR']==Operateur) 
          & (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif) 
          & (df['ORIGINE'] == Origin)]

st.write(f"Evolution de la valeur FOB unitaire des **{Descriptif}** en provenance de **{Origin}** de l'opérateur **{Operateur}**.")
st.line_chart(data=data, x='DATENR', y='PU')
