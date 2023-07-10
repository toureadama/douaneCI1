import streamlit as st
import pandas as pd
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Variation_CIAB7.py","Variation"),
    Page("pages/ControleCIAB7.py","Contrôle"),
    Page("pages/Suivi_CodeOperateurCIAB7.py","Suivi Opérateur")
])

update = False

@st.cache_resource 
def load_all_file(update):
    df  = pd.read_csv('df_CIAB7.csv')
    
    return df

df = load_all_file(update) 

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
