import streamlit as st
import pandas as pd
import pandas as pd

update = False

@st.cache_resource
def load_all_file(update):
    df_CIAB1 = pd.read_csv('df_CIAB1.csv')
    df_Scan  = pd.read_csv('df_Scan.csv')
    
    return df_CIAB1, df_Scan

df_CIAB1, df_Scan = load_all_file(update) 


department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'Scanner'))

if department == 'CIAB1':
    df = df_CIAB1
elif department == 'Scanner':
    df = df_Scan
else:
    st.sidebar.write("Veuillez sélectionner le département.")

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

#st.write(f"La valeur FOB moyenne doit être **:blue[{PdsNet * Val_moy:.0f}]** FCFA :sunglasses:")
st.write(f"La valeur FOB moyenne doit être:")
st.header(f"**:blue[{PdsNet * Val_moy:,.0f}]** FCFA")
#st.header(f"**:blue[{PdsNet * Val_moy:,d}]** FCFA")
# st.write(f":sunglasses:") 

Comp = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]

# Modiffication pour l'affichage de certaines données
#col_dec = ['D&T', 'Val FOB', 'Val CAF', 'Pds Brut', 'Pds Net', 'fret']
Comp.loc[:, 'D&T']      = Comp['D&T'].map('{:,d}'.format)
Comp.loc[:, 'Val FOB']  = Comp['Val FOB'].map('{:,d}'.format)
Comp.loc[:, 'Val CAF']  = Comp['Val CAF'].map('{:,d}'.format)
Comp.loc[:, 'Pds Brut'] = Comp['Pds Brut'].map('{:,d}'.format)
Comp.loc[:, 'Pds Net']  = Comp['Pds Net'].map('{:,d}'.format)
Comp.loc[:, 'fret']     = Comp['fret'].map('{:,d}'.format)

#col_mille = ['D&T_tx', 'PU', 'PU_moy', 'Ecart']
Comp.loc[:, 'D&T_tx'] = Comp['D&T_tx'].map('{:.2f}'.format)
Comp.loc[:, 'PU']     = Comp['PU'].map('{:.2f}'.format)
Comp.loc[:, 'PU_moy'] = Comp['PU_moy'].map('{:.2f}'.format)
Comp.loc[:, 'Ecart']  = Comp['Ecart'].map('{:.2f}'.format)

st.write(f"Quelques exemples de déclarations de la même catégorie.")
st.write(Comp.T)

