import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages
import xlsxwriter

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Variation.py","Variation"),
    Page("pages/Controle.py","Contrôle"),
    Page("pages/Suivi_CodeOperateur.py","Suivi Opérateur")
])

update = True

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_all_file(update):
    df_CIAB1     = pd.read_csv('df_CIAB1.csv', sep=";")
    df_Scan      = pd.read_csv('df_Scan.csv', sep=";")
    df_BAE_Auto  = pd.read_csv('df_BAE.csv', sep=";")
    df_CIAB6_neuf  = pd.read_csv('df_CIAB6_neuf.csv', sep=";")
    df_CIAB3     = pd.read_csv('df_CIAB3.csv', sep=";")
    df_Auto3     = pd.read_csv('df_Auto3.csv', sep=";")
    df_CIAB5     = pd.read_csv('df_CIAB5.csv', sep=";")
    df_CIAB7     = pd.read_csv('df_CIAB7.csv', sep=";")
    df_CIABP     = pd.read_csv('df_CIABP.csv', sep=";")
    
    return df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf, df_CIAB3, df_Auto3, df_CIAB5, df_CIAB7, df_CIABP

df_CIAB1, df_Scan, df_BAE_Auto, df_CIAB6_neuf, df_CIAB3, df_Auto3, df_CIAB5, df_CIAB7, df_CIABP = load_all_file(update) 

department = st.sidebar.radio(
    "Choisir le département",
    ('CIAB1', 'CIAB1_Scanner', 'CIAB1_Auto', 'CIAB6_neuf', 'CIAB3', 'CIAB3_Auto', 'CIAB5', 'CIAB7', 'CIABP'))

if department == 'CIAB1':
    df = df_CIAB1
elif department == 'CIAB1_Scanner':
    df = df_Scan
elif department == 'CIAB1_Auto':
    df = df_BAE_Auto
elif department == 'CIAB6_neuf':
    df = df_CIAB6_neuf
elif department == 'CIAB3':
    df = df_CIAB3
elif department == 'CIAB3_Auto':
    df = df_Auto3
elif department == 'CIAB5':
    df = df_CIAB5
elif department == 'CIAB7':
    df = df_CIAB7
elif department == 'CIABP':
    df = df_CIABP
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

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_fourn_libel.to_excel(writer, sheet_name='sortie')

    download1 = st.download_button(
        label="Export sous Excel",
        data=buffer.getvalue(),
        file_name='Sortie.xlsx',
        mime='application/vnd.ms-excel'
    )
else:
    st.write(f":red[Il n'existe pas d'autre déclaration avec la même position tarifaire achetée chez le même fournisseur.]")

# Mettre dans un tableau toutes les déclarations avec 3 équivalentes

#st.write(nb_crit['N°déclaration'].iloc[2])
#st.write(nb_crit[nb_crit['N°déclaration']== nb_crit['N°déclaration'].iloc[2]].index[0])

#def tableau(nb_crit):
    #for i in nb_crit.shape[0]:
        #r = nb_crit[nb_crit['N°déclaration']== nb_crit['N°déclaration'].iloc[i]].index[0]
        #df_fourn_libel = df[
            #(df["Fournisseur"] == nb_crit["Fournisseur"][r]) & (df["Sous_Produit"] == nb_crit["Sous_Produit"][r])]
        ## Excure la déclaration comparée de la liste des déclarations équivalentes
        #df_fourn_libel = df_fourn_libel[
            #df_fourn_libel["N°déclaration"] != nb_crit['N°déclaration'].iloc[i]]
        #df_equiv.iloc[i] = df_fourn_libel.iloc[i]
    #return df_equiv
       
