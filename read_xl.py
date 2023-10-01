import streamlit as st
import pandas as pd
from io import BytesIO

output = BytesIO()

df = pd.read_excel("C:/Users/toure/Desktop/OpenClassrooms/DOUANES CI/TEC_CEDEAO/TEC_CEDEAO_SH_2017_LR_TAXES.xlsx")
#st.dataframe(df)
st.write(df.head())

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
df_xlsx = to_excel(df)
st.download_button(label='📥 Download Current Result',
                                data=df_xlsx ,
                                file_name= 'df_test.xlsx')


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

