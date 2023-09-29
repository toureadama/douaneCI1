import streamlit as st
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Variation_CIAB6.py","Variation"),
    Page("pages/ControleCIAB6.py","Contrôle"),
    Page("pages/Suivi_CodeOperateurCIAB6.py","Suivi Opérateur")
])

update = False

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource 
def load_all_file(update):
    df_CIAB6_neuf  = pd.read_csv('df_CIAB6_neuf.csv')
    
    return df_CIAB6_neuf

df = load_all_file(update) 

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Obligation de fournir le numéro de la déclaration
NumDecla = st.sidebar.text_input("Renseigner le numéro de déclaration")

if NumDecla :
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

    Comp.loc[:, "Pds Net Rel"] = abs(Comp.loc[:, "Pds Net"] - PdsNet)
    Comp.sort_values(by=["Pds Net Rel"], inplace=True)
    Comp.drop(columns=["Pds Net Rel"], inplace=True)

    # Appréciation de la suspicion
    Susp = st.radio(
        ":red[Suspicion confirmée?]",
        ('Oui', 'Non'))

    st.write(f"Quelques exemples de déclarations de la même catégorie.")
    st.write(Comp.T)

    csv = Comp.to_csv(index=False).encode('utf-8')

    download1 = st.download_button(
        label="Export sous CSV",
        data=csv,
        file_name='Sortie.csv',
        mime='text/csv'
    )