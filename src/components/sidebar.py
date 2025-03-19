# src/components/sidebar.py
import streamlit as st

def render_sidebar():
    st.sidebar.title("Jobify")
    st.sidebar.image("path/to/logo.png", width=100)  # Add your logo here
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("User Profile")
    
    # Login/Signup placeholder
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    
    if not st.session_state.user_logged_in:
        with st.sidebar.expander("Login / Sign Up"):
            # Simple login form (for demo purposes)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login"):
                    # Implement actual authentication here
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()
            with col2:
                if st.button("Sign Up"):
                    # Implement registration here
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("Logout"):
            st.session_state.user_logged_in = False
            st.session_state.pop("username", None)
            st.experimental_rerun()
    
    st.sidebar.markdown("---")
    
    # Saved Jobs
    st.sidebar.subheader("Saved Jobs")
    saved_jobs = st.session_state.get("saved_jobs", [])
    if saved_jobs:
        for i, job in enumerate(saved_jobs):
            with st.sidebar.container():
                st.write(f"**{job.get('title')}**")
                st.write(f"{job.get('company')} | {job.get('location')}")
                if st.button("Remove", key=f"remove_{i}"):
                    saved_jobs.pop(i)
                    st.experimental_rerun()
    else:
        st.sidebar.info("No saved jobs yet.")
    
    st.sidebar.markdown("---")
    
    # Settings
    with st.sidebar.expander("Settings"):
        st.checkbox("Dark Mode", key="dark_mode")
        st.selectbox("Job Match Algorithm", 
                    ["TF-IDF + Cosine Similarity", "Word2Vec", "BERT Embeddings"],
                    key="match_algorithm")
        st.slider("Results per page", 5, 50, 10, key="results_per_page")
