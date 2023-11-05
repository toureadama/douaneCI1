import pandas as pd
import streamlit as st
from io import BytesIO

# Chargement et observation du fichier 

update = False

@st.cache_resource
def load_all_file(update):
    df = pd.read_csv("sortie_viandes_abats.csv")
    st.write(df.shape)
    return df

dpp = load_all_file(update)

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

output = BytesIO()

def to_excel2(df):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()

excel_data = to_excel2(resultDesMarch)
file_name = "sortie.xlsx"
st.download_button(
    f"Exporter sous Excel",
    excel_data,
    file_name,
    f"text/{file_name}",
    key=file_name
)