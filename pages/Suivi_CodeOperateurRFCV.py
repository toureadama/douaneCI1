import pandas as pd
from datetime import datetime
import streamlit as st
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Controle_RFCV.py","Contrôle"), # FOBUn2.py
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur"), # FOBUn3.py
    Page("pages/testEspecesRFCV.py","Frêt") # FOBUn.py
])

update = False

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_file(update):
    
    df = pd.read_csv("sortie_ViAb_enquete.csv", sep=';', low_memory=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['DATENR'] = df['DATENR'].apply(lambda x:datetime.strptime(x, "%d/%m/%Y"))
       
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
    
    if origine:
        operateur = st.sidebar.selectbox(
        'Choisir le code opérateur',
        df[(df['SH_FCVR']==SH) & (df['ORIGINE']==origine)]['CODE_OPERATEUR'].unique())
    
        data = df[(df['SH_FCVR']==SH) 
                  & (df['ORIGINE']==origine)
                  & (df['CODE_OPERATEUR']==operateur)]
        
        
        data=data[['DESCRIPTION_PRODUIT_FCVR', 'DATENR', 'PU']]
        
        for descript in data['DESCRIPTION_PRODUIT_FCVR'].unique():
            st.write(descript)
            st.line_chart(data=data[data['DESCRIPTION_PRODUIT_FCVR']==descript], x='DATENR', y='PU')
        
        