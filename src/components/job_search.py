# src/components/job_search.py
import streamlit as st
import pandas as pd
from utils.linkedin_api import LinkedInJobsAPI

def render_job_search(job_matcher, resume_data):
    st.header("Job Search")
    
    # Initialize LinkedIn API
    linkedin_api = LinkedInJobsAPI()
    
    # Extract skills from resume
    skills = resume_data.get("skills", [])
    skill_keywords = ", ".join(skills[:5])  # Use top 5 skills as default keywords
    
    # Search options
    col1, col2 = st.columns(2)
    
    with col1:
        keywords = st.text_area("Search Keywords", value=skill_keywords, 
                               help="Enter keywords separated by commas")
    
    with col2:
        location = st.text_input("Location", value="", 
                                help="Enter city, state, or country")
        
    num_results = st.slider("Number of Results", min_value=5, max_value=50, value=20)
    
    # Search button
    if st.button("Search Jobs"):
        with st.spinner("Searching for jobs..."):
            # Search for jobs using LinkedIn API
            job_results = linkedin_api.search_jobs(keywords, location, num_results)
            
            if job_results:
                st.success(f"Found {len(job_results)} jobs matching your criteria.")
                
                # Preprocess job descriptions for matching
                job_matcher.preprocess_job_descriptions(job_results)
                
                # Match resume with job descriptions
                job_matches = job_matcher.match_resume(resume_data)
                
                # Display matches summary
                st.subheader("Job Matches")
                st.info(f"Found {len(job_matches)} matches. Results are sorted by relevance to your resume.")
                
                return job_matches
            else:
                st.error("No jobs found. Please try different keywords or location.")
                return None
    
    return None
