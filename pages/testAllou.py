import pandas as pd
import streamlit as st
from io import BytesIO

# Chargement et observation du fichier 

update = True

@st.cache_resource
def load_file(update):
    df = pd.read_csv('sortie_viandes_abats.csv')
    
    return df

dpp = load_file(update)

prod = st.sidebar.selectbox(
    'Choisir la position tarifaire',
    dpp['Position SH'].unique())

resultSH = dpp[dpp['Position SH']==prod]

descMarch = st.sidebar.selectbox(
    'Choisir la description de la marchandise',
    resultSH['DESCRIPTION MARCHANDISE'].unique())

resultDesMarch = resultSH[resultSH['DESCRIPTION MARCHANDISE']==descMarch]

st.dataframe(resultDesMarch, use_container_width=True)
st.write('Nombre de champs concernés:', resultDesMarch.shape[0])

# Extraction sous Excel

csv = resultDesMarch.to_csv(index=False).encode('utf-8')

# download button 1 to download dataframe as csv
download1 = st.download_button(
    label="Export sous CSV",
    data=csv,
    file_name='Sortie.csv',
    mime='text/csv'
)