#! C:\Users\HP 820 G3\Desktop\DOUANES CI\douanenv\Scripts\python.exe

import pandas as pd
import pymysql.cursors
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages

# Identification des onglets à faire apparaître
show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin"),
    Page("pages/testKarim.py","PU REC"),
    Page("pages/testKarimpareto.py","Analyse CC"),
    Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur 2"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testAlloupareto.py","Analyse Valeurs"),
    Page("pages/testAllouEspeces.py","Analyse Espèces"),
    Page("pages/ControleNiveau1.py","Contrôle 1er niveau"),
    Page("pages/Controle.py","Controle"),
    Page("pages/Controle_CIAB1.py","Controle1"),
    Page("pages/Controle_CIAB3.py","Controle3"),
    Page("pages/Controle_CIAB5.py","Controle5"),
    Page("pages/Controle_CIAB6.py","Controle6"),
    Page("pages/Controle_CIAB7.py","Controle7"),
    Page("pages/Controle_CIABP.py","ControleP")
])


hide_pages(['Accueil', 'Admin', 'Contrôle 1er niveau', 'Controle', 'Controle1', 
            'Controle3', 'Controle5', 'Controle6', 'Controle7', 'ControleP',
             'Recherche', 'Analyse Valeurs', 'PU REC', "Contrôle Code Opérateur",
             "Analyse Espèces", "Analyse CC", "Contrôle Code Opérateur 2"
             ])  


#Etablir la connexion
#@st.cache_resource
def init_connection():
    host = 'sql11.freemysqlhosting.net'
    user = 'sql11664568'
    password = 'fMJHRX62M7'
    database = 'sql11664568'
    cursorclass=pymysql.cursors.DictCursor
    return pymysql.connect(host=host, database=database, user=user, password=password, cursorclass=cursorclass)

mydb = init_connection()

mycursor = mydb.cursor()

st.title('Bienvenue sur le page de connexion!')


mycursor.execute("select * from utilisateur")
result = mycursor.fetchall()
result = pd.DataFrame(result)#, columns=['ID','Nom','Prénom','Bureau','Base_de_donnees', 'Habilitation','Identifiant','Mot_de_passe'])

new_list = list(zip(list(result["Identifiant"]), list(result["Password"])))
new_list_acces = list(zip(list(result["Bureau"]), list(result["BDD"]), list(result["Acces"])))

identifiant = st.text_input("Votre identifiant", key="name")
mdp = st.text_input("Votre mot de passe", key="password", type="password")

if st.button('Valider'):
    if (identifiant, mdp) in new_list:
        ind = new_list.index((identifiant, mdp))
        
        if new_list_acces[ind][0]=='Admin':
            switch_page('Admin')
        elif (new_list_acces[ind][0:3]==('CIAB1', 'Décisionnel', 'Vérificateur')) or (new_list_acces[ind][0:3]==('Scanner', 'Décisionnel', 'Vérificateur')):
            switch_page('Controle1')
        elif new_list_acces[ind][0:3]==('CIAB3', 'Décisionnel', 'Vérificateur'):
            switch_page('Controle3')
        elif new_list_acces[ind][0:3]==('CIAB6Neuf', 'Décisionnel', 'Vérificateur'):
            switch_page('Controle6')
        elif new_list_acces[ind][0:3]==('BRP', 'Décisionnel', 'Vérificateur'):
            switch_page('Controle5')
        elif new_list_acces[ind][0:3]==('CIABP', 'Décisionnel', 'Vérificateur'):
            switch_page('ControleP')
        elif new_list_acces[ind][1:3]==('Décisionnel', 'Manager'):
            switch_page('Contrôle 1er niveau') 
        elif new_list_acces[ind][0:3]==('TOUT', 'Décisionnel', 'Vérificateur'):
            switch_page('Controle')
        elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CV')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CV')):
            switch_page('PU REC')
        elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CB')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CB')):
            switch_page('Recherche')   
        else:
            st.write("Cet utilisateur n'a pas d'accès défini")
    else:
        st.write("Mot de passe incorrect")

        
