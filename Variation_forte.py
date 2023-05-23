import streamlit as st
import pandas as pd

update = True

@st.cache_resource
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_rest.csv')
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