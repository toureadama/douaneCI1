# AVANT BASCULE
#**********************************************************************************
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

# Listes des mots de passe par département avec des tests.
list_MDP_NIV1  = ['OUI' , 'NIV1' ]
list_MDP       = ['BONJOUR' , 'BONSOIR', 'X', 'Y', 'Z' ]
list_MDP_CIAB1 = ['BONJOUR1', 'BONSOIR1', 'A', 'B', 'C', 'D', 'E']
list_MDP_CIAB3 = ['BONJOUR3', 'BONSOIR3', 'CIAB3']
list_MDP_CIAB5 = ['BONJOUR5', 'BONSOIR5', 'CIAB5']
list_MDP_CIAB6 = ['BONJOUR6', 'BONSOIR6', 'CIAB6']
list_MDP_CIAB7 = ['BONJOUR7', 'BONSOIR7', 'CIAB7']
list_MDP_CIABP = ['BONJOURP', 'BONSOIRP', 'CIABP']
list_MDP_ALLOU  = ['BAP']
list_MDP_KARIM  = ['CV']
list_MDP_ADMIN  = ['SERGE']

hide_pages(['Accueil', 'Admin', 'Contrôle 1er niveau', 'Variation', 'Variation1', 
            'Variation3', 'Variation5', 'Variation6', 'Variation7', 'VariationP','XL2',
             'Recherche', 'Analyse Valeurs', 'PU REC', "Contrôle Code Opérateur",
             "Analyse Espèces", "Analyse CC", "Contrôle Code Opérateur 2"
             ]) # 

st.text_input("Votre mot de passe", key="name", type='password')

# You can access the value at any point with:
if st.session_state.name in list_MDP:
    switch_page('Variation')
elif st.session_state.name in list_MDP_ADMIN:
    switch_page('Admin') 
elif st.session_state.name in list_MDP_NIV1:
    switch_page('Contrôle 1er niveau') 
elif st.session_state.name in list_MDP_ALLOU:
    switch_page('Recherche')   
elif st.session_state.name in list_MDP_KARIM:
    switch_page('PU REC')   
elif st.session_state.name in list_MDP_CIAB1:
    switch_page('Variation1')
elif st.session_state.name in list_MDP_CIAB3:
    switch_page('Variation3')
elif st.session_state.name in list_MDP_CIAB5:
    switch_page('Variation5')
elif st.session_state.name in list_MDP_CIAB6:
    switch_page('Variation6')
elif st.session_state.name in list_MDP_CIAB7:
    switch_page('Variation7')
elif st.session_state.name in list_MDP_CIABP:
    switch_page('VariationP')
else:
    st.write("Mot de passe incorrect")
    
# APRES BASCULE
#**********************************************************************************

#import pandas as pd
#import pymysql.cursors
#import streamlit as st
#from streamlit_extras.switch_page_button import switch_page
#from st_pages import Page, show_pages, hide_pages

#show_pages([
    #Page("Variation_forte.py","Accueil"),
    #Page("Administrateur.py","Admin"),
    #Page("read_xl2.py","XL2"),
    #Page("pages/testKarim.py","PU REC"),
    #Page("pages/testKarimpareto.py","Analyse CC"),
    #Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    #Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur 2"),
    #Page("pages/testAllou.py","Recherche"),
    #Page("pages/testAlloupareto.py","Analyse Valeurs"),
    #Page("pages/testAllouEspeces.py","Analyse Espèces"),
    #Page("pages/ControleNiveau1.py","Contrôle 1er niveau"),
    #Page("pages/Variation.py","Variation"),
    #Page("pages/Variation_CIAB1.py","Variation1"),
    #Page("pages/Variation_CIAB3.py","Variation3"),
    #Page("pages/Variation_CIAB5.py","Variation5"),
    #Page("pages/Variation_CIAB6.py","Variation6"),
    #Page("pages/Variation_CIAB7.py","Variation7"),
    #Page("pages/Variation_CIABP.py","VariationP")
#])


#hide_pages(['Accueil', 'Admin', 'Contrôle 1er niveau', 'Variation', 'Variation1', 
            #'Variation3', 'Variation5', 'Variation6', 'Variation7', 'VariationP','XL2',
#             'Recherche', 'Analyse Valeurs', 'PU REC', "Contrôle Code Opérateur",
             #"Analyse Espèces", "Analyse CC", "Contrôle Code Opérateur 2"
             #]) # 


##Etablir la connexion
#@st.cache_resource
#def init_connection():
    #host = 'sql11.freemysqlhosting.net'
    #user = 'sql11664568'
    #password = 'fMJHRX62M7'
    #database = 'sql11664568'
    #cursorclass=pymysql.cursors.DictCursor
    #return pymysql.connect(host=host, database=database, user=user, password=password, cursorclass=cursorclass)

#mydb = init_connection()

#mycursor = mydb.cursor()

#st.title('Bienvenue sur le page de connexion!')

#st.subheader("Les utilisateurs dans la base")
#mycursor.execute("select * from utilisateur")
#result = mycursor.fetchall()
#result = pd.DataFrame(result, columns=['ID','Nom','Prénom','Bureau','Base_de_donnees', 'Habilitation','Identifiant','Mot_de_passe'])
#st.dataframe(result)
#new_list = list(zip(list(result["Identifiant"]), list(result["Mot_de_passe"])))
#new_list_acces = list(zip(list(result["Bureau"]), list(result["Base_de_donnees"]), list(result["Habilitation"])))

#identifiant = st.text_input("Votre identifiant", key="name")
#mdp = st.text_input("Votre mot de passe", key="password", type="password")

#if (identifiant, mdp) in new_list:
    #ind = new_list.index((identifiant, mdp))
    #st.write(new_list_acces[ind][0:3])
    #if (new_list_acces[ind][0:3]==('CIAB1', 'Décisionnel', 'Vérificateur')) or (new_list_acces[ind][0:3]==('Scanner', 'Décisionnel', 'Vérificateur')):
        #switch_page('Variation1')
    #elif new_list_acces[ind][0:3]==('CIAB3', 'Décisionnel', 'Vérificateur'):
        #switch_page('Variation3')
    #elif new_list_acces[ind][0:3]==('CIAB6Neuf', 'Décisionnel', 'Vérificateur'):
        #switch_page('Variation6')
    #elif new_list_acces[ind][0:3]==('BRP', 'Décisionnel', 'Vérificateur'):
        #switch_page('Variation5')
    #elif new_list_acces[ind][0:3]==('CIABP', 'Décisionnel', 'Vérificateur'):
        #switch_page('VariationP')
    #elif new_list_acces[ind][1:3]==('Décisionnel', 'Manager'):
        #switch_page('Contrôle 1er niveau') 
    #elif new_list_acces[ind][0:3]==('TOUT', 'Décisionnel', 'Vérificateur'):
        #switch_page('Variation')
    #elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CV')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CV')):
        #switch_page('PU REC')
    #elif (new_list_acces[ind][0:3]==('CIAB1', 'RFCV', 'CB')) or (new_list_acces[ind][0:3]==('Scanner', 'RFCV', 'CB')):
        #switch_page('Recherche')   
    #elif new_list_acces[ind][0]=='ADMIN':
        #switch_page('Admin')
    #else:
        #st.write("Cet utilisateur n'a pas d'accès défini")
#else:
    #st.write("Mot de passe incorrect")
