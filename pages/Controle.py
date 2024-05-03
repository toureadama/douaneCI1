import streamlit as st
import pandas as pd
from st_pages import Page, show_pages
from io import BytesIO
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

ValeurFOB = st.sidebar.number_input(
    'Renseigner la valeur FOB')

exch = st.sidebar.number_input(
    'Renseigner le taux de change de la devise du FOB et le FCFA', 1.00)

Val_moy = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]["PU_moy"].unique()[0]

Val_min = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]["PU_min"].unique()[0]

Val_max = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]["PU_max"].unique()[0]

ValFOBref = PdsNet * Val_moy

st.write(f"La valeur FOB moyenne doit être:")
st.subheader(f"**:blue[{ValFOBref:,.0f}]** FCFA")
st.write(f"La valeur FOB minimale :blue[{PdsNet * Val_min:,.0f}] FCFA")
st.write(f"La valeur FOB maximale :blue[{PdsNet * Val_max:,.0f}] FCFA")

ValDD = ValFOBref - ValeurFOB * exch
if ValDD > 0:
    st.write(f"La valeur FOB déclarée par l'opérateur est de **:blue[{ValeurFOB * exch:,.0f}]** FCFA. Elle est sous-évaluée. Donc, ")
    st.write(f"la valeur taxable du DC est :red[{ValDD:,.0f}] FCFA")

Comp = df[
    (df["Produit"] == PosTarif) 
    & (df["Sous_Produit"] == Libelle) 
    & (df["Origine"] == Origin)]

Comp.loc[:, "Pds Net Rel"] = abs(Comp.loc[:, "Pds Net"].copy() - PdsNet)
Comp.sort_values(by=["Pds Net Rel"], inplace=True)
Comp.drop(columns=["Pds Net Rel"], inplace=True)

st.write(f"Quelques exemples de déclarations de la même catégorie.")
st.write(Comp.T)

# Extraction sous Excel


buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    Comp.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)