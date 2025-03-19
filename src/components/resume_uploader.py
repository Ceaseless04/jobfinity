# src/components/resume_uploader.py
import streamlit as st
import pandas as pd
import tempfile

def render_resume_uploader(resume_parser):
    st.header("Upload Your Resume")
    
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])
    
    resume_data = None
    
    if uploaded_file is not None:
        # Display the uploaded file
        st.success("File successfully uploaded!")
        
        # Create a button to parse the resume
        if st.button("Parse Resume"):
            with st.spinner("Parsing resume..."):
                # Save the uploaded file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # Parse the resume
                if uploaded_file.name.endswith('.pdf'):
                    resume_data = resume_parser.parse_pdf(open(tmp_path, 'rb'))
                elif uploaded_file.name.endswith('.docx'):
                    resume_data = resume_parser.parse_docx(tmp_path)
                
                # Display the parsed data
                if resume_data:
                    st.subheader("Parsed Resume Data")
                    
                    # Display skills
                    st.write("**Skills:**")
                    skills_df = pd.DataFrame({"Skills": resume_data.get("skills", [])})
                    st.dataframe(skills_df)
                    
                    # Display experience
                    st.write("**Experience:**")
                    experience = resume_data.get("experience", [])
                    for idx, exp in enumerate(experience):
                        st.write(f"**{exp.get('title', '')} at {exp.get('company', '')}**")
                        st.write(f"*{exp.get('duration', '')}*")
                        st.write(exp.get('description', ''))
                    
                    # Display education
                    st.write("**Education:**")
                    education = resume_data.get("education", [])
                    for idx, edu in enumerate(education):
                        st.write(f"**{edu.get('degree', '')} in {edu.get('field', '')}**")
                        st.write(f"*{edu.get('institution', '')}*")
                        st.write(edu.get('duration', ''))
                
                else:
                    st.error("Failed to parse the resume. Please try again with a different file.")
    
    return resume_data
