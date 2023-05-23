import streamlit as st
import pandas as pd
import numpy as np


#st.text_input("Votre mot de passe", key="name")


# You can access the value at any point with:
#if st.session_state.name != "":
    #st.write("Mot de passe incorrect")
#else:
@st.cache_resource
def load_all_file():
    df_CIAB1 = pd.read_csv('df_rest.csv')
    df_Scan  = pd.read_csv('df_Scan.csv')
    
    return df_CIAB1, df_Scan

df_CIAB1, df_Scan = load_all_file() 

@st.cache_resource
def load_file(dep):
    # Chargement du fichier des données
    if dep == 2:
        df = df_Scan
    else:
        df = df_CIAB1
        
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

department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'Scanner'))

if department == 'CIAB1':
    dep = 1
elif department == 'Scanner':
    dep = 2
else:
    st.sidebar.write("Veuillez sélectionner le département.")


df = load_file(dep)


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

# Modiffication pour l'affichage de certaines données
#col_dec = ['D&T', 'Val FOB', 'Val CAF', 'Pds Brut', 'Pds Net', 'fret']
df_fourn_libel.loc[:, 'D&T']      = df_fourn_libel['D&T'].map('{:,d}'.format)
df_fourn_libel.loc[:, 'Val FOB']  = df_fourn_libel['Val FOB'].map('{:,d}'.format)
df_fourn_libel.loc[:, 'Val CAF']  = df_fourn_libel['Val CAF'].map('{:,d}'.format)
df_fourn_libel.loc[:, 'Pds Brut'] = df_fourn_libel['Pds Brut'].map('{:,d}'.format)
df_fourn_libel.loc[:, 'Pds Net']  = df_fourn_libel['Pds Net'].map('{:,d}'.format)
df_fourn_libel.loc[:, 'fret']     = df_fourn_libel['fret'].map('{:,d}'.format)

#col_mille = ['D&T_tx', 'PU', 'PU_moy', 'Ecart']
df_fourn_libel.loc[:, 'D&T_tx'] = df_fourn_libel['D&T_tx'].map('{:.2f}'.format)
df_fourn_libel.loc[:, 'PU']     = df_fourn_libel['PU'].map('{:.2f}'.format)
df_fourn_libel.loc[:, 'PU_moy'] = df_fourn_libel['PU_moy'].map('{:.2f}'.format)
df_fourn_libel.loc[:, 'PU_min'] = df_fourn_libel['PU_min'].map('{:.2f}'.format)
df_fourn_libel.loc[:, 'PU_max'] = df_fourn_libel['PU_max'].map('{:.2f}'.format)
df_fourn_libel.loc[:, 'Ecart']  = df_fourn_libel['Ecart'].map('{:.2f}'.format)

st.write("Nombre de déclarations équivalente:", df_fourn_libel.shape[0])
df_fourn_libel.T

csv = df_fourn_libel.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='Sortie.csv',
    mime='text/csv'
)