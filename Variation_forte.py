#! C:\Users\HP 820 G3\Desktop\DOUANES CI\douanenv\Scripts\python.exe

import pandas as pd
import pymysql
import pymysql.cursors
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages, hide_pages, Page


# Identification des onglets 
show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin"),
    Page("pages/Controle_RFCV.py","ContrôleRFCV"), # FOBUn2.py
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur RFCV"), # FOBUn3.py
    Page("pages/testEspecesRFCV.py","Frêt") # FOBUn.py
    ])

hide_pages(['Accueil', 'Admin', 'ContrôleRFCV', 'Suivi Opérateur RFCV', "Frêt"])  
            
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
        elif new_list_acces[ind][0:3]==('TOUT', 'RFCV', 'Vérificateur'):
            switch_page('ContrôleRFCV')  
        else:
            st.write("Cet utilisateur n'a pas d'accès défini")
    else:
        st.write("Mot de passe incorrect")

        