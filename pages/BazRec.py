import streamlit as st
import pandas as pd
from datetime import datetime
from st_pages import Page, show_pages
from io import BytesIO
import xlsxwriter

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
    
    LibelleSHrfcv = st.sidebar.selectbox('', dfR['LIBELLE_SH_DEC'].unique(), index=None, placeholder="Choisir le libéllé SH")
    if LibelleSHrfcv != None:
        dfR = dfR[dfR['LIBELLE_SH_DEC'] == LibelleSHrfcv]
    
    Origin = st.sidebar.selectbox('', dfR['ORIGINE'].unique(), index=None, placeholder="Choisir le pays d''origine")
    if Origin != None:
        dfR = dfR[dfR['ORIGINE'] == Origin]
    
    PdsNetKgs = st.sidebar.selectbox('', dfR['POIDSNET'].unique(), index=None, placeholder="Choisir le poids net en kgs")
    if PdsNetKgs != None:
        dfR = dfR[dfR['POIDSNET'] == PdsNetKgs]
    
    NbArticle = st.sidebar.selectbox('', dfR['NOMBRE_ARTICLE'].unique(), index=None, placeholder="Choisir le nombre d''articles")
    if NbArticle != None:
        dfR = dfR[dfR['NOMBRE_ARTICLE'] == NbArticle]
    
    SHrfcv = st.sidebar.selectbox('', dfR['SH_FCVR'].unique(), index=None, placeholder="Choisir le numéro SH")
    if SHrfcv != None:
        dfR = dfR[dfR['SH_FCVR'] == SHrfcv]
        
    ValFOB = st.sidebar.selectbox('', dfR['VALFOB'].unique(), index=None, placeholder="Choisir la valeur FOB")
    if ValFOB != None:
        dfR = dfR[dfR['VALFOB'] == ValFOB]
    Devise = st.sidebar.selectbox('', dfR['LIBELLE_DEVISE'].unique(), index=None, placeholder="Choisir la devise")
    if Devise != None:
        dfR = dfR[dfR['LIBELLE_DEVISE'] == Devise]
        
    Fournisseur = st.sidebar.selectbox('', dfR['FOURNISSEUR_IMP_CLIENT_EXP'].unique(), index=None, placeholder="Choisir le fournisseur")
    if Fournisseur != None:
        dfR = dfR[dfR['FOURNISSEUR_IMP_CLIENT_EXP'] == Fournisseur]
    

df_Search = dfR[['DATENR', 'FOURNISSEUR_IMP_CLIENT_EXP', 'ORIGINE', 'LIBELLE_DEVISE', 
                 'NOMBRE_ARTICLE', 'POIDSNET', 'SH_FCVR', 'LIBELLE_SH_DEC', 'NUM_AV_FCVR', 'NBL', 'PU']]

if st.button('Rechercher'):
    st.dataframe(df_Search)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_Search.to_excel(writer, sheet_name='sortie')

    download1 = st.download_button(
        label="Export sous Excel",
        data=buffer.getvalue(),
        file_name='Sortie.xlsx',
        mime='application/vnd.ms-excel'
    )
        
    #csv = df_Search.to_csv(index=False).encode('utf-8')

    #download1 = st.download_button(
        #label="Export sous CSV",
        #data=csv,
        #file_name='Sortie.csv',
        #mime='text/csv'
    #)