# src/components/job_search.py
import streamlit as st
from utils.adzuna_api import AdzunaJobsAPI

def render_job_search(job_matcher, resume_data):
    st.subheader("🔍 Job Search (Powered by Adzuna)")

    adzuna_api = AdzunaJobsAPI()
    keyword = resume_data.get("skills", [""])[0]  # use top skill
    location = st.text_input("Enter job location", value="")

    if st.button("Search Jobs"):
        jobs = adzuna_api.search_jobs(keywords=keyword, location=location)

        if jobs:
            st.success(f"Found {len(jobs)} jobs")
            for job in jobs:
                st.markdown(f"### [{job['title']}]({job['url']})")
                st.markdown(f"**Company:** {job['company']}  \n"
                            f"**Location:** {job['location']}  \n"
                            f"**Posted on:** {job['date_posted']}  \n"
                            f"**Type:** {job['employment_type']}  \n"
                            f"**Industry:** {', '.join(job['industries'])}")
                st.markdown(f"**Description:** {job['description'][:250]}...")
                st.markdown("---")
        else:
            st.warning("No jobs found for that keyword or location.")
