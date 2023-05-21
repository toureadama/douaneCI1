import streamlit as st
import pandas as pd
import numpy as np
import time


@st.cache_resource
def load_file():
    # Chargement du fichier des données
    df = pd.read_csv('df_rest_total.csv')
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

    return df

df = load_file()

Operateur = st.sidebar.selectbox(
    'Code Opérateur',
    df['Code Opérateur'].unique())

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
