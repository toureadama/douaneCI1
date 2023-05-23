import streamlit as st
import pandas as pd
import pandas as pd

update = True

@st.cache_resource
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_CIAB1.csv')
    df_Scan      = pd.read_csv('df_Scan.csv')
    df_BAE_Auto  = pd.read_csv('df_BAE.csv')
    
    return df_CIAB1, df_Scan, df_BAE_Auto

df_CIAB1, df_Scan, df_BAE_Auto = load_all_file(update) 


department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'Scanner', 'BAE'))

if department == 'CIAB1':
    df = df_CIAB1
elif department == 'Scanner':
    df = df_Scan
elif department == 'BAE':
    df = df_BAE_Auto
else:
    st.sidebar.write("Veuillez sélectionner le département.")

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

Operateur = st.sidebar.selectbox(
    'Code Opérateur',
    df['Code Opérateur'].unique(), index=10)

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
