import pandas as pd
#from datetime import datetime, timedelta
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
       
    return df

df = load_file(update)

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


        data = df[(df['Origine']==origine) 
                & (df['Type Conteneur']==conteneur)
                & (df['SH Déclaré'] == sh)]
            
        #data = data[data['date_TC'] >= data['date_TC'].iloc[0] - timedelta(days=5)]

        st.dataframe(
            data[['Fret Unitaire min', 'Fret Unitaire moyen', 'Fret Unitaire max', 'Devise', 'N° Déclaration inf', 'N° Déclaration sup']].set_index([pd.Series([1])])
            )
        
        NBCont = st.number_input('Renseigner le nombre de conteneurs', 1)
        NBCont_inf = NBCont * data['Fret Unitaire min'].iloc[0]
        NBCont_sup = NBCont * data['Fret Unitaire max'].iloc[0]
        Dev = data['Devise'].iloc[0]
        
        st.write("Le fret devrait être compris entre {} {} et {} {}".format(NBCont_inf, Dev, NBCont_sup, Dev))

        #st.write("Le fret devrait être compris entre {} et {}".format(NBCont * data['Fret Unitaire min'].iloc[0], NBCont * data['Fret Unitaire max'].iloc[0]))
