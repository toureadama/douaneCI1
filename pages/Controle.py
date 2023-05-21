import streamlit as st
import pandas as pd
import numpy as np
import time


@st.cache_resource
def load_file():
    # Chargement du fichier des données
    df = pd.read_csv('df_rest.csv')
    df = df.drop(columns=df.columns[0])

    # Calcul du frêt
    df = df.dropna()
    df["fret"] = df["Val CAF"] - df["Val FOB"]
    # valeur unitaire (Val Fob / Poids net)
    df = df[df["Pds Net"] != 0]
    df["PU"] = df["Val FOB"] / df["Pds Net"]
    # Calcul du taux de la taxe de douane
    df["D&T_tx"] = df["D&T"].copy()
    df["D&T_tx"] = df["D&T"] / df["Val CAF"]

    df_mean = df[['Sous_Produit', 'Origine', 'PU']].groupby(['Sous_Produit', 'Origine']).mean()

    df["PU_moy"] = df["PU"].copy()

    for i in range(df.shape[0]):
        df["PU_moy"].iloc[i] = df_mean.loc[(df.Sous_Produit.iloc[i], df.Origine.iloc[i])][0]

    df["Ecart"] = df["PU_moy"] / df["PU"]
    df.insert(16, 'Sous_Produit', df.pop('Sous_Produit'))
    df.insert(27, 'D&T_tx', df.pop('D&T_tx'))

    return df

df = load_file()

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

