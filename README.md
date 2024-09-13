# GradeGraph

GradeGraph is a tool we built to solve the time-consuming challenge of extracting student information from result PDFs. It's designed to make it easy for teachers to assess their entire class's performance and for students to quickly view their semester grades. GradeGraph also offers simple and effective data visualization features. and allows students as well as teachers to quickly view their semester grades with the added benefit of intuitive data visualization.
![image](https://github.com/user-attachments/assets/58e23744-dc48-4035-9565-e9cf93651dc0)
![Screenshot (213)](https://github.com/user-attachments/assets/7b5470fe-dfd5-40d5-9783-32391f41a3cc)
![Screenshot (217)](https://github.com/user-attachments/assets/c168b76f-42c3-4715-904f-c722b180629b)
![Screenshot (216)](https://github.com/user-attachments/assets/cdc023f5-9111-49ec-a5b8-13f2da04d81e)
![Screenshot (215)](https://github.com/user-attachments/assets/03088656-bbb6-4246-bb87-ea8b7916cdd3)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Data Extraction and Cleaning](#data-extraction-and-cleaning)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GradeGraph is designed to assist educators, students, and researchers in extracting relevant data from LTCE result PDFs and preparing it for further analysis. It simplifies the process of cleaning and structuring data, making it suitable for visualization, reporting, and other educational purposes.

## Features

- Extracts data from LTCE result PDFs for semesters 3, 4, 5, and 6.
- Cleans and formats the extracted data.
- Customizable to handle specific data patterns.
- Generates an Excel file with cleaned data for further use.
- Simple and user-friendly interface.

## Getting Started

### Prerequisites

Before using GradeGraph, make sure you have the following software and libraries installed on your system:

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the GradeGraph repository to your local machine:

   ```shell
   git clone https://github.com/your-username/GradeGraph.git
   ```

2. Navigate to the project directory:

   ```shell
   cd GradeGraph
   ```

3. Install the required Python packages using pip:

   ```shell
   pip install -r requirements.txt
   ```

Now, GradeGraph is set up and ready to use.

## Usage

To use GradeGraph, follow these steps:

1. Run the application:

   ```shell
   streamlit run app.py
   ```

2. Upload the LTCE result PDF for semester 3, 4, 5, or 6.

3. Click the "Extract and Clean PDF Data" button to process the data.

4. GradeGraph will extract and clean the data from the PDF and generate an Excel file.

5. Download the cleaned Excel file for further analysis and visualization.

## Data Extraction and Cleaning

GradeGraph performs the following data extraction and cleaning steps:

1. Extracts tabular data from PDF pages.

2. Cleans and formats the extracted data.
   
3. Cleans CGPI (Cumulative Grade Point Index) and SGPI (Semester Grade Point Index) values, handling specific error patterns.

4. Extracts seat numbers and student names from the data.

## Customization

You can customize GradeGraph to handle specific data patterns by modifying the cleaning functions in the code. Follow the code comments to identify and modify the cleaning functions as needed.

## Contributing

We welcome contributions from the community. If you have suggestions for improvements, found bugs, or want to contribute new features, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
