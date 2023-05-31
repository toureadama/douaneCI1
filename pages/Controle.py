import streamlit as st
import pandas as pd


update = False

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource 
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_CIAB1.csv')
    df_Scan      = pd.read_csv('df_Scan.csv')
    df_BAE_Auto  = pd.read_csv('df_BAE.csv')
    df_CIAB6_neuf  = pd.read_csv('df_CIAB6_neuf.csv')
    
    return df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf

df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf = load_all_file(update) 

department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'Scanner', 'BAE', 'CIAB6_neuf'))

if department == 'CIAB1':
    df = df_CIAB1
elif department == 'Scanner':
    df = df_Scan
elif department == 'BAE':
    df = df_BAE_Auto
elif department == 'CIAB6_neuf':
    df = df_CIAB6_neuf
else:
    st.sidebar.write("Veuillez sélectionner le département.")

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

PosTarif = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    df['Produit'].unique())

if PosTarif :
    Libelle = st.sidebar.selectbox(
        'Choisir le libellé TEC',
        df[df['Produit']==PosTarif]['Sous_Produit'].unique())

    if Libelle:
        Origin = st.sidebar.selectbox(
            'Origine du produit',
            df[(df['Produit']==PosTarif) & (df["Sous_Produit"] == Libelle)]['Origine'].unique())

PdsNet = st.sidebar.number_input(
    'Renseigner le poids net (kgs)', 0)

Val_moy = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]["PU_moy"].unique()[0]

st.write(f"La valeur FOB moyenne doit être:")
st.header(f"**:blue[{PdsNet * Val_moy:,.0f}]** FCFA")

Comp = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]

Comp.loc[:, "Pds Net Rel"] = abs(Comp.loc[:, "Pds Net"] - PdsNet)
Comp.sort_values(by=["Pds Net Rel"], inplace=True)
Comp.drop(columns=["Pds Net Rel"], inplace=True)
Comp.loc[:, 'Pds Net']  = Comp['Pds Net'].map('{:,d}'.format)

st.write(f"Quelques exemples de déclarations de la même catégorie.")
st.write(Comp.T)

csv = Comp.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='Sortie.csv',
    mime='text/csv'
)