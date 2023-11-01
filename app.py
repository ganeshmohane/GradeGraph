import streamlit as st
import seaborn as sns
import pandas as pd
import pdfplumber
import matplotlib.pyplot as plt
from io import BytesIO
import base64 

data_cleaned = False
#Step 1 : pdf data extraction
def extract_pdf_data(pdf_file_path):
    extracted_data = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table() 

            if table is None:
                continue
            df = pd.DataFrame(table[1:], columns=table[0])
            extracted_data.append(df)

    combined_data = pd.concat(extracted_data, ignore_index=True)
    excel_buffer = BytesIO()
    combined_data.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)  
    return excel_buffer

st.title("GradeGraph")
st.header("Pdf Extraction and Analysis")


with st.expander("Step 1: Upload PDF File for Extraction"):
    uploaded_pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_pdf_file is not None:
        if st.button("Extract PDF Data"):
            excel_buffer = extract_pdf_data(uploaded_pdf_file)
            st.success(f"PDF data extraction complete.")
            st.markdown("### Download Extracted Data")
            st.markdown("Click below to download the extracted data as an Excel file.")
            excel_base64 = base64.b64encode(excel_buffer.read()).decode()
            st.markdown(f'<a href="data:application/octet-stream;base64,{excel_base64}" download="extracted_data.xlsx">Download Excel file</a>',
                        unsafe_allow_html=True)
            
            
#------------------------------------------------------------------


# Step 2: Upload Uncleaned Excel File
with st.expander("Step 2: Upload Uncleaned Excel File"):
    uploaded_uncleaned_excel_file = st.file_uploader("Choose the uncleaned Excel file", type=["xlsx"])
    
data_cleaned = False

if uploaded_uncleaned_excel_file is not None:
    uncleaned_df = pd.read_excel(uploaded_uncleaned_excel_file)
    cleaned_df = uncleaned_df.copy()
    cleaned_df = cleaned_df.drop(cleaned_df.columns[1], axis=1)
    cleaned_df = cleaned_df.dropna(subset=[cleaned_df.columns[0]])
    cleaned_df.columns = cleaned_df.iloc[0]
    cleaned_df = cleaned_df[1:]
    cleaned_df = cleaned_df.iloc[:, :-1]
    cleaned_df = cleaned_df.dropna()
    cleaned_df.columns = list(cleaned_df.columns[:-4]) + ['Total','SGPI', 'Result', 'CGPI']
    cleaned_df.reset_index(drop=True, inplace=True)

    data_cleaned = True
    
    if data_cleaned:
        cleaned_excel_file = 'cleaned_data.xlsx'
        cleaned_df.to_excel(cleaned_excel_file, index=False)
        st.success(f"Data cleaning complete.")
        st.markdown(f"[Download Cleaned Excel file](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(cleaned_excel_file, 'rb').read()).decode()})")
        
        
#---------------------------------------------------------------------------


# Step 3: Data Visualization
import matplotlib.pyplot as plt
st.expander("Step 3: Data Visualization")

uploaded_cleaned_excel_file = st.file_uploader("Choose the cleaned Excel file", type=["xlsx"])

if uploaded_cleaned_excel_file is not None:
    cleaned_df = pd.read_excel(uploaded_cleaned_excel_file)
    pass_fail_counts = cleaned_df['Result'].value_counts()
    st.write("Pass/Fail Distribution:")
    fig, ax = plt.subplots()
    ax.pie(pass_fail_counts, labels=pass_fail_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    st.pyplot(fig)
