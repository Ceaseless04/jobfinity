import streamlit as st
import pandas as pd
import os
import sys

# Add the project root directory to Python path
# This allows importing modules from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your components and models
from components.sidebar import render_sidebar
from components.resume_uploader import render_resume_uploader
from components.job_search import render_job_search
from components.results_display import render_results
from models.resume_parser import ResumeParser
from models.job_matcher import JobMatcher


def main():
    # Page configuration with improved styling
    st.set_page_config(
        page_title="Jobify - AI Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            border-bottom: 1px solid #333;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            border-bottom: 2px solid #ff4b4b !important;
            color: white;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #ff3333;
        }
        .card {
            background-color: #1e2130;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #333;
        }
        .warning-box {
            background-color: rgba(255, 214, 10, 0.1);
            border-left: 4px solid #ffd60a;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .logo-text {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(90deg, #ff4b4b, #ff8f8f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .success-box {
            background-color: rgba(75, 181, 67, 0.1);
            border-left: 4px solid #4bb543;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .info-box {
            background-color: rgba(33, 150, 243, 0.1);
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .metric-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #1e2130;
            border-radius: 8px;
            padding: 20px;
            flex: 1;
            text-align: center;
            border: 1px solid #333;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #aaa;
        }
        .progress-container {
            margin-bottom: 15px;
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        .progress-bar {
            height: 8px;
            background-color: #2c3142;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background-color: #ff4b4b;
        }
        .skill-tag {
            background-color: #2c3142;
            border-radius: 15px;
            padding: 5px 10px;
            margin-right: 5px;
            margin-bottom: 5px;
            display: inline-block;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with logo and title
    st.markdown(
        """
        <div class="header-container">
            <div>
                <div class="logo-text">Jobify</div>
                <p>AI Resume Analyzer</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <p style="font-size: 1.1rem; margin-bottom: 30px;">
    Upload your resume and get personalized job recommendations based on your skills and experience.
    </p>
    """, unsafe_allow_html=True)
    
    # Initialize session state variables if not already present
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'job_matches' not in st.session_state:
        st.session_state.job_matches = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0
    if 'saved_jobs' not in st.session_state:
        st.session_state.saved_jobs = []
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'search_complete' not in st.session_state:
        st.session_state.search_complete = False
    
    # Function to change tab
    def change_tab(tab_index):
        st.session_state.active_tab = tab_index
    
    # Function to save a job
    def save_job(job):
        if 'saved_jobs' not in st.session_state:
            st.session_state.saved_jobs = []
        
        # Add current date to job
        from datetime import datetime
        job['saved_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Check if job is already saved
        job_titles = [j.get('title') for j in st.session_state.saved_jobs]
        if job.get('title') not in job_titles:
            st.session_state.saved_jobs.append(job)
            return True
        return False
    
    # Render sidebar with options
    render_sidebar()
    
    # Create tabs for different sections
    tab_labels = ["Upload Resume", "Job Search", "Results"]
    tab1, tab2, tab3 = st.tabs(tab_labels)
    
    # Set the active tab based on session state
    tabs = [tab1, tab2, tab3]
    active_tab = tabs[st.session_state.active_tab]
    
    with tab1:
        if st.session_state.active_tab == 0:
            resume_parser = ResumeParser()
            resume_data = render_resume_uploader(resume_parser)
            
            if resume_data and (st.session_state.resume_data is None or resume_data != st.session_state.resume_data):
                st.session_state.resume_data = resume_data
                st.session_state.analysis_complete = True
                
                st.markdown(
                    """
                    <div class="success-box">
                        <h3>Resume Analysis Complete!</h3>
                        <p>Your resume has been successfully analyzed. You can now proceed to the Job Search tab to find matching jobs.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Display a summary of the resume analysis
                if resume_data:
                    st.subheader("Resume Analysis Summary")
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-value" style="color: #4bb543;">
                                """ + str(len(resume_data.get('skills', []))) + """
                                </div>
                                <div class="metric-label">Skills Identified</div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-value" style="color: #ff4b4b;">
                                """ + str(resume_data.get('experience_years', 0)) + """
                                </div>
                                <div class="metric-label">Years Experience</div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-value" style="color: #2196f3;">
                                """ + str(len(resume_data.get('education', []))) + """
                                </div>
                                <div class="metric-label">Education Entries</div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                
                st.button("Proceed to Job Search", on_click=change_tab, args=(1,), use_container_width=True)
    
    with tab2:
        if st.session_state.active_tab == 1:
            if st.session_state.resume_data:
                job_matcher = JobMatcher()
                job_matches = render_job_search(job_matcher, st.session_state.resume_data)
                
                if job_matches and (st.session_state.job_matches is None or job_matches != st.session_state.job_matches):
                    st.session_state.job_matches = job_matches
                    st.session_state.search_complete = True
                    
                    st.markdown(
                        """
                        <div class="success-box">
                            <h3>Job Matching Complete!</h3>
                            <p>We've found jobs that match your skills and experience. View your personalized results now.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Preview of top matches
                    if job_matches and len(job_matches) > 0:
                        st.subheader(f"Found {len(job_matches)} matching jobs")
                        
                        # Display top 3 matches
                        for i, job in enumerate(job_matches[:3]):
                            match_score = job.get('match_score', 0)
                            match_color = '#ff4b4b' if match_score > 85 else '#ff9d4b' if match_score > 70 else '#ffce4b'
                            
                            st.markdown(
                                f"""
                                <div class="card">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                        <div>
                                            <h3>{job.get('title', 'Job Title')}</h3>
                                            <p style="color: #aaa; margin-top: 5px;">{job.get('company', 'Company')} • {job.get('location', 'Location')}</p>
                                        </div>
                                        <div style="text-align: right;">
                                            <p style="color: {match_color}; font-weight: bold;">{match_score}% Match</p>
                                        </div>
                                    </div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                    
                    st.button("View Detailed Results", on_click=change_tab, args=(2,), use_container_width=True)
            else:
                st.markdown(
                    """
                    <div class="warning-box">
                        <h3>Resume Required</h3>
                        <p>Please upload and analyze your resume first before searching for jobs.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.button("Go to Resume Upload", on_click=change_tab, args=(0,), use_container_width=True)
    
    with tab3:
        if st.session_state.active_tab == 2:
            if st.session_state.job_matches:
                # Add save_job function to the render_results call
                render_results(st.session_state.job_matches, save_job_func=save_job)
            else:
                st.markdown(
                    """
                    <div class="warning-box">
                        <h3>No Job Matches Available</h3>
                        <p>Please complete the previous steps to view your job matches.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.session_state.resume_data:
                    st.button("Go to Job Search", on_click=change_tab, args=(1,), use_container_width=True)
                else:
                    st.button("Start from Beginning", on_click=change_tab, args=(0,), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            © 2025 Jobify | AI-Powered Resume Analysis | Made with ❤️ for job seekers
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()