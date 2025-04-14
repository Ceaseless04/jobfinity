import sys
import os
import streamlit as st
import time

# Get current directory of app.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the parent folder of 'front_end_testing' to the path
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# Import from back_end_testing
from back_end_testing.resume_parser import parse_resume
from back_end_testing.job_matcher import match_jobs

st.set_page_config(page_title="AI-Powered Resume Analyzer")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'form'
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = ''
if 'upload_time' not in st.session_state:
    st.session_state.upload_time = None

# Function to move to result page
def go_to_result():
    st.session_state.page = 'result'
    st.session_state.upload_time = time.time()
    st.session_state.show_recommendations = False

# Go back to form page
def go_back():
    st.session_state.page = 'form'

# FORM PAGE
if st.session_state.page == 'form':
    st.markdown(
        """
        <div style='text-align: center; white-space: nowrap; overflow: hidden;'>
            <h2 style='color: #4CAF50; display: inline-block; font-size: 28px;' >
                Welcome to Jobfinity AI-Powered Resume Analyzer
            </h2>
        </div>
        <p style='color: #4CAF50; font-size: 18px; text-align: center;'>
            Please upload your resume to get job recommendations!!!
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("- This app uses AI models to analyze your resume and suggest job roles that match your skills and experience.")
    st.write("- Please fill in your name and upload your resume in PDF or DOCX format.")
    st.write("- Note: The resume will not be stored or shared with any third party. It will only be used for analysis.")

    name = st.text_input("Enter your name:", value=st.session_state.user_name)
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX):", type=None)

    # Keep track of previously uploaded file
    if not uploaded_file and st.session_state.uploaded_file:
        st.info(f"Previously uploaded file: **{st.session_state.uploaded_filename}**")
        uploaded_file = st.session_state.uploaded_file

    file_valid = False
    if uploaded_file:
        filename = uploaded_file.name
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ['.pdf', '.docx']:
            st.error("Invalid file type! Only .pdf or .docx files are allowed.")
        else:
            st.session_state.uploaded_file = uploaded_file
            st.session_state.uploaded_filename = filename
            file_valid = True

    if st.button("Submit"):
        if not name:
            st.warning("Please enter your name before submitting.")
        elif not st.session_state.uploaded_file:
            st.warning("Please upload a valid resume before submitting.")
        elif file_valid:
            st.session_state.user_name = name
            go_to_result()
            st.rerun()

# RESULT PAGE
elif st.session_state.page == 'result':
    st.markdown("### Confirm your name to view job recommendations:")

    name_display = st.text_input("Confirm your name:", key="confirmed_name", placeholder="Enter your name again")

    if st.button("Go Back to Edit Name/Resume"):
        go_back()
        st.rerun()

    if not name_display:
        st.warning("Please confirm your name to continue.")
    elif name_display != st.session_state.user_name:
        st.error("The name you entered doesn't match the name from the previous page. Please try again.")
    else:
        st.success(f"Hi {name_display}, your resume has been uploaded successfully! Processing data....")

        current_time = time.time()
        elapsed = current_time - st.session_state.upload_time

        if not st.session_state.show_recommendations and elapsed >= 3:
            st.session_state.show_recommendations = True
            st.rerun()

        if st.session_state.show_recommendations:
            # Call resume parsing function
            resume_file = st.session_state.uploaded_file
            parsed_data = parse_resume(resume_file)

            # Extract parsed skills from resume data
            resume_skills = " ".join([skill for skill in parsed_data['skills']])

            # Call job matching function
            job_descriptions = [
                "Data Scientist - Experience in machine learning, Python, and data analysis.",
                "Software Engineer - Expertise in Java, algorithms, and software development.",
                "Product Manager - Strong communication skills, project management, and technical knowledge.",
                "UX Designer - Focus on user experience design, wireframing, and prototyping.",
                "Marketing Specialist - Expertise in digital marketing, SEO, and content creation."
            ]

            # Get job matches from job matcher
            job_matches = match_jobs(resume_skills, job_descriptions)

            st.subheader("Here are the top 5 job recommendations you could pursue based on your uploaded resume:")

            for job, match_percentage in job_matches.items():
                st.write(f"- **{job}** (Match: {match_percentage:.2f}%)")
