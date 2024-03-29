import streamlit as st
import pandas as pd
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Variation.py","Variation"),
    Page("pages/Controle.py","Contrôle"),
    Page("pages/Suivi_CodeOperateur.py","Suivi Opérateur")
])

update = True

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_CIAB1.csv', sep=";")
    df_Scan      = pd.read_csv('df_Scan.csv', sep=";")
    df_BAE_Auto  = pd.read_csv('df_BAE.csv', sep=";")
    df_CIAB6_neuf  = pd.read_csv('df_CIAB6_neuf.csv', sep=";")
    df_CIAB3     = pd.read_csv('df_CIAB3.csv', sep=";")
    df_Auto3     = pd.read_csv('df_Auto3.csv', sep=";")
    df_CIAB5     = pd.read_csv('df_CIAB5.csv', sep=";")
    df_CIAB7     = pd.read_csv('df_CIAB7.csv', sep=";")
    df_CIABP     = pd.read_csv('df_CIABP.csv', sep=";")
    
    return df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf, df_CIAB3, df_Auto3, df_CIAB5, df_CIAB7, df_CIABP

df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf, df_CIAB3, df_Auto3, df_CIAB5, df_CIAB7, df_CIABP = load_all_file(update) 

department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'CIAB1_Scanner', 'CIAB1_Auto', 'CIAB6_neuf', 'CIAB3', 'CIAB3_Auto', 'CIAB5', 'CIAB7', 'CIABP'))

if department == 'CIAB1':
    df = df_CIAB1
elif department == 'CIAB1_Scanner':
    df = df_Scan
elif department == 'CIAB1_Auto':
    df = df_BAE_Auto
elif department == 'CIAB6_neuf':
    df = df_CIAB6_neuf
elif department == 'CIAB3':
    df = df_CIAB3
elif department == 'CIAB3_Auto':
    df = df_Auto3
elif department == 'CIAB5':
    df = df_CIAB5
elif department == 'CIAB7':
    df = df_CIAB7
elif department == 'CIABP':
    df = df_CIABP
else:
    st.sidebar.write("Veuillez sélectionner le département.")

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

Operateur = st.sidebar.selectbox(
    'Code Opérateur',
    df['Code Opérateur'].unique(), index=0)

if Operateur:
    PosTarif = st.sidebar.selectbox(
        'Choisir la position tarifaire',
        df[df['Code Opérateur']==Operateur]['Produit'].unique())

    if PosTarif :
        Libelle = st.sidebar.selectbox(
            'Choisir le libellé TEC',
            df[(df['Code Opérateur']==Operateur) & (df['Produit']==PosTarif)]['Sous_Produit'].unique())

        if Libelle:
            Origin = st.sidebar.selectbox(
                'Origine du produit',
                df[(df['Code Opérateur']==Operateur) 
                   & (df['Produit']==PosTarif) 
                   & (df["Sous_Produit"] == Libelle)]['Origine'].unique())

data = df[(df['Code Opérateur']==Operateur) 
          & (df['Produit']==PosTarif) 
          & (df["Sous_Produit"] == Libelle)
          & (df['Origine'] == Origin)]

st.write(f"Evolution de la valeur FOB unitaire des **{Libelle}** en provenance de **{Origin}** de l'opérateur **{Operateur}**.")
st.line_chart(data=data, x='Date déclaration', y='PU')
