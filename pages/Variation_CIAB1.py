import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    #Page("pages/Variation_CIAB1.py","Variation"),
    Page("pages/ControleCIAB1.py","Contrôle"),
    Page("pages/Suivi_CodeOperateurCIAB1.py","Suivi Opérateur")
])

update = False

@st.cache_resource
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_CIAB1.csv')
    df_Scan      = pd.read_csv('df_Scan.csv')
    
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
        
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#df.loc[:, 'Pds Net']  = df.loc[:, 'Pds Net'].map('{:,d}'.format)

# Seuil critique de x fois la moyenne du groupe
seuil = st.sidebar.slider('Seuil', 0, 6, 5)

nb_crit = df[df["Ecart"] > seuil]
pourc = df[df["Ecart"] > seuil].shape[0]/df.shape[0] * 100

st.write(f"Le nombre de déclarations critiques à :red[{seuil:.0f}] fois la moyenne est {nb_crit.shape[0]:.0f} déclarations(s). Ce qui correspond à {pourc:.1f} % de l'ensemble du groupe concerné.")

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

# Excure la déclaration comparée de la liste des déclarations équivalentes
df_fourn_libel = df_fourn_libel[df_fourn_libel["N°déclaration"] != declaration]

if df_fourn_libel.shape[0] > 0:
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

else:
    st.write(f":red[Il n'existe pas d'autre déclaration avec la même position tarifaire achetée chez le même fournisseur.]")
