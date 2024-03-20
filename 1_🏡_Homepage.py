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
    if st.button("Visualize Data"):
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
    combined_df['Result'] = combined_df['Result'].replace({'P#': 'P', 'PF': 'P', 'FF': 'F', 'F\nP': 'F'})

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

    # Function to remove the pattern '(cid:13)\n*'
    def remove_pattern(text):
        if isinstance(text, str):
            pattern = r'\(cid:13\)\n\*'
            cleaned_text = re.sub(pattern, '', text)
            return cleaned_text
        return text  # If not a string, return as is

    # Apply the cleaning function to the entire DataFrame
    combined_df = combined_df.applymap(remove_pattern)

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

# Step 3: Data Visualization
st.subheader("Data Visualization :")

# Allow user to select a student or 'Overall' option
selected_student = st.selectbox("Select a student or 'Overall'", ["Overall"] + combined_df['Student Name'].unique().tolist())

if selected_student == "Overall":
    if combined_df is not None:
        # 1. Calculate the number of students, pass, and fail
        total_students = len(combined_df)
        pass_count = len(combined_df[combined_df['Result'].str.contains('P', case=False, na=False)])  
        fail_count = total_students - pass_count
        st.markdown(f"<b>Total Students: {total_students} </b>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:green; ">Passed Students : {pass_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:red; ">Failed Students : {fail_count}</div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # 2. Students Marks
        sorted_df = combined_df.sort_values(by='CGPI', ascending=False)
        sorted_df['Rank'] = range(1, len(sorted_df) + 1)
        # Print the sorted DataFrame with ranks
        st.markdown(f"<b>Students Marks : </b>", unsafe_allow_html=True)
        st.write(sorted_df)
        
        # 3. Overall pass/fail Pie chart
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f"<b>PASS/FAIL : </b>", unsafe_allow_html=True)
        pass_fail_counts = combined_df['Result'].value_counts()
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(pass_fail_counts, labels=pass_fail_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.savefig("pass_fail_pie.png")
        st.image("pass_fail_pie.png")
        
        # 4. Avg CGPI
        st.markdown(f"<b>Average CGPI : </b>", unsafe_allow_html=True)
        avg_cgpi = combined_df['CGPI'].mean()
        st.write(f"Average CGPI: {avg_cgpi:.2f}")
        st.markdown('<br>', unsafe_allow_html=True)

        # 5. Top 5 students as per SGPI
        st.markdown(f"<b>Top 5 as per SGPI, (This Sem Toppers) : </b>", unsafe_allow_html=True)
        top_sgpi_students = combined_df.sort_values(by='SGPI', ascending=False).head(5)
        sns.set(rc={'figure.figsize': (15, 6)})
        fig, ax = plt.subplots()
        sns.barplot(data=top_sgpi_students, x='Student Name', y='SGPI')
        for i in range(len(top_sgpi_students)):
            plt.text(i, top_sgpi_students['SGPI'].iloc[i], f"{top_sgpi_students['SGPI'].iloc[i]:.2f}", ha="center", va="bottom")
        plt.savefig("top_sgpi_students.png")
        st.image("top_sgpi_students.png")

        # 6. Top 5 students as per CGPI
        st.markdown(f"<b>TOP 5 as per CGPI : </b>", unsafe_allow_html=True)
        top_cgpi_students = combined_df.sort_values(by='CGPI', ascending=False).head(5)
        sns.set(rc={'figure.figsize': (15, 6)})
        fig, ax = plt.subplots()
        sns.barplot(data=top_cgpi_students, x='Student Name', y='CGPI')
        for i in range(len(top_cgpi_students)):
            plt.text(i, top_cgpi_students['CGPI'].iloc[i], f"{top_cgpi_students['CGPI'].iloc[i]:.2f}", ha="center", va="bottom")
        plt.savefig("top_cgpi_students.png")
        st.image("top_cgpi_students.png")

        # 7. Subject-wise performance for the whole class
        subject_columns = [col for col in combined_df.columns if col not in ['Seat No', 'Student Name', 'CGPI', 'SGPI', 'Result', 'Total']]
        subject_columns = [col for col in subject_columns if not col.startswith('Unnamed')]
        subject_columns = subject_columns[:-2]

        if len(subject_columns) > 0:
            # Allow user to select a subject
            st.markdown(f"<b>WHOLE CLASS SUBJECT WISE PERFORMANCE : </b>", unsafe_allow_html=True)
            selected_subject = st.selectbox('Select a subject', subject_columns)
            
            if selected_subject:
                # Use regular expressions to remove alphabetical letters and convert to float
                values = [float(re.sub('[^0-9.]', '', str(value)) if re.search(r'\d', str(value)) else 0) for value in combined_df[selected_subject]]

                # Calculate the average score for the selected subject
                average_score = sum(values) / len(values)
                st.write(f"<b>Average score for '{selected_subject}: {average_score:.2f}'</b>", unsafe_allow_html=True)
                
                                # Create a bar plot for the selected subject
                fig, ax = plt.subplots()
                sns.barplot(data=combined_df, x='Student Name', y=values, color='dodgerblue')
                ax.set_ylim(0, 100)  # Set the y-axis limit to 0-100
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Marks')
                ax.set_title(f'Whole Class - {selected_subject} Marks')

                # Add values on top of the bars
                for i in range(len(combined_df)):
                    plt.text(i, values[i], f"{values[i]:.2f}", ha="center", va="bottom")

                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
                plt.tight_layout()  # Adjust layout to prevent overlapping
                plt.savefig("subject_wise_performance.png")
                st.image("subject_wise_performance.png")

            else:
                st.write("Please select a subject.")
        else:
            st.write("No subject columns detected for the selected student.")
    
    else:
        st.write(f"{selected_student} not found in the dataset.")



                                                                        
