import streamlit as st
import pandas as pd
from datetime import datetime
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/BazRec.py","Recherce"),
    Page("pages/BazAnalyse.py","Analyse"),
])


update = False

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource 
def load_all_file(update):
    #df  = pd.read_csv('C:/Users/HP 820 G3/Desktop/DOUANES CI/df_sortie/df_rfcv.csv', sep=";")
    df  = pd.read_csv('df_rfcv2.csv', sep=";")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['DATENR'] = pd.to_datetime(df['DATENR'])
    # valeur unitaire (Val CAF / Poids net)
    df = df[df["POIDSNET"] != 0]
    df["PU"] = df["VALCAF"] / df["POIDSNET"]
    
    return df

df = load_all_file(update) 

deb = df['DATENR'].min()
fin = df['DATENR'].max()

DateDeb = st.sidebar.date_input(label="Date de début", value=deb, min_value=deb, max_value=fin)
DateFin = st.sidebar.date_input(label="Date de fin", value=DateDeb,min_value=DateDeb, max_value=fin)

if DateDeb:# & DateFin:
    dfR = df[(df['DATENR'] >= pd.to_datetime(DateDeb)) & (df['DATENR'] <= pd.to_datetime(DateFin))]
    
    SHrfcv = st.sidebar.selectbox('', dfR['SH_FCVR'].unique(), index=None, placeholder="Choisir le numéro SH")
    if SHrfcv != None:
        dfR = dfR[dfR['SH_FCVR'] == SHrfcv]
    
    Devise = st.sidebar.selectbox('', dfR['CODE_DEVISE'].unique(), index=None, placeholder="Choisir la devise")
    if Devise != None:
        dfR = dfR[dfR['CODE_DEVISE'] == Devise]
    
    Origin = st.sidebar.selectbox('', dfR['ORIGINE'].unique(), index=None, placeholder="Choisir le pays d''origine")
    if Origin != None:
        dfR = dfR[dfR['ORIGINE'] == Origin]
        
    Fournisseur = st.sidebar.selectbox('', dfR['FOURNISSEUR_IMP_CLIENT_EXP'].unique(), index=None, placeholder="Choisir le fournisseur")
    if Fournisseur != None:
        dfR = dfR[dfR['FOURNISSEUR_IMP_CLIENT_EXP'] == Fournisseur]
    
    PrixU = st.sidebar.selectbox('', dfR['PU'].unique(), index=None, placeholder="Choisir le prix unitaire")
    

if st.button('Analyser'):
    st.write('Le nombre de RFCV ayant un prix unitaire inférieur à ', int(PrixU),' est: ', dfR[dfR['PU'] > PrixU].shape[0])
    st.write('Le nombre de RFCV ayant un prix unitaire supérieur à ', int(PrixU),' est: ', dfR[dfR['PU'] < PrixU].shape[0])
        
    