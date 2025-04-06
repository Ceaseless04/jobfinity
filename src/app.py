import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image
import io
import base64

# Page configuration with improved styling
st.set_page_config(
    page_title="Jobify - AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Add the project root directory to Python path
# This allows importing modules from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components and models

from components.resume_uploader import render_resume_uploader
from components.job_search import render_job_search
from components.results_display import render_results
from models.resume_parser import ResumeParser
from models.job_matcher import JobMatcher

# Custom CSS for modern dark theme UI
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main theme colors and variables */
        :root {
            --primary: #ff4b4b;
            --primary-hover: #ff3333;
            --secondary: #4fd1c5;
            --secondary-hover: #3db1a8;
            --dark-bg: #0e1117;
            --card-bg: #1e2130;
            --nav-bg: #1e1e1e;
            --border: #333;
            --text: #e0e0e0;
            --text-muted: #a0a0a0;
        }
                

        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }

        
        /* Base styles */
        .main {
            background-color: var(--dark-bg);
            color: var(--text);
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Navigation bar styling */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: var(--nav-bg);
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .nav-links {
            display: flex;
            gap: 20px;
        }
        
        .nav-link {
            color: var(--text);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            padding: 8px 12px;
            border-radius: 4px;
        }
        
        .nav-link:hover {
            color: var(--secondary);
            background-color: rgba(79, 209, 197, 0.1);
        }
        
        .nav-link.active {
            color: var(--secondary);
            border-bottom: 2px solid var(--secondary);
        }
        
        .profile-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .login-btn {
            background-color: transparent;
            color: var(--secondary);
            border: 1px solid var(--secondary);
            border-radius: 4px;
            padding: 8px 15px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .login-btn:hover {
            background-color: var(--secondary);
            color: var(--dark-bg);
        }
        
        .profile-btn {
            background-color: var(--secondary);
            color: var(--dark-bg);
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .profile-btn:hover {
            background-color: var(--secondary-hover);
        }
        
        /* File upload area styling */
        .upload-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 2px dashed #4a4a4a;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            background-color: rgba(30, 33, 48, 0.7);
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        
        .upload-container:hover {
            border-color: var(--secondary);
            background-color: rgba(30, 33, 48, 0.9);
            transform: translateY(-2px);
        }
        
        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
            color: var(--secondary);
        }
        
        .upload-text {
            margin-bottom: 15px;
            font-size: 18px;
            font-weight: 600;
        }
        
        .file-size-text {
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .browse-btn {
            background-color: var(--secondary);
            color: var(--dark-bg);
            border: none;
            border-radius: 6px;
            padding: 10px 24px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .browse-btn:hover {
            background-color: var(--secondary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }
        
        /* File list styling */
        .file-list {
            margin-top: 30px;
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid var(--border);
            transition: background-color 0.2s;
        }
        
        .file-item:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .file-item:last-child {
            border-bottom: none;
        }
        
        .file-name {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
        }
        
        .file-info {
            color: var(--text-muted);
            font-size: 14px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: var(--nav-bg);
            border-radius: 8px;
            padding: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border: none;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 75, 75, 0.15);
            border-radius: 6px;
            color: var(--primary);
            font-weight: 600;
        }
        
        /* Card styling */
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Message boxes */
        .warning-box {
            background-color: rgba(255, 214, 10, 0.1);
            border-left: 4px solid #ffd60a;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .success-box {
            background-color: rgba(75, 181, 67, 0.1);
            border-left: 4px solid #4bb543;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .info-box {
            background-color: rgba(33, 150, 243, 0.1);
            border-left: 4px solid #2196f3;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        /* Header styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo-text {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--primary), #ff8f8f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
            margin-bottom: 8px;
        }
        
        /* Metric cards */
        .metric-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            flex: 1;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .metric-label {
            font-size: 1rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton>button:hover {
            background-color: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }
        
        /* Progress bar */
        .progress-container {
            margin-bottom: 15px;
        }
        
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .progress-bar {
            height: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), #ff8f8f);
            border-radius: 4px;
        }
        
        /* Skill tags */
        .skill-tag {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 6px 12px;
            margin-right: 8px;
            margin-bottom: 8px;
            display: inline-block;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        
        .skill-tag:hover {
            background-color: rgba(79, 209, 197, 0.2);
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

# Navigation bar component
def render_navbar(is_logged_in=False, username="User"):
    navbar_html = f"""
    <div class="navbar">
        <div class="nav-links">
            <a href="#" class="nav-link active">Home</a>
            <a href="#" class="nav-link">Dashboard</a>
            <a href="#" class="nav-link">Files</a>
            <a href="#" class="nav-link">Settings</a>
        </div>
        <div class="profile-section">
            {"<button class='profile-btn'>" + username + "</button>" if is_logged_in else "<button class='login-btn'>Login</button>"}
        </div>
    </div>
    """
    st.markdown(navbar_html, unsafe_allow_html=True)

# File upload area component
def render_file_upload_area():
    upload_html = """
    <div class="upload-container">
        <div class="upload-icon">⬆️</div>
        <div class="upload-text">Drag & Drop Your Resume</div>
        <div class="file-size-text">Supported formats: PDF, DOCX, TXT • Max size: 10MB</div>
        <button class="browse-btn" onclick="document.getElementById('file_uploader').click()">Browse Files</button>
    </div>
    """
    st.markdown(upload_html, unsafe_allow_html=True)
    
    # Hidden file uploader that will be triggered by the button
    uploaded_files = st.file_uploader("", type=["pdf", "docx", "txt"], accept_multiple_files=False, key="file_uploader", label_visibility="collapsed")
    
    return uploaded_files

# Display uploaded files
def display_files(files):
    if not files:
        return
    
    if isinstance(files, list):
        file_list = files
    else:
        file_list = [files]
    
    st.markdown("<div class='file-list'>", unsafe_allow_html=True)
    
    for file in file_list:
        file_size = len(file.getvalue())
        size_str = format_file_size(file_size)
        
        file_icon = get_file_icon(file.name)
        
        file_item_html = f"""
        <div class="file-item">
            <div class="file-name">
                {file_icon} {file.name}
            </div>
            <div class="file-info">
                {size_str}
            </div>
        </div>
        """
        st.markdown(file_item_html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Helper function to format file size
def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

# Helper function to get file icon based on extension
def get_file_icon(filename):
    extension = filename.split('.')[-1].lower() if '.' in filename else ''
    
    icons = {
        'pdf': '📄',
        'doc': '📝',
        'docx': '📝',
        'txt': '📄',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'gif': '🖼️',
        'mp3': '🎵',
        'mp4': '🎬',
        'zip': '📦',
        'rar': '📦',
        'xls': '📊',
        'xlsx': '📊',
        'ppt': '📊',
        'pptx': '📊',
    }
    
    return icons.get(extension, '📁')

# Initialize session state
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = "User"
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

def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Render navigation bar
   
    
    # Header with logo and title
    st.markdown(
        """
        <div class="header-container" style="justify-content: center; text-align: center;" >
            <div>
                <div class="logo-text">Jobify</div>
                <p style="font-size: 1.2rem; margin-top: -5px;">AI Resume Analyzer</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <p style="font-size: 1.1rem; margin-bottom: 30px; text-align: center; ">
    Upload your resume and get personalized job recommendations based on your skills and experience.
    </p>
    """, unsafe_allow_html=True)
    
    # Render sidebar with options
  
    
    # Create tabs for different sections
    tab_labels = ["Upload Resume", "Job Search", "Results"]
    tab1, tab2, tab3 = st.tabs(tab_labels)
    
    # Set the active tab based on session state
    tabs = [tab1, tab2, tab3]
    active_tab = tabs[st.session_state.active_tab]
    
    with tab1:
        if st.session_state.active_tab == 0:
            st.markdown("""
            <div style="text-align: center;">
                <h2>Upload Your Resume</h2>
                <p>Choose a resume file to analyze.</p>
            </div>
        """, unsafe_allow_html=True)
            
            # Instead of using the component, we'll implement it directly
            resume_parser = ResumeParser()
            
            # Upload resume
            uploaded_file = render_file_upload_area()
            
            if uploaded_file:
                display_files(uploaded_file)
                
                # Analyze button with processing animation
                analyze_btn = st.button("Analyze Resume", use_container_width=True)
                
                if analyze_btn:
                    with st.spinner("Analyzing your resume..."):
                        # Simulate processing time
                        import time
                        time.sleep(2)
                        
                        # Process the resume (this would normally call resume_parser.parse())
                        # For demo purposes, we'll create sample data
                        resume_data = {
                            'name': 'John Smith',
                            'email': 'john.smith@example.com',
                            'phone': '(123) 456-7890',
                            'skills': ['Python', 'Data Analysis', 'Machine Learning', 'SQL', 'JavaScript', 'React', 'Project Management'],
                            'experience': [
                                {'title': 'Data Scientist', 'company': 'TechCorp', 'duration': '2019-2022'},
                                {'title': 'Data Analyst', 'company': 'DataFirm', 'duration': '2017-2019'}
                            ],
                            'education': [
                                {'degree': 'M.S. Computer Science', 'institution': 'State University', 'year': '2017'},
                                {'degree': 'B.S. Statistics', 'institution': 'City College', 'year': '2015'}
                            ],
                            'experience_years': 5
                        }
                        
                        st.session_state.resume_data = resume_data
                        st.session_state.analysis_complete = True
                
                # Show result if analysis is complete
                if st.session_state.analysis_complete:
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
                    if st.session_state.resume_data:
                        st.subheader("Resume Analysis Summary")
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(
                                """
                                <div class="metric-card">
                                    <div class="metric-value" style="color: #4bb543;">
                                """ + str(len(st.session_state.resume_data.get('skills', []))) + """
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
                                """ + str(st.session_state.resume_data.get('experience_years', 0)) + """
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
                                """ + str(len(st.session_state.resume_data.get('education', []))) + """
                                    </div>
                                    <div class="metric-label">Education Entries</div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                        
                        # Display skills
                        st.subheader("Skills")
                        skills_html = "<div style='margin-bottom: 20px;'>"
                        for skill in st.session_state.resume_data.get('skills', []):
                            skills_html += f"<span class='skill-tag'>{skill}</span>"
                        skills_html += "</div>"
                        st.markdown(skills_html, unsafe_allow_html=True)
                    
                    st.button("Proceed to Job Search", on_click=change_tab, args=(1,), use_container_width=True)
    
    with tab2:
        if st.session_state.active_tab == 1:
            if st.session_state.resume_data:
                st.subheader("Find Matching Jobs")
                
                # Job search form
                col1, col2 = st.columns(2)
                with col1:
                    job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist")
                with col2:
                    location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Remote", "All"])
                with col2:
                    experience_level = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior", "All"])
                with col3:
                    salary_range = st.selectbox("Salary Range", ["$0-50k", "$50-100k", "$100-150k", "150k+", "All"])
                
                # Search button
                search_btn = st.button("Find Matching Jobs", use_container_width=True)
                
                if search_btn:
                    with st.spinner("Searching for matching jobs..."):
                        # Simulate processing time
                        import time
                        time.sleep(2)
                        
                        # Process the job search (this would normally call job_matcher.find_matches())
                        # For demo purposes, we'll create sample data
                        job_matches = [
                            {
                                'title': 'Senior Data Scientist',
                                'company': 'Tech Innovations Inc.',
                                'location': 'San Francisco, CA',
                                'type': 'Full-time',
                                'salary': '$120,000 - $150,000',
                                'description': 'We are looking for an experienced Data Scientist to join our growing team...',
                                'requirements': ['Python', 'Machine Learning', 'SQL', 'Data Visualization', 'Statistics'],
                                'match_score': 92
                            },
                            {
                                'title': 'Data Scientist',
                                'company': 'AI Solutions',
                                'location': 'Remote',
                                'type': 'Full-time',
                                'salary': '$100,000 - $130,000',
                                'description': 'Join our team to work on cutting-edge machine learning models...',
                                'requirements': ['Python', 'Deep Learning', 'TensorFlow', 'SQL'],
                                'match_score': 87
                            },
                            {
                                'title': 'Machine Learning Engineer',
                                'company': 'DataCorp',
                                'location': 'New York, NY',
                                'type': 'Full-time',
                                'salary': '$110,000 - $140,000',
                                'description': 'Looking for talented ML engineers to develop and deploy models...',
                                'requirements': ['Python', 'Machine Learning', 'Cloud platforms', 'CI/CD'],
                                'match_score': 85
                            },
                            {
                                'title': 'Data Analyst',
                                'company': 'Finance Tech',
                                'location': 'Chicago, IL',
                                'type': 'Full-time',
                                'salary': '$80,000 - $100,000',
                                'description': 'Work with our finance team to analyze complex datasets...',
                                'requirements': ['SQL', 'Data Analysis', 'Excel', 'Tableau'],
                                'match_score': 78
                            },
                            {
                                'title': 'Business Intelligence Analyst',
                                'company': 'Retail Solutions',
                                'location': 'Seattle, WA',
                                'type': 'Full-time',
                                'salary': '$90,000 - $110,000',
                                'description': 'Help our clients make data-driven decisions with powerful BI solutions...',
                                'requirements': ['SQL', 'Power BI', 'Data Warehousing'],
                                'match_score': 75
                            }
                        ]
                        
                        st.session_state.job_matches = job_matches
                        st.session_state.search_complete = True
                
                # Show results if search is complete
                if st.session_state.search_complete:
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
                    if st.session_state.job_matches and len(st.session_state.job_matches) > 0:
                        st.subheader(f"Found {len(st.session_state.job_matches)} matching jobs")
                        
                        # Display top 3 matches
                        for i, job in enumerate(st.session_state.job_matches[:3]):
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
                                            <p style="font-size: 1.2rem; font-weight: 700; color: {match_color};">{match_score}% Match</p>
                                        </div>
                                    </div>
                                    
                                    <div style="margin: 15px 0;">
                                        <p>{job.get('description', '')}</p>
                                    </div>
                                    
                                    <div style="margin-top: 15px;">
                                        <p style="font-weight: 600; margin-bottom: 10px;">Required Skills:</p>
                                        <div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            # Display skills as tags
                            skills_html = ""
                            for skill in job.get('requirements', []):
                                skills_html += f"<span class='skill-tag'>{skill}</span>"
                            
                            st.markdown(skills_html, unsafe_allow_html=True)
                            
                            # Job details and apply button
                            st.markdown(
                                f"""
                                        </div>
                                    </div>
                                    
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                                        <div>
                                            <p style="color: #aaa;">{job.get('type', 'Full-time')} • {job.get('salary', 'Salary not specified')}</p>
                                        </div>
                                        <div>
                                            <button class="browse-btn" onclick="alert('Application feature coming soon!')">Apply Now</button>
                                        </div>
                                    </div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                        
                        # Button to view all results
                        st.button("View All Results", on_click=change_tab, args=(2,), use_container_width=True)
            else:
                # If no resume data, show warning
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
            if st.session_state.job_matches and len(st.session_state.job_matches) > 0:
                st.subheader("Your Job Matches")
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                with col1:
                    match_filter = st.selectbox("Match Score", ["All", "90%+", "80%+", "70%+"])
                with col2:
                    location_filter = st.selectbox("Location", ["All", "Remote", "San Francisco", "New York", "Chicago", "Seattle"])
                with col3:
                    job_type_filter = st.selectbox("Job Type", ["All", "Full-time", "Part-time", "Contract"])
                
                # Display all job matches
                for i, job in enumerate(st.session_state.job_matches):
                    match_score = job.get('match_score', 0)
                    match_color = '#ff4b4b' if match_score > 85 else '#ff9d4b' if match_score > 70 else '#ffce4b'
                    
                    # Create an expander for each job
                    with st.expander(f"{job.get('title', 'Job Title')} - {job.get('company', 'Company')} ({match_score}% Match)", expanded=i==0):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {job.get('title', 'Job Title')}")
                            st.markdown(f"**{job.get('company', 'Company')}** • {job.get('location', 'Location')}")
                            st.markdown(f"**Type:** {job.get('type', 'Full-time')} • **Salary:** {job.get('salary', 'Not specified')}")
                            
                            st.markdown("### Description")
                            st.write(job.get('description', 'No description available.'))
                            
                            st.markdown("### Required Skills")
                            skills_html = "<div style='margin-bottom: 20px;'>"
                            for skill in job.get('requirements', []):
                                skills_html += f"<span class='skill-tag'>{skill}</span>"
                            skills_html += "</div>"
                            st.markdown(skills_html, unsafe_allow_html=True)
                        
                        with col2:
                            # Match score visualization
                            st.markdown(
                                f"""
                                <div style="background-color: var(--card-bg); padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                                    <h4 style="margin-bottom: 10px;">Match Score</h4>
                                    <div style="font-size: 2.5rem; font-weight: 700; color: {match_color};">{match_score}%</div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            # Action buttons
                            st.button("Apply Now", key=f"apply_{i}", use_container_width=True)
                            
                            # Save job button
                            if st.button("Save Job", key=f"save_{i}", use_container_width=True):
                                if save_job(job):
                                    st.success("Job saved successfully!")
                                else:
                                    st.info("This job is already saved.")
                            
                            # Share button
                            st.button("Share", key=f"share_{i}", use_container_width=True)
            
            elif st.session_state.resume_data:
                # If resume data exists but no job matches
                st.markdown(
                    """
                    <div class="info-box">
                        <h3>No Job Matches Yet</h3>
                        <p>Please go to the Job Search tab to find matching jobs based on your resume.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                st.button("Go to Job Search", on_click=change_tab, args=(1,), use_container_width=True)
            else:
                # If no resume data
                st.markdown(
                    """
                    <div class="warning-box">
                        <h3>Resume Required</h3>
                        <p>Please upload and analyze your resume first before viewing job matches.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                st.button("Go to Resume Upload", on_click=change_tab, args=(0,), use_container_width=True)

# Run the main function
if __name__ == "__main__":
    main()