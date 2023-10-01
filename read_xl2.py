import streamlit as st
import pandas as pd
from io import BytesIO

output = BytesIO()

df = pd.read_excel("TEC_CEDEAO/TEC_CEDEAO_SH_2017_LR_TAXES.xlsx")
#st.dataframe(df)
st.write(df.head())

def to_excel2(df):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()

excel_data = to_excel2(df)
file_name = "excel.xlsx"
st.download_button(
    f"Click to download {file_name}",
    excel_data,
    file_name,
    f"text/{file_name}",
     key=file_name
)