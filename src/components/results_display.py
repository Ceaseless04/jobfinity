# src/components/results_display.py
import streamlit as st
import pandas as pd

def render_results(job_matches, career_recommendations):
    st.header("🚀 Career Path Recommendations")
    if career_recommendations:
        for path in career_recommendations:
            st.subheader(f"🔹 {path['path_name']}")
            st.write(f"**Current Role:** {path['current_role']}")
            st.write(f"**Next Role:** {path['next_role']}")
            if path['missing_skills']:
                st.markdown("**Missing Skills:**")
                st.markdown(", ".join(path["missing_skills"]))
            st.markdown("---")
    else:
        st.info("No career path recommendations available.")

    st.header("🎯 Top Job Matches")

    if job_matches:
        top_jobs = pd.DataFrame(job_matches)
        top_jobs = top_jobs[["title", "company", "location", "url"]]
        top_jobs.columns = ["Job Title", "Company", "Location", "Apply Link"]

        for _, row in top_jobs.iterrows():
            st.markdown(f"**{row['Job Title']}** at *{row['Company']}* — {row['Location']}  ")
            st.write(f"🔗 [Apply here]({row['Apply Link']})")
            st.markdown("---")
    else:
        st.info("No job matches available.")


