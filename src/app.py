# src/app.py
import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.resume_uploader import render_resume_uploader
from components.job_search import render_job_search
from components.results_display import render_results
from models.resume_parser import ResumeParser
from models.job_matcher import JobMatcher
from database.db_connector import DatabaseConnector

def main():
    st.set_page_config(
        page_title="Jobify - AI Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("Jobify - AI Resume Analyzer")
    st.markdown("""
    Upload your resume and get personalized job recommendations based on your skills and experience.
    """)
    
    # Initialize session state variables if not already present
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'job_matches' not in st.session_state:
        st.session_state.job_matches = None
    
    # Render sidebar with options
    render_sidebar()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Upload Resume", "Job Search", "Results"])
    
    with tab1:
        resume_parser = ResumeParser()
        st.session_state.resume_data = render_resume_uploader(resume_parser)
    
    with tab2:
        if st.session_state.resume_data:
            job_matcher = JobMatcher()
            st.session_state.job_matches = render_job_search(job_matcher, st.session_state.resume_data)
        else:
            st.warning("Please upload and parse your resume first.")
    
    with tab3:
        if st.session_state.job_matches:
            render_results(st.session_state.job_matches)
        else:
            st.warning("No job matches available. Please complete the previous steps.")

if __name__ == "__main__":
    main()
