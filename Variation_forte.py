import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("pages/Variation.py","Variation"),
    Page("pages/Variation_CIAB1.py","Variation1"),
    Page("pages/Variation_CIAB3.py","Variation3"),
    Page("pages/Variation_CIAB6.py","Variation6")
])

# Listes des mots de passe par département
list_MDP       = ['BONJOUR' , 'BONSOIR', 'X', 'Y', 'Z' ]
list_MDP_CIAB1 = ['BONJOUR1', 'BONSOIR1', 'A', 'B', 'C', 'D', 'E']
list_MDP_CIAB3 = ['BONJOUR3', 'BONSOIR3', 'CIAB3']
list_MDP_CIAB6 = ['BONJOUR6', 'BONSOIR6', 'CIAB6']

hide_pages(['Accueil', 'Variation', 'Variation1', 'Variation3', 'Variation6'])

st.text_input("Votre mot de passe", key="name", type='password')

# You can access the value at any point with:
if st.session_state.name in list_MDP:
    switch_page('Variation')
elif st.session_state.name in list_MDP_CIAB1:
    switch_page('Variation1')
elif st.session_state.name in list_MDP_CIAB3:
    switch_page('Variation3')
elif st.session_state.name in list_MDP_CIAB6:
    switch_page('Variation6')
else:
    st.write("Mot de passe incorrect")
    
