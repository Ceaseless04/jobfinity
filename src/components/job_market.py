# src/components/job_market_insights.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_job_market_insights(job_matches, resume_data):
    st.title("Job Market Insights")
    
    # Extract skills from resume
    user_skills = set([skill.lower() for skill in resume_data.get("skills", [])])
    
    # Extract data from job matches
    job_data = []
    skill_mentions = {}
    locations = []
    
    for job in job_matches:
        # Add job data
        job_data.append({
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", ""),
            "match_score": job.get("similarity_score", 0) * 100
        })
        
        # Count skill mentions
        description = job.get("description", "").lower()
        for skill in user_skills:
            if skill in description:
                skill_mentions[skill] = skill_mentions.get(skill, 0) + 1
        
        # Add location
        location = job.get("location", "")
        if location:
            locations.append(location)
    
    # Create DataFrame
    df = pd.DataFrame(job_data)
    
    # Display insights in tabs
    tab1, tab2, tab3 = st.tabs(["Skills in Demand", "Geographic Distribution", "Salary Insights"])
    
    with tab1:
        st.subheader("Your Skills in Demand")
        
        # Create skills demand chart
        skills_df = pd.DataFrame({
            "Skill": list(skill_mentions.keys()),
            "Mentions": list(skill_mentions.values())
        })
        
        # Sort by mentions
        skills_df = skills_df.sort_values("Mentions", ascending=False)
        
        # Display chart
        fig = px.bar(skills_df, x="Skill", y="Mentions", color="Mentions",
                    title="Your Skills Mentioned in Job Descriptions",
                    color_continuous_scale="blues")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display insights text
        if not skills_df.empty:
            top_skill = skills_df.iloc[0]["Skill"]
            top_mentions = skills_df.iloc[0]["Mentions"]
            st.info(f"Your most in-demand skill is **{top_skill}**, mentioned in {top_mentions} job postings. This skill appears in {top_mentions/len(job_matches)*100:.1f}% of the job matches.")
            
            # Skills not mentioned
            not_mentioned = [skill for skill in user_skills if skill not in skill_mentions]
            if not_mentioned:
                st.warning(f"The following skills were not mentioned in any job posting: {', '.join(not_mentioned)}. Consider focusing on other skills in your resume.")
    
    with tab2:
        st.subheader("Job Opportunities by Location")
        
        # Count locations
        location_counts = pd.Series(locations).value_counts().reset_index()
        location_counts.columns = ["Location", "Count"]
        
        # Display chart
        fig = px.pie(location_counts, values="Count", names="Location",
                    title="Job Distribution by Location")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display map if we have location data
        if locations:
            # Would need to geocode locations for an actual map
            st.info("A geographic map would be displayed here with actual latitude/longitude data.")
    
    with tab3:
        st.subheader("Salary Insights")
        st.info("This section would display salary data extracted from job descriptions or from a salary database. For now, showing dummy data.")
        
        # Create dummy salary data
        salary_data = {
            "Job Title": ["Software Engineer", "Data Scientist", "DevOps Engineer", "Product Manager", "UX Designer"],
            "Min Salary": [70000, 85000, 75000, 90000, 65000],
            "Max Salary": [120000, 145000, 125000, 150000, 110000],
            "Average": [95000, 115000, 100000, 120000, 87500]
        }
        salary_df = pd.DataFrame(salary_data)
        
        # Display salary range chart
        fig = go.Figure()
        for i, row in salary_df.iterrows():
            fig.add_trace(go.Bar(
                name=row["Job Title"],
                y=[row["Job Title"]],
                x=[row["Max Salary"] - row["Min Salary"]],
                orientation='h',
                marker=dict(
                    color='rgba(58, 71, 180, 0.6)',
                    line=dict(color='rgba(58, 71, 180, 1.0)', width=3)
                ),
                base=row["Min Salary"]
            ))
        
        fig.update_layout(
            title="Salary Ranges by Job Title",
            xaxis_title="Salary (USD)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display average salaries
        st.subheader("Average Salaries")
        avg_fig = px.bar(salary_df, x="Job Title", y="Average", color="Average",
                      title="Average Salary by Job Title", color_continuous_scale="blues")
        st.plotly_chart(avg_fig, use_container_width=True)
