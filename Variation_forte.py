import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

output = BytesIO()

#st.text_input("Votre mot de passe", key="name")


# You can access the value at any point with:
#if st.session_state.name != "":
    #st.write("Mot de passe incorrect")
#else:
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
    df_min  = df[['Sous_Produit', 'Origine', 'PU']].groupby(['Sous_Produit', 'Origine']).min()
    df_max  = df[['Sous_Produit', 'Origine', 'PU']].groupby(['Sous_Produit', 'Origine']).max()

    df["PU_moy"] = df["PU"].copy()
    df["PU_min"] = df["PU"].copy()
    df["PU_max"] = df["PU"].copy()

    for i in range(df.shape[0]):
        df["PU_moy"].iloc[i] = df_mean.loc[(df.Sous_Produit.iloc[i], df.Origine.iloc[i])][0]
        df["PU_min"].iloc[i] = df_min.loc[(df.Sous_Produit.iloc[i], df.Origine.iloc[i])][0]
        df["PU_max"].iloc[i] = df_max.loc[(df.Sous_Produit.iloc[i], df.Origine.iloc[i])][0]

    df["Ecart"] = df["PU_moy"] / df["PU"]
    df.insert(16, 'Sous_Produit', df.pop('Sous_Produit'))
    df.insert(27, 'D&T_tx', df.pop('D&T_tx'))

    return df

df = load_file()

# Seuil critique de x fois la moyenne du groupe
seuil = st.sidebar.slider('Seuil', 0, 6, 5)

nb_crit = df[df["Ecart"] > seuil]
pourc = df[df["Ecart"] > seuil].shape[0]/df.shape[0] * 100

st.write(f"Le nombre de déclarations critiques à :red[{seuil:.0f}] fois la moyenne est {nb_crit.shape[0]:.0f} déclarations(s). Ce qui correspond à {pourc:.1f} % de l'ensemble du groupe concerné.")

nb_crit["Val FOB moy equivalent"] = nb_crit["PU_moy"] * nb_crit["Pds Net"]
nb_crit.insert(16, 'Sous_Produit', nb_crit.pop('Sous_Produit'))
nb_crit.insert(38, 'Val FOB', nb_crit.pop('Val FOB'))


declaration = st.sidebar.selectbox(
    'Choisir la déclaration',
    nb_crit['N°déclaration'])

result = nb_crit[nb_crit['N°déclaration']==declaration].index

if len(result) > 1:
    st.write(f"Attention, il y a {len(result)} fois cette même déclaration")
    decla = st.selectbox(
    'Choisir une position de la déclaration',
    list(range(len(result))))
    r = result[decla]
else:
    r = result[0]

gt = nb_crit["N°déclaration"][r]
st.write(f"le numéro de déclaration:{gt}")

Fourn = nb_crit["Fournisseur"][r]
Pos_tarif = nb_crit["Produit"][r]
Libelle = nb_crit["Sous_Produit"][r]
st.write(f"Le fournisseur: **{Fourn}**")
st.write(f"La position tarifaire:     **{Pos_tarif}**--- **{Libelle}**.")

df_fourn_libel = df[(df["Fournisseur"] == Fourn) & (df["Sous_Produit"] == Libelle)]

st.write("Nombre de déclarations équivalente:", df_fourn_libel.shape[0])
df_fourn_libel.T

writer = pd.ExcelWriter(output, engine='xlsxwriter')
df_fourn_libel.to_excel(writer, index=False, sheet_name='Sheet1')
workbook = writer.book
worksheet = writer.sheets['Sheet1']
writer.save()
processed_data = output.getvalue()

st.download_button(
    label='Exporter sous Excel',
    data=processed_data,
    file_name= 'Sortie.xlsx')

