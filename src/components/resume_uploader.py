# src/components/resume_uploader.py
import streamlit as st
import tempfile
import pandas as pd

def render_resume_uploader(resume_parser):
    st.header("Upload Your Resume")

    uploaded_file = st.file_uploader("Choose a resume file", type="pdf")
    resume_data = None

    if uploaded_file:
        st.success("File successfully uploaded!")

        if st.button("Parse Resume"):
            with st.spinner("Parsing resume..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                if uploaded_file.name.endswith(".pdf"):
                    resume_data = resume_parser.parse_pdf(open(tmp_path, "rb"))
                elif uploaded_file.name.endswith(".docx"):
                    resume_data = resume_parser.parse_docx(tmp_path)

                if resume_data:
                    st.subheader("Parsed Resume Data")

                    st.markdown("**Skills:**")
                    skills = resume_data.get("skills", {}).get("all_skills", [])
                    st.dataframe(pd.DataFrame({"Skills": skills}))

                    st.markdown("**Experience:**")
                    for exp in resume_data.get("experience", []):
                        st.write(f"**{exp.get('title', '')} at {exp.get('company', '')}**")
                        st.write(f"{exp.get('dates', '')}")

                    st.markdown("**Education:**")
                    for edu in resume_data.get("education", []):
                        st.write(f"**{edu.get('degree', '')} in {edu.get('field', '')}**")
                        st.write(f"{edu.get('school', '')}")
                else:
                    st.error("Failed to parse the resume. Please try a different file.")

    return resume_data

