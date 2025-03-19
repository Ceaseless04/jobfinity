# src/components/results_display.py
import streamlit as st
import pandas as pd
import plotly.express as px

def render_results(job_matches):
    st.header("Job Match Results")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["List View", "Analytics"])
    
    with tab1:
        # Display job matches in a list
        for i, job in enumerate(job_matches):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(job.get("title", "Untitled Position"))
                    st.write(f"**Company:** {job.get('company', 'N/A')}")
                    st.write(f"**Location:** {job.get('location', 'N/A')}")
                    
                    # Truncate description
                    description = job.get("description", "")
                    max_chars = 300
                    truncated_desc = description[:max_chars] + "..." if len(description) > max_chars else description
                    st.write(truncated_desc)
                    
                    # Show job link
                    st.markdown(f"[View on LinkedIn]({job.get('url', '#')})")
                
                with col2:
                    # Display match score
                    match_score = job.get("similarity_score", 0) * 100
                    st.metric("Match Score", f"{match_score:.1f}%")
                    
                    # Add to favorites button
                    if st.button("Save", key=f"save_{i}"):
                        st.session_state.setdefault("saved_jobs", []).append(job)
                        st.success("Job saved!")
            
            st.divider()
    
    with tab2:
        # Display analytics based on job matches
        st.subheader("Job Match Analytics")
        
        # Calculate average match score
        average_score = sum(job.get("similarity_score", 0) for job in job_matches) / len(job_matches) * 100
        st.metric("Average Match Score", f"{average_score:.1f}%")
        
        # Create dataframe for visualization
        df = pd.DataFrame([{
            "title": job.get("title", "Untitled"),
            "company": job.get("company", "N/A"),
            "match_score": job.get("similarity_score", 0) * 100,
            "location": job.get("location", "N/A"),
            "date_posted": job.get("date_posted", "")
        } for job in job_matches])
        
        # Plot match scores
        fig1 = px.bar(df.head(10), x="title", y="match_score", color="match_score",
                     title="Top 10 Job Matches by Score",
                     labels={"title": "Job Title", "match_score": "Match Score (%)"},
                     color_continuous_scale="blues")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Plot jobs by location
        location_counts = df["location"].value_counts().reset_index()
        location_counts.columns = ["location", "count"]
        fig2 = px.pie(location_counts, values="count", names="location", 
                     title="Jobs by Location")
        st.plotly_chart(fig2, use_container_width=True)
