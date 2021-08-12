import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

def main():

    # ...
    st.sidebar.title("Cambridge Exam Results")
    st.sidebar.subheader("Navigation")

    # Declare pages
    pages = {
        "Overview": overview_page,
        "Report": report_page,
        "Summary": summary_page
    }

    # Declare grades
    grades = {
        # "None": None,
        "Grade 11": 1,
        "Grade 12": 2
    }

    # Set widget to select grade
    grade = st.sidebar.selectbox("Select a grade:",
                                 options=tuple(grades.keys()))


    page = st.sidebar.radio("Navigate pages:",
                            options=tuple(pages.keys()))

    if grade == None:
        pass
    else:
        # Fetch data
        data = get_data(level=grades[grade])

        # User interface widgets to define parameters
        ui_params = ui_navigation(target_page=page, target_grade=grade)

        # Display the selected page within the current session
        pages[page](params=ui_params, page_data=data)

# Define function to get data
def get_data(level):
    # ...
    data=None
    # Import data
    raw_data = pd.read_csv("data.csv")
    data = raw_data[raw_data.level == level]

    return data

# Define function to generate navigation from user input
def ui_navigation(target_page, target_grade):
    # Create dictionary to store input parameters
    ui_params = dict()

    # Declare subject options
    subject_map_dict = {
        'Biology': 'bio',
        'Chemistry': 'chem',
        'Economics': 'eco',
        'Global Perspectives': 'gp',
        'Mathematics': 'math',
        'Physics': 'phy',
        'Travel & Tourism': 'tt'
    }


    if target_grade == "Grade 11":
        # ...
        st.sidebar.subheader(f"{target_grade}")

        # Assign subject selection to subject variable
        subject = st.sidebar.selectbox("Select subject:",
                                       options=list(subject_map_dict.keys()),
                                       )

        # Append keys and values to parameter dictionary
        ui_params['level'] = 1
        ui_params['target_grade'] = target_grade
        ui_params['subject'] = [subject, subject_map_dict[subject]]

    elif target_grade == "Grade 12":
        # ...
        st.sidebar.subheader(f"{target_grade}")

        # Assign subject selection to subject variable
        subject = st.sidebar.selectbox("Select subject:",
                                       options=list(subject_map_dict.keys()))

        # Append keys and values to parameter dictionary
        ui_params['level'] = 2
        ui_params['target_grade'] = target_grade
        ui_params['subject'] = [subject, subject_map_dict[subject]]

    else:
        ui_params = None

    return ui_params

def overview_page(params, page_data):
    ## Initialise subject params as variables
    sub = params['subject'][1]  # subject abbreviation
    subject = params['subject'][0]  # subject name in full

    # ...
    st.title(f"Results for {params['target_grade']} - {subject}")

    ## Dataframe pipeline
    # Select grade appropriate letter grade index
    if params['level'] == 1:
        let_grad_index = ['A', 'B', 'C', 'D', 'E', 'F', 'U']
    else:
        let_grad_index = ['A*', 'A', 'B', 'C', 'D', 'E', 'F', 'U']

    # Set grade relevant data
    grade_filter = page_data['level'] == params['level']
    subj_data = page_data[grade_filter][sub]

    # Create dataframe
    df = (subj_data.value_counts().to_frame('Count').join(
        subj_data.value_counts(normalize=True).mul(100).round(decimals=2).to_frame('Percentage'))
    ).reindex(let_grad_index).fillna(0)

    ## Set page layout - Columns
    col1, col2 = st.beta_columns([2, 1])
    # Set column 1 - Graphs
    if params['level'] == 1:
        val = round(sum([g for g in df.loc[['A', 'B', 'C'], 'Percentage']]), 2)
        col1.subheader(f"Percentage grades A to C: {val} %")

    else:
        val = round(sum([g for g in df.loc[['A*', 'A', 'B', 'C'], 'Percentage']]), 2)
        col1.subheader(
            f"Percentage grades A* to C:    {val} %")
    g = sns.catplot(x=df.index, y='Count', data=df, kind='bar', height=4, aspect=1.1)
    # Customise graph object
    (g.set_axis_labels("Grades", "")) # label axes
    col1.pyplot(g) # Show graph

    # Set column 2 - Tables and graphs
    col2.subheader("Grade Summary:")

    col2.write(df[df.Count != 0])
    pie, ax = plt.subplots(figsize=[10, 6])

    plt.pie(x=df[df.Count != 0]['Count'].dropna(axis=0), autopct="%.1f%%", labels=df[df.Count != 0].index, pctdistance=0.5)
    plt.title(f"{params['target_grade']} {subject}", fontsize=14);
    col2.pyplot(pie)


def report_page(params, page_data):
    st.title("Report Page")
    image = Image.open(
        'https://images.unsplash.com/photo-1503387762-592deb58ef4e?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y29uc3RydWN0aW9ufGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60')
    st.write("""
    Welcome to the reports page.
    
    This part of the app will be developed at a later stage after consultation with department heads.
    
    This page has been included for proof of concept purposes, as this is a work in progress.
    
    Please provide any feedback or comments at vincevanderberg@nguyensieu.edu.vn
    
    Best
    
    Vince
    """)
    st.image(image, caption='Me hard at work')
def summary_page(params, page_data):
    st.title("Summary Page")
    image = Image.open(
        'https://images.unsplash.com/photo-1503387762-592deb58ef4e?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y29uc3RydWN0aW9ufGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60')
    st.write("""
        Welcome to the summary page.

        This part of the app will be developed at a later stage after consultation with department heads.

        This page has been included for proof of concept purposes, as this is a work in progress.

        Please provide any feedback or comments at vincevanderberg@nguyensieu.edu.vn

        Best

        Vince
        """)
    st.image(image, caption='Me hard at work')

if __name__ == "__main__":
    main()
