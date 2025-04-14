# src/app.py
import sys
import os
import streamlit as st
from components.resume_uploader import render_resume_uploader
from components.results_display import render_results

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.resume_parser import ResumeParser
from models.job_matcher import JobMatcher
from models.career_path import CareerPathRecommender
from utils.adzuna_api import AdzunaJobsAPI

def main():
    st.set_page_config(
        page_title="Jobfinity - AI Resume Matcher",
        page_icon="📄",
        layout="wide"
    )

    st.title("Jobfinity - AI Resume Matcher")
    st.markdown("""
    Upload your tech resume and get job recommendations with personalized career path suggestions.
    """)

    # Initialize session state
    st.session_state.setdefault('resume_data', None)
    st.session_state.setdefault('job_matches', None)
    st.session_state.setdefault('career_recommendations', None)
    st.session_state.setdefault('active_tab', 'Upload Resume')

    # Tabs with index management
    tab_labels = ["Upload Resume", "Matched Jobs"]
    tab_index = tab_labels.index(st.session_state.active_tab)
    tab1, tab2 = st.tabs(tab_labels)

    # Resume Upload Tab
    with tab1:
        resume_parser = ResumeParser()
        resume_data = render_resume_uploader(resume_parser)

        # If resume was successfully parsed, trigger redirect
        if resume_data:
            st.session_state.resume_data = resume_data
            st.session_state.active_tab = "Matched Jobs"
            st.experimental_rerun()

    # Matched Jobs Tab
    with tab2:
        if st.session_state.resume_data:
            with st.spinner("Fetching and matching jobs from Adzuna API..."):
                adzuna_api = AdzunaJobsAPI()
                jobs = adzuna_api.search_jobs('US', limit=100)

                if jobs:
                    job_matcher = JobMatcher()
                    print("DEBUG: Resume Data:", st.session_state.resume_data)
                    try:
                        job_matcher.preprocess_job_descriptions(jobs)
                        st.session_state.job_matches = job_matcher.match_resume(st.session_state.resume_data)[:20]

                        recommender = CareerPathRecommender(jobs)
                        st.session_state.career_recommendations = recommender.recommend_career_paths(st.session_state.resume_data)
                    except ValueError as e:
                        st.error(f"Matching error: {str(e)}")
                else:
                    st.warning("No jobs fetched from Adzuna API.")

            render_results(st.session_state.job_matches, st.session_state.career_recommendations)
        else:
            st.warning("Please upload and parse your resume first.")

if __name__ == "__main__":
    main()
