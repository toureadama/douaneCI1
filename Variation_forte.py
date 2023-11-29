import pandas as pd
import pymysql.cursors
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin"),
    Page("read_xl2.py","XL2"),
    Page("pages/testKarim.py","PU REC"),
    Page("pages/testKarimpareto.py","Analyse CC"),
    Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur 2"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/testAlloupareto.py","Analyse Valeurs"),
    Page("pages/testAllouEspeces.py","Analyse Espèces"),
    Page("pages/ControleNiveau1.py","Contrôle 1er niveau"),
    Page("pages/Variation.py","Variation"),
    Page("pages/Variation_CIAB1.py","Variation1"),
    Page("pages/Variation_CIAB3.py","Variation3"),
    Page("pages/Variation_CIAB5.py","Variation5"),
    Page("pages/Variation_CIAB6.py","Variation6"),
    Page("pages/Variation_CIAB7.py","Variation7"),
    Page("pages/Variation_CIABP.py","VariationP")
])


hide_pages(['Accueil', 'Admin', 'Contrôle 1er niveau', 'Variation', 'Variation1', 
            'Variation3', 'Variation5', 'Variation6', 'Variation7', 'VariationP','XL2',
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
        
        if (new_list_acces[ind][0:3]==('CIAB1', 'Décisionnel', 'Vérificateur')) or (new_list_acces[ind][0:3]==('Scanner', 'Décisionnel', 'Vérificateur')):
            switch_page('Variation1')
        elif new_list_acces[ind][0:3]==('CIAB3', 'Décisionnel', 'Vérificateur'):
            switch_page('Variation3')
        elif new_list_acces[ind][0:3]==('CIAB6Neuf', 'Décisionnel', 'Vérificateur'):
            switch_page('Variation6')
        elif new_list_acces[ind][0:3]==('BRP', 'Décisionnel', 'Vérificateur'):
            switch_page('Variation5')
        elif new_list_acces[ind][0:3]==('CIABP', 'Décisionnel', 'Vérificateur'):
            switch_page('VariationP')
        elif new_list_acces[ind][1:3]==('Décisionnel', 'Manager'):
            switch_page('Contrôle 1er niveau') 
        elif new_list_acces[ind][0:3]==('TOUT', 'Décisionnel', 'Vérificateur'):
            switch_page('Variation')
        elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CV')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CV')):
            switch_page('PU REC')
        elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CB')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CB')):
            switch_page('Recherche')   
        elif new_list_acces[ind][0]=='ADMIN':
            switch_page('Admin')
        else:
            st.write("Cet utilisateur n'a pas d'accès défini")
    else:
        st.write("Mot de passe incorrect")
