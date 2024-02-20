import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64 
import re

# Set page title and icon
st.set_page_config(page_title="GradeGraph", page_icon="📊")
# Header
# Center-aligned title
st.markdown('<div style="text-align: center;"><h1>📊GradeGraph</h1></div>', unsafe_allow_html=True)


# Add a larger emoji above and below the name in the sidebar using HTML and CSS
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 10.5rem;">📊</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 2.5rem;"><b>GradeGraph</b></span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center;"><span style="font-size: 1.5rem;">"Developed by Data Science Students"</span></div>', unsafe_allow_html=True)



data_cleaned = False
combined_df = None

st.subheader("Data Extraction & Cleaning :")
st.write("Note : Upload only LTCE result pdf's of semester 3,4,5,6")
st.markdown('You can download LTCE result pdfs from here <a href="https://ltce-exam.blogspot.com/">LTCE RESULTS</a>', unsafe_allow_html=True)
uploaded_pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_pdf_file is not None:
    if st.button("Extract and Clean PDF Data"):
        extracted_data = []
        with pdfplumber.open(uploaded_pdf_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()

                if table is not None:  # Change this line
                    df = pd.DataFrame(table[1:], columns=table[0])
                    extracted_data.append(df)
        if extracted_data:  # Check if extracted_data is not empty
            combined_data = pd.concat(extracted_data, ignore_index=True)
            combined_df = combined_data  # Assign combined_data to combined_df here
# Data cleaning
if combined_df is not None:
    combined_df = combined_df.drop(combined_df.columns[1], axis=1)
    combined_df.columns = combined_df.iloc[0]
    combined_df = combined_df.iloc[:, :-1]
    combined_df.columns.values[0] = 'Seat No'
    combined_df.reset_index(drop=True, inplace=True)

    # Specify the correct column name that contains seat numbers
    seat_column_name = "Seat No"  # Replace with the actual column name

    # Extract Seat No and Student Name
    seat_no_pattern = r'\b\w{3}\d+\b'

    # Create new DataFrames for Seat No and Student Name
    seat_no_df = pd.DataFrame(columns=['Seat No'])
    student_name_df = pd.DataFrame(columns=['Student Name'])

    # Initialize variables for row indices
    row_idx = 0
    previous_name = None  # To store the previous student name
    unique_names = set()  # To track unique student names

    # Iterate through the specified column
    for cell_content in combined_df[seat_column_name]:
        if isinstance(cell_content, str):
            seat_matches = re.findall(seat_no_pattern, cell_content)
            if seat_matches:
                for seat_number in seat_matches:
                    seat_no_df.at[row_idx, 'Seat No'] = seat_number
                    row_idx += 1
            else:
                # Remove the pattern "Seat No / Name of Student ↓" and clean up student names
                cleaned_name = cell_content.strip().replace("Seat No / Name of Student ↓", "")

                  # Check if the cleaned name contains "Seat No" and remove it
                if "Seat No" in cleaned_name:
                    cleaned_name = cleaned_name.replace("Seat No", "")
                
                # Check if the cleaned name is empty
                if not cleaned_name:
                    # If empty, fill with the previous name (if available)
                    if previous_name:
                        cleaned_name = previous_name
                    else:
                        # If no previous name, skip this row
                        continue

                # Check if the name is unique
                if cleaned_name not in unique_names:
                    student_name_df.at[row_idx, 'Student Name'] = cleaned_name
                    unique_names.add(cleaned_name)
                    previous_name = cleaned_name
                    row_idx += 1

    combined_df.columns = list(combined_df.columns[:-4]) + ['Total', 'SGPI', 'Result', 'CGPI']
    combined_df['Result'] = combined_df['Result'].replace({'P#': 'P', 'PF': 'P', 'FF': 'F', 'F\nP':'F'})

    # ------------------------------------------------------------------------

    # e1
    # Function to clean the specific CGPI error pattern
    def clean_specific_pattern(cgpi):
        if pd.notna(cgpi):
            # Check for the specific error pattern like 'x1x2..y1y2' and replace it with 'x2.y2'
            if '..' in cgpi:
                x1, y1 = cgpi.split('..')
                x2, y2 = x1[-1], y1[1]
                cgpi = x2 + '.' + y2

        return cgpi

    # Apply the cleaning function to the 'CGPI' column
    combined_df['CGPI'] = combined_df['CGPI'].apply(clean_specific_pattern)

    # e2
    def clean_specific_pattern(cgpi):
        if pd.notna(cgpi):
            # Define a regular expression pattern to match the specific error pattern
            pattern = r'(\d)(\d)\.(\d)'
            match = re.match(pattern, cgpi)
            if match:
                # Extract the groups x1, x2, and y1
                x1, x2, y1 = match.groups()
                # Reconstruct the CGPI with x2.y1
                cgpi = x2
        return cgpi

    # Apply the cleaning function to the 'CGPI' column
    combined_df['CGPI'] = combined_df['CGPI'].apply(clean_specific_pattern)

    # Reset the index
    combined_df.reset_index(drop=True, inplace=True)

    # e3
    def clean_specific_pattern(cgpi):
        if pd.notna(cgpi):
            # Define a regular expression pattern to match the specific error pattern
            pattern = r'(\d+\.\d+)\n(\d+\.\d+)'
            match = re.match(pattern, cgpi)
            if match:
                # Extract the groups x1.x2 and y1.y2
                x1x2, y1y2 = match.groups()
                # Keep only y1.y2
                cgpi = y1y2

        return cgpi

    # Apply the cleaning function to the 'CGPI' column
    combined_df['CGPI'] = combined_df['CGPI'].apply(clean_specific_pattern)

    # Reset the index
    combined_df.reset_index(drop=True, inplace=True)

    # --------------------------------------------------------

    # SGPI
    # Function to clean the SGPI column
    def clean_sgpi(sgpi):
        if pd.notna(sgpi):
            # Remove any '-' and '\n' characters in the SGPI
            sgpi = sgpi.replace('-', '').replace('\n', '')

        return sgpi

    # Apply the cleaning function to the 'SGPI' column
    combined_df['SGPI'] = combined_df['SGPI'].apply(clean_sgpi)

    # Reset the index
    combined_df.reset_index(drop=True, inplace=True)

    # Function to remove the pattern '(cid:13)\n*'
    def remove_pattern(text):
        if isinstance(text, str):
            pattern = r'\(cid:13\)\n\*'
            cleaned_text = re.sub(pattern, '', text)
            return cleaned_text
        return text  # If not a string, return as is

    # Apply the cleaning function to the entire DataFrame
    combined_df = combined_df.applymap(remove_pattern)

    # ------------------------------------------------------------------------

    # Remove the specified column from combined_df
    combined_df.drop(seat_column_name, axis=1, inplace=True)

    # Drop rows with NaN values in the combined_df
    combined_df = combined_df.dropna()

    # Reset the index for all data frames
    combined_df.reset_index(drop=True, inplace=True)
    seat_no_df.reset_index(drop=True, inplace=True)
    student_name_df.reset_index(drop=True, inplace=True)

    # Integrate Seat No and Student Name into the combined_df
    combined_df = pd.concat([seat_no_df, student_name_df, combined_df], axis=1)

    excel_buffer = BytesIO()
    combined_df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    st.success("PDF data extraction and data cleaning complete.")
    st.markdown("### Download Cleaned Data")
    st.markdown("Note: Plz note that we have cleaned data but still cross check it, if you find any garbage data plz clean it before moving to visualization")
    excel_base64 = base64.b64encode(excel_buffer.read()).decode()
    st.markdown(f'<a href="data:application/octet-stream;base64,{excel_base64}" download="cleaned_data.xlsx">Download Cleaned Excel file</a>',unsafe_allow_html=True)

#---------------------------------------------------------------------------


# Step 3: Data Visualization

st.subheader("Data Visualization :")
with st.expander("Upload Cleaned Excel file "):
    uploaded_excel = st.file_uploader("Note : Upload Cleaned Excel File (only extracted from GradeGraph files allowed)")

if uploaded_excel is not None:
    cleaned_df = pd.read_excel(uploaded_excel)

    # Fetch unique student names
    student_names = cleaned_df['Student Name'].unique().tolist()
    student_names.sort()

    # Allow user to select a student or 'Overall' option
    selected_student = st.selectbox("Select a student or 'Overall'", ["Overall"] + student_names)

#-----------------------------------------------------------------------------------------------------------

    if selected_student != "Overall":
        st.write(f"Analysis for {selected_student} goes here...")
        # Add code to display individual student graphs based on the selected student
        # Filter data for the selected student
        student_df = cleaned_df[cleaned_df['Student Name'] == selected_student]
        
      
       # 1. Calculate the number of students, pass, and fail
        total_students = len(cleaned_df)
        pass_count = len(cleaned_df[cleaned_df['Result'].str.contains('P', case=False, na=False)])  
        fail_count = total_students - pass_count
        st.markdown(f"<b>Total Students: {total_students} </b>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:green; ">Passed Students : {pass_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:red; ">Failed Students : {fail_count}</div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # 2. pass/fail status of student
        if not student_df.empty:
            pass_status = student_df['Result'].values[0]
            if pass_status == 'P':
                # If the student passed, display "Passed" with a green box
                st.markdown(f"<div style='background-color: limegreen; padding: 10px; border-radius: 5px;'>Congratulations 🎉😀, You passed this Sem</div>", unsafe_allow_html=True)
            else:
                # If the student failed, display "Failed" with a red box
                st.markdown(f"<div style='background-color: tomato; padding: 10px; border-radius: 5px;'>Better Luck Next Time 🥺😓</div>", unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)

            # 3. No. Of KT's
            def count_failures(column):
                return column.astype(str).str.count('F')
            # Select all columns except the last 4
            columns_to_check = student_df.columns[:-4]
            subject_columns = student_df.copy()
            total_kts = 0
            # Loop through the selected columns and add a 'KT' column
            for col in columns_to_check:
                subject_columns[f'{col}_KT'] = count_failures(student_df[col])

            # Print the 'KT' columns
            for col in columns_to_check:
                kt_column = f'{col}_KT'
                kt_count = subject_columns[kt_column].sum()
                total_kts += kt_count
                if kt_count > 0:
                    st.write(f"Failed in '{col}'")
            st.write(f"<b>Total KT </b>'{total_kts}'",unsafe_allow_html = True)
            
            
            
            # 4. Display individual student's CGPI and SGPI
            st.markdown(f"<b>CGPI : </b>", unsafe_allow_html=True)
            st.write(f"{selected_student}'s CGPI: {student_df['CGPI'].values[0]}")
            st.markdown(f"<b>SGPI : </b>", unsafe_allow_html=True)
            st.write(f"{selected_student}'s SGPI: {student_df['SGPI'].values[0]}")
            
            # 5. Rank and Marks
            st.markdown('<br>', unsafe_allow_html=True)
            sorted_df = cleaned_df.sort_values(by='CGPI', ascending=False)
            sorted_df['Rank'] = range(1, len(sorted_df) + 1)
            # Print the sorted DataFrame with ranks
            st.markdown(f"<b>Students Marks : </b>", unsafe_allow_html=True)
            selected_student_entry = sorted_df[sorted_df['Student Name'] == selected_student]
            st.write(selected_student_entry)
            # Find the rank of the selected student
            st.markdown(f"<b>OVERALL RANK : </b>", unsafe_allow_html=True)
            selected_student_rank = sorted_df[sorted_df['Student Name'] == selected_student]['Rank'].values[0]
            st.write(f"{selected_student}'s CGPI Rank: {selected_student_rank}")

            # Find the rank of the selected student
            st.markdown('<br>', unsafe_allow_html=True)
            sorted_df = cleaned_df.sort_values(by='SGPI', ascending=False)
            sorted_df['Rank'] = range(1, len(sorted_df) + 1)
            st.markdown(f"<b>THIS SEM RANK : </b>", unsafe_allow_html=True)
            selected_student_rank = sorted_df[sorted_df['Student Name'] == selected_student]['Rank'].values[0]
            st.write(f"{selected_student}'s SGPI Rank: {selected_student_rank}")
            st.write()
            # 6. subjects performance
            subject_columnss = [col for col in student_df.columns if col not in ['Seat No', 'Student Name', 'CGPI', 'SGPI', 'Result', 'Total']]
            subject_columnss = [col for col in subject_columnss if not col.startswith('Unnamed')]
            subject_columnss = subject_columnss[:-2]    

        if len(subject_columnss) > 0:
            
            # Allow user to select a subject
            st.markdown(f"<b>SUBJECT WISE PERFORMANCE : </b>", unsafe_allow_html=True)
            selected_subject = st.selectbox('Select a subject', subject_columnss)
            
            if selected_subject:
                # Use regular expressions to remove alphabetical letters and convert to float
                values = [float(re.sub('[^0-9.]', '', str(value)) if re.search(r'\d', str(value)) else 0) for value in student_df[selected_subject]]
                # Create a larger figure with Seaborn
                sns.set(rc={'figure.figsize': (10, 6)})
                fig, ax = plt.subplots()
                sns.barplot(data=student_df, x='Student Name', y=values, color='dodgerblue')
                ax.set_ylim(0, 100) 
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Marks')
                ax.set_title(f'{selected_student} - {selected_subject} Marks')

                # Add values on top of the bars
                for i in range(len(student_df)):
                    plt.text(i, values[i], f"{values[i]:.2f}", ha="center", va="bottom")
                    # Save the plot as an image (e.g., PNG)
                plt.savefig("img.png")
                st.image("img.png")
            
                
            else:
                st.write("Please select a subject.")
        else:
            st.write("No subject columns detected for the selected student.")
        
    else:      
        st.write(f"{selected_student} not found in the dataset.")

       
        
        
        
        
#---------------------------------------------------------------------------------------------------------    

    if selected_student == "Overall":
        # Add code to display overall student graphs
        
        # 1.Calculate the number of students, pass, and fail
        total_students = len(cleaned_df)
        pass_count = len(cleaned_df[cleaned_df['Result'].str.contains('P', case=False, na=False)])  
        fail_count = total_students - pass_count
        st.markdown(f"<b>Total Students: {total_students} </b>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:green; ">Passed Students : {pass_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:red; ">Failed Students : {fail_count}</div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # 2. Students Marks
        sorted_df = cleaned_df.sort_values(by='CGPI', ascending=False)
        sorted_df['Rank'] = range(1, len(sorted_df) + 1)
        # Print the sorted DataFrame with ranks
        st.markdown(f"<b>Students Marks : </b>", unsafe_allow_html=True)
        selected_overall = sorted_df
        st.write(selected_overall)
        
        # 3. Overall pass/fail Pie chart
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f"<b>PASS/FAIL : </b>", unsafe_allow_html=True)
        pass_fail_counts = cleaned_df['Result'].value_counts()
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(pass_fail_counts, labels=pass_fail_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.savefig("img.png")
        st.image("img.png")
        
        # 4. Avg CGPI
        st.markdown(f"<b>Average CGPI : </b>", unsafe_allow_html=True)
        avg_cgpi = cleaned_df['CGPI'].mean()
        st.write(f"Average CGPI: {avg_cgpi:.2f}")
        st.markdown('<br>', unsafe_allow_html=True)


        # 5. top 5 as per SGPI
        st.markdown(f"<b>Top 5 as per SGPI, (This Sem Toppers) : </b>", unsafe_allow_html=True)
        top_mathsstud = cleaned_df.groupby(['Student Name'], as_index=False)['SGPI'].sum().sort_values(by='SGPI', ascending=False).head(5)
        sns.set(rc={'figure.figsize': (15, 6)})
        fig, ax = plt.subplots()
        sns.barplot(data=top_mathsstud, x='Student Name', y='SGPI')
        for i in range(len(top_mathsstud)):
            plt.text(i, top_mathsstud['SGPI'].iloc[i], f"{top_mathsstud['SGPI'].iloc[i]:.2f}", ha="center", va="bottom")
        plt.savefig("img.png")
        st.image("img.png")

        
        # 6. top 5 
        st.markdown(f"<b>TOP 5 as per CGPI : </b>", unsafe_allow_html=True)
        top_mathsstud = cleaned_df.groupby(['Student Name'], as_index=False)['CGPI'].sum().sort_values(by='CGPI', ascending=False).head(5)
        sns.set(rc={'figure.figsize': (15, 6)})
        fig, ax = plt.subplots()
        sns.barplot(data=top_mathsstud, x='Student Name', y='CGPI')
        for i in range(len(top_mathsstud)):
            plt.text(i, top_mathsstud['CGPI'].iloc[i], f"{top_mathsstud['CGPI'].iloc[i]:.2f}", ha="center", va="bottom")
        plt.savefig("img.png")
        st.image("img.png")




        # Filter the subject columns
        subject_columns = [col for col in cleaned_df.columns if col not in ['Seat No', 'Student Name', 'CGPI', 'SGPI', 'Result', 'Total']]
        subject_columns = [col for col in subject_columns if not col.startswith('Unnamed')]
        subject_columns = subject_columns[:-2]

        if len(subject_columns) > 0:
        # Allow user to select a subject
            st.markdown(f"<b>WHOLE CLASS SUBJECT WISE PERFORMANCE : </b>", unsafe_allow_html=True)
            selected_subject = st.selectbox('Select a subject', subject_columns)
    
            if selected_subject:
                # Use regular expressions to remove alphabetical letters and convert to float
                values = [float(re.sub('[^0-9.]', '', str(value)) if re.search(r'\d', str(value)) else 0) for value in cleaned_df[selected_subject]]
        
                # Calculate the average score for the selected subject
                average_score = sum(values) / len(values)
                st.write(f"<b>Average score for '{selected_subject}: {average_score:.2f}'</b>",unsafe_allow_html=True)
                

        
            else:
                st.write("Please select a subject.")
        else:
            st.write("No subject columns detected for the selected student.")
        
        
# Footer
st.markdown("---")
st.markdown('<div style="text-align: center;">© 2023 GradeGraph</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">For more information Follow us on <a href="https://github.com/ganeshmohane/GradeGraph">GitHub</a></div>', unsafe_allow_html=True)
