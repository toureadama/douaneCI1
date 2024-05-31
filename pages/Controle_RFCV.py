import streamlit as st
import pandas as pd
from io import BytesIO
from st_pages import Page, show_pages
import xlsxwriter

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Controle_RFCV.py","Contrôle"),
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur")
])

update = False

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource 
def load_all_file(update):
    df = pd.read_csv('df_RFCV.csv', sep=";")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    return df

df = load_all_file(update) 

Descriptif = st.sidebar.selectbox(
    'Choisir le descriptif de marchandise',
    df['DESCRIPTION_PRODUIT_FCVR'].unique())

if Descriptif:
    Origin = st.sidebar.selectbox(
        'Origine de la marchandise',
        df[df['DESCRIPTION_PRODUIT_FCVR']==Descriptif]['ORIGINE'].unique())

PdsNet = st.sidebar.number_input(
    'Renseigner le poids net (kgs)', 0)

ValeurFOB = st.sidebar.number_input(
    'Renseigner la valeur FOB')

exch = st.sidebar.number_input(
    'Renseigner le taux de change de la devise du FOB et le FCFA', 1.00)

Val_moy = df[
    (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif) 
    & (df["ORIGINE"] == Origin)]["PU_moy"].unique()[0]

Val_min = df[
    (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif) 
    & (df["ORIGINE"] == Origin)]["PU_min"].unique()[0]

Val_max = df[
    (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif) 
    & (df["ORIGINE"] == Origin)]["PU_max"].unique()[0]

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
    (df['DESCRIPTION_PRODUIT_FCVR']==Descriptif)  
    & (df["ORIGINE"] == Origin)]

Comp.loc[:, "Pds Net Rel"] = abs(Comp.loc[:, "POIDSNET"] - PdsNet)
Comp.sort_values(by=["Pds Net Rel"], inplace=True)
Comp.drop(columns=["Pds Net Rel"], inplace=True)


st.write(f"Quelques exemples de déclarations de la même catégorie.")
st.write(Comp.T)

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    Comp.to_excel(writer, sheet_name='sortie')

download1 = st.download_button(
    label="Export sous Excel",
    data=buffer.getvalue(),
    file_name='Sortie.xlsx',
    mime='application/vnd.ms-excel'
)