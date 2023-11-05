import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("read_xl2.py","XL2"),
    Page("pages/testAllou.py","Allou"),
    Page("pages/ControleNiveau1.py","Contrôle 1er niveau"),
    Page("pages/Variation.py","Variation"),
    Page("pages/Variation_CIAB1.py","Variation1"),
    Page("pages/Variation_CIAB3.py","Variation3"),
    Page("pages/Variation_CIAB5.py","Variation5"),
    Page("pages/Variation_CIAB6.py","Variation6"),
    Page("pages/Variation_CIAB7.py","Variation7")
])

# Listes des mots de passe par département avec des tests.
list_MDP_NIV1  = ['OUI' , 'NIV1' ]
list_MDP       = ['BONJOUR' , 'BONSOIR', 'X', 'Y', 'Z' ]
list_MDP_CIAB1 = ['BONJOUR1', 'BONSOIR1', 'A', 'B', 'C', 'D', 'E']
list_MDP_CIAB3 = ['BONJOUR3', 'BONSOIR3', 'CIAB3']
list_MDP_CIAB5 = ['BONJOUR5', 'BONSOIR5', 'CIAB5']
list_MDP_CIAB6 = ['BONJOUR6', 'BONSOIR6', 'CIAB6']
list_MDP_CIAB7 = ['BONJOUR7', 'BONSOIR7', 'CIAB7']
list_MDP_ALLOU  = ['BAP']

hide_pages(['Accueil', 'Contrôle 1er niveau', 'Variation', 'Variation1', 
            'Variation3', 'Variation5', 'Variation6', 'Variation7']) # , 'XL','XL2', 'Allou'

st.text_input("Votre mot de passe", key="name", type='password')

# You can access the value at any point with:
if st.session_state.name in list_MDP:
    switch_page('Variation')
elif st.session_state.name in list_MDP_NIV1:
    switch_page('Contrôle 1er niveau') 
#elif st.session_state.name in list_MDP_ALLOU:
    #switch_page('Allou')   
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
else:
    st.write("Mot de passe incorrect")
    
