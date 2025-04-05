import streamlit as st
from datetime import datetime

def render_sidebar():
    # Apply custom styling to sidebar
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1a1c24;
            border-right: 1px solid #333;
        }
        .sidebar-header {
            margin-bottom: 0;
            color: #ff4b4b;
            font-weight: 600;
        }
        .sidebar-subheader {
            font-size: 0.9rem;
            color: #ccc;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05rem;
        }
        .sidebar-divider {
            margin-top: 1rem;
            margin-bottom: 1rem;
            border-top: 1px solid #333;
        }
        .saved-job-card {
            background-color: #252836;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 3px solid #ff4b4b;
        }
        .job-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: white;
        }
        .job-company {
            font-size: 0.8rem;
            color: #aaa;
            margin-bottom: 5px;
        }
        .remove-btn {
            color: #ff4b4b;
            font-size: 0.7rem;
            cursor: pointer;
            text-align: right;
        }
        .user-profile-box {
            background-color: #252836;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            display: flex;
            align-items: center;
        }
        .user-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #ff4b4b;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Logo and title
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        # Placeholder for logo - replace with actual image when available
        st.markdown("""
        <div style="background-color: #ff4b4b; width: 40px; height: 40px; border-radius: 8px; 
                    display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
            J
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<h1 class="sidebar-header">Jobify</h1>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # User Profile
    st.markdown('<div class="sidebar-subheader">User Profile</div>', unsafe_allow_html=True)
    
    # Login/Signup placeholder
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    
    if not st.session_state.user_logged_in:
        with st.sidebar.expander("Login / Sign Up"):
            tabs = st.tabs(["Login", "Sign Up"])
            
            with tabs[0]:
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                remember_me = st.checkbox("Remember me")
                
                if st.button("Login", use_container_width=True):
                    # Implement actual authentication here
                    if username and password:  # Simple validation
                        st.session_state.user_logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.experimental_rerun()
                    else:
                        st.error("Please enter both username and password")
                
                st.markdown('<div style="text-align: center; margin-top: 10px;">'
                           '<a href="#" style="color: #ff4b4b; font-size: 0.8rem;">Forgot password?</a>'
                           '</div>', unsafe_allow_html=True)
            
            with tabs[1]:
                new_username = st.text_input("Username", key="signup_username")
                email = st.text_input("Email", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
                
                terms = st.checkbox("I agree to the Terms of Service")
                
                if st.button("Create Account", use_container_width=True):
                    # Implement registration here
                    if new_username and email and new_password and new_password == confirm_password and terms:
                        st.session_state.user_logged_in = True
                        st.session_state.username = new_username
                        st.success("Account created successfully!")
                        st.experimental_rerun()
                    elif not terms:
                        st.error("Please agree to the Terms of Service")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        st.error("Please fill in all fields")
    else:
        # User profile display when logged in
        st.markdown(f"""
        <div class="user-profile-box">
            <div class="user-avatar">{st.session_state.username[0].upper()}</div>
            <div>
                <div style="font-weight: bold;">{st.session_state.username}</div>
                <div style="font-size: 0.7rem; color: #aaa;">Free Plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("My Profile", use_container_width=True):
                # Navigate to profile page
                pass
        with col2:
            if st.button("Logout", use_container_width=True):
                st.session_state.user_logged_in = False
                st.session_state.pop("username", None)
                st.experimental_rerun()
    
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Saved Jobs
    st.markdown('<div class="sidebar-subheader">Saved Jobs</div>', unsafe_allow_html=True)
    
    # Get saved jobs from session state or initialize empty list
    saved_jobs = st.session_state.get("saved_jobs", [])
    
    if saved_jobs:
        # Add a search box for saved jobs
        search_saved = st.sidebar.text_input("Search saved jobs", placeholder="Search by title or company...")
        
        # Filter jobs based on search
        filtered_jobs = saved_jobs
        if search_saved:
            filtered_jobs = [job for job in saved_jobs if 
                            search_saved.lower() in job.get('title', '').lower() or 
                            search_saved.lower() in job.get('company', '').lower()]
        
        # Display saved jobs count
        st.sidebar.markdown(f"<div style='font-size: 0.8rem; color: #aaa; margin-bottom: 10px;'>{len(filtered_jobs)} job(s) saved</div>", unsafe_allow_html=True)
        
        # Display saved jobs
        for i, job in enumerate(filtered_jobs):
            st.sidebar.markdown(f"""
            <div class="saved-job-card">
                <div class="job-title">{job.get('title', 'Job Title')}</div>
                <div class="job-company">{job.get('company', 'Company')} | {job.get('location', 'Location')}</div>
                <div class="job-company">Saved on: {job.get('saved_date', datetime.now().strftime('%Y-%m-%d'))}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                if st.button("View", key=f"view_{i}", use_container_width=True):
                    # Implement view job details
                    st.session_state.selected_job = job
            with col2:
                if st.button("✕", key=f"remove_{i}", use_container_width=True):
                    saved_jobs.pop(i)
                    st.session_state.saved_jobs = saved_jobs
                    st.experimental_rerun()
    else:
        st.sidebar.markdown("""
        <div style="background-color: #252836; border-radius: 5px; padding: 15px; text-align: center;">
            <div style="color: #aaa; margin-bottom: 10px;">No saved jobs yet</div>
            <div style="font-size: 0.8rem; color: #777;">Jobs you save will appear here for easy access</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Settings
    st.markdown('<div class="sidebar-subheader">Settings</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("Application Settings", expanded=False):
        st.checkbox("Dark Mode", value=True, key="dark_mode", 
                   help="Toggle between light and dark theme")
        
        st.selectbox("Job Match Algorithm", 
                    ["TF-IDF + Cosine Similarity", "Word2Vec", "BERT Embeddings"],
                    key="match_algorithm",
                    help="Algorithm used to match your resume with job listings")
        
        st.slider("Results per page", 5, 50, 10, key="results_per_page",
                 help="Number of job results to display per page")
        
        st.checkbox("Auto-save searches", value=True, key="auto_save_searches",
                   help="Automatically save your search history")
        
        st.checkbox("Email notifications", value=False, key="email_notifications",
                   help="Receive email notifications for new job matches")
    
    # App info at the bottom
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 0.7rem; color: #666;">
        Jobify v1.0.0<br>
        © 2025 Jobify Inc.
    </div>
    """, unsafe_allow_html=True)