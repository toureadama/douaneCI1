import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from st_pages import Page, show_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/FOBUn.py","Analyse Fret RFCV")
])


update = True

# Chargement des fichiers contenant déjà les variables retraitées
@st.cache_resource
def load_file(update):
    
    df = pd.read_csv("Fret_1er_SEMESTRE_2024.csv", sep=';', low_memory=False) # C:/Users/HP 820 G3/Desktop/ZZ/
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['Date Déclaration'] = df['Date Déclaration'].apply(lambda x:datetime.strptime(x, "%d/%m/%Y"))
       
    return df

df = load_file(update)


date_min = min(df['Date Déclaration'])
date_max = max(df['Date Déclaration'])


debut = st.sidebar.date_input("Date de début:", value=date_min)
fin   = st.sidebar.date_input("Date de fin:", value=date_max)

df = df[(df['Date Déclaration'] >= pd.to_datetime(debut)) & 
          (df['Date Déclaration'] <= pd.to_datetime(fin))]

origine = st.sidebar.selectbox(
    'Renseigner la provenance',
    df['Origine'].unique(), index=0)

if origine:
    conteneur = st.sidebar.selectbox(
        'Choisir le type de conteneur',
        df[df['Origine']==origine]['Type Conteneur'].unique())
    
    if conteneur:
        sh = st.sidebar.selectbox(
            'Choisir la position tarifaire',
            df[(df['Origine']==origine) & (df['Type Conteneur']==conteneur)]['SH Déclaré'].unique())
        
        if sh:
            Dev = st.sidebar.selectbox(
                'Choisir la devise', 
                df[(df['Origine']==origine) 
                    & (df['Type Conteneur']==conteneur)
                    & (df['SH Déclaré']==sh)]['Devise'].unique())


            data = df[(df['Origine']==origine) 
                      & (df['Type Conteneur']==conteneur)
                      & (df['SH Déclaré'] == sh)
                      & (df['Devise'] == Dev)]
            
            data.sort_values(by=["Fret Unitaire"], inplace=True, ignore_index=True)
            
            donnees = pd.DataFrame.from_dict({'Fret Unitaire min': [round(data['Fret Unitaire'].iloc[0], 0)], 
                                              'Fret Unitaire moyen': [round(data['Fret Unitaire'].mean(), 0)],
                                              'Fret Unitaire max': [round(data['Fret Unitaire'].iloc[-1], 0)], 
                                              'Devise': [data['Devise'].iloc[0]],
                                              'Decla inf': [data['N° Déclaration'].iloc[0]], 
                                              'Decla sup': [data['N° Déclaration'].iloc[-1]]})

            st.dataframe(donnees)
            
            NBCont = st.number_input('Renseigner le nombre de conteneurs', 1)
            NBCont_inf = NBCont * donnees['Fret Unitaire min'].iloc[0]
            NBCont_sup = NBCont * donnees['Fret Unitaire max'].iloc[0]
            Dev = donnees['Devise'].iloc[0]
            
            st.write("Le fret devrait être compris entre {} {} et {} {}".format(NBCont_inf, Dev, NBCont_sup, Dev))

            #st.write("Le fret devrait être compris entre {} et {}".format(NBCont * data['Fret Unitaire min'].iloc[0], NBCont * data['Fret Unitaire max'].iloc[0]))
