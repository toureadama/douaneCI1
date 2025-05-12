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

timeout=st.secrets["timeout"]

connection = pymysql.connect(
    connect_timeout=st.secrets["timeout"],
    cursorclass=st.secrets["cursorclass"],
    db=st.secrets["db"],
    host=st.secrets["host"],
    password=st.secrets["password"],
    read_timeout=timeout,
    port=st.secrets["port"],
    user=st.secrets["user"],
    write_timeout=timeout,
)

st.write(timeout)
st.write(timeout)

cursor = connection.cursor()

try:
    cursor = connection.cursor()
    
except:
    st.write('pas ok') 

st.title('Bienvenue sur le page de connexion!')


cursor.execute("select * from utilisateur")
result = cursor.fetchall()
result = pd.DataFrame(result)#, columns=['ID','Nom','Prénom','Bureau','Base_de_donnees', 'Habilitation','Identifiant','Mot_de_passe'])

new_list = list(zip(list(result["identifiant"]), list(result["password"])))
new_list_acces = list(zip(list(result["bureau"]), list(result["bdd"]), list(result["acces"])))

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

        