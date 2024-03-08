import streamlit as st
import pandas as pd
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Controle_All.py","Croisement")
])

update = False

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


try:
    
    # Charger le fichier des déclarations à vérifier
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        #dataframe = pd.read_csv(uploaded_file, sep=';')
        df_anorm = pd.read_excel(
            uploaded_file, 
            usecols= ["N°déclaration", "Bureau", "Déclarant", "Nom Opérateur", "Produit", "Type visite", "Origine", "Val FOB", "Pds Net"],
            engine='openpyxl'
            )
        
        df_anorm["Libelle_Produit"] = df_anorm["Produit"].copy()
        df_anorm["Sous_Produit"] = df_anorm["Produit"].copy()
        
        for i in range(df_anorm.shape[0]): 
            df_anorm.loc[df_anorm.index[i], 'Bureau']       = df_anorm.loc[df_anorm.index[i], 'Bureau'].split(' ')[0]
            df_anorm.loc[df_anorm.index[i], 'Sous_Produit'] = df_anorm.loc[df_anorm.index[i], 'Produit'].split('-')[-1].replace(' ', '', 1)
            df_anorm.loc[df_anorm.index[i], 'Produit']      = df_anorm.loc[df_anorm.index[i], 'Produit'].split(' ')[0]
        
    
    # Les codes SH des véhicules neufs
    neuf = ['8701201000', '8701301000', '8701911100', '8701911900', '8701921100', '8701921900', '8701931100', 
    '8701931900', '8701941100', '8701941900', '8701951100', '8701951900', '8702101110', '8702101190', '8702101210',
    '8702101290', '8702101310', '8702101390', '8702201110', '8702201190', '8702201210', '8702201290', '8702201310',
    '8702301110', '8702301210', '8702401110', '8702401210', '8702401310', '8702901110', '8702901190', '8702901210',
    '8702901290', '8702901310', '8702901390', '8703211100', '8703211900', '8703221100', '8703221900', '8703231100',
    '8703231900', '8703241100', '8703241900', '8703311100', '8703311900', '8703321100', '8703321900', '8703331100',
    '8703331900', '8703401100', '8703401900', '8703501100', '8703501900', '8703601100', '8703601900', '8703701100',
    '8703701900', '8703801100', '8703801900', '8704211110', '8704211190', '8704211910', '8704211990', '8704221110',
    '8704221190', '8704221910', '8704221990', '8704231110', '8704231190', '8704231910', '8704231990', '8704311110',
    '8704311190', '8704311910', '8704311990', '8704321110', '8704321190', '8704321910', '8704321990']


    def Anorm(i, departement, PosTarif, Libelle, Origin, PdsNet, ValeurFOB, exch=1.00):
        if df_anorm.loc[df_anorm.index[i], 'Bureau']   == 'CIAB1':
            df = df_CIAB1
        elif (df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB1') & (df_anorm.loc[df_anorm.index[i], 'Type visite'] == 'Annexe / Scanner'):
            df = df_Scan
        elif (df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB1') & (df_anorm.loc[df_anorm.index[i], 'Type visite'] == 'BAE Auto'):
            df = df_BAE_Auto
        elif (df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB6') & (df_anorm.loc[df_anorm.index[i], 'Produit'].isin(neuf)):
            df = df_CIAB6_neuf
        elif df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB3':
            df = df_CIAB3
        elif (df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB3') & (df_anorm.loc[df_anorm.index[i], 'Type visite'] == 'BAE Auto'):
            df = df_Auto3
        elif df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB5':
            df = df_CIAB5
        elif df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIAB7':
            df = df_CIAB7
        elif df_anorm.loc[df_anorm.index[i], 'Bureau'] == 'CIABP':
            df = df_CIABP
        else:
            df ='nan'
        
        df["Produit"] = df["Produit"].astype(str)
        
        try:
            Val_moy = df[
                (df["Bureau"] == departement) 
                & (df["Produit"] == PosTarif) 
                & (df["Sous_Produit"] == Libelle) 
                & (df["Origine"] == Origin)]["PU_moy"].unique()[0]
        
            ValFOBref = PdsNet * Val_moy

            ValDD = ValFOBref - ValeurFOB * exch
            
            # Fixer le seuil de l'appréciation de la suspicion
            susp = 0
            
            if ValDD > susp:
                warn = 'OUI'
                ValTaxDC = int(ValDD)

                Comp = df[
                    (df["Produit"] == PosTarif) 
                    & (df["Sous_Produit"] == Libelle) 
                    & (df["Origine"] == Origin)]

                Comp.loc[:, "Pds Net Rel"] = abs(Comp.loc[:, "Pds Net"] - PdsNet)
                Comp.sort_values(by=["Pds Net Rel"], inplace=True)
                Comp.drop(columns=["Pds Net Rel"], inplace=True)
                
                DeclaComp = list(Comp["N°déclaration"][0:5]) + [None] * (5 - len(list(Comp["N°déclaration"][0:5])))
            else:
                ValTaxDC = 0
                warn = 'NON'
                DeclaComp = [None, None, None, None, None]
        
        except:
            #st.write("Pas de base de comparaison")
            ValTaxDC = 0
            warn = 'NON'
            DeclaComp = [None, None, None, None, None]
        
        return warn, ValTaxDC, DeclaComp

    Alerte = []
    ValTax = []
    Decla  = []
    Decla1 = []
    Decla2 = []
    Decla3 = []
    Decla4 = []
    Decla5 = []

    for i in range(df_anorm.shape[0]):
        warn, ValTaxDC, DeclaComp = Anorm(i, df_anorm["Bureau"].iloc[i], df_anorm["Produit"].iloc[i], df_anorm["Sous_Produit"].iloc[i], df_anorm["Origine"].iloc[i], df_anorm["Pds Net"].iloc[i], df_anorm["Val FOB"].iloc[i], exch=1.00)
        #st.write(DeclaComp)
        Alerte.append(warn)
        ValTax.append(ValTaxDC)
        Decla.append(DeclaComp)
        Decla1.append(DeclaComp[0])
        Decla2.append(DeclaComp[1])
        Decla3.append(DeclaComp[2])
        Decla4.append(DeclaComp[3])
        Decla5.append(DeclaComp[4])
        
    df_anorm['WARNING']       = pd.DataFrame(Alerte)
    df_anorm['Valeur Tax DC'] = pd.DataFrame(ValTax)
    df_anorm['Déclaration 1']  = pd.DataFrame(Decla1)
    df_anorm['Déclaration 2']  = pd.DataFrame(Decla2)
    df_anorm['Déclaration 3']  = pd.DataFrame(Decla3)
    df_anorm['Déclaration 4']  = pd.DataFrame(Decla4)
    df_anorm['Déclaration 5']  = pd.DataFrame(Decla4)

    df_sortie = df_anorm[['N°déclaration', 'Déclarant', 'Nom Opérateur', 'Libelle_Produit', 'WARNING', 'Valeur Tax DC',
                    'Déclaration 1', 'Déclaration 2', 'Déclaration 3', 'Déclaration 4', 'Déclaration 5']]

    st.write(df_sortie)

    csv = df_sortie.to_csv(index=False).encode('utf-8')

    download1 = st.download_button(
        label="Export sous CSV",
        data=csv,
        file_name='Sortie_warning.csv',
        mime='text/csv'
    )
except:
    pass
