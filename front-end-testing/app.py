import streamlit as st
import time

st.set_page_config(page_title="AI-Powered Resume Analyzer")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'form'
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

# Function to simulate processing and move to result page
def go_to_result():
    st.session_state.page = 'result'
    st.session_state.upload_time = time.time()
    st.session_state.show_recommendations = False
    st.rerun()

# FORM PAGE
if st.session_state.page == 'form':
    st.markdown(
        """
        <div style='text-align: center; white-space: nowrap; overflow: hidden;'>
            <h2 style='color: #4CAF50; display: inline-block; font-size: 28px;'>
                Welcome to Jobfinity AI-Powered Resume Analyzer
            </h2>
        </div>
        <p style='color: #4CAF50; font-size: 18px; text-align: center;'>
            Please upload your resume to get job recommendations!!!
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("- This app uses AI models to analyze your resume and suggest job roles that match your skills and experience.")
    st.write("- Please fill in your name and upload your resume in PDF or DOCX format.")
    st.write("- Note: The resume will not be stored or shared with any third party. It will only be used for analysis.")

    name = st.text_input("Enter your name:")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX):")

    if name and uploaded_file:
        st.session_state.user_name = name  # 🔑 Store name
        go_to_result()


# RESULT PAGE
elif st.session_state.page == 'result':
    name_display = st.text_input("Confirm your name:", key="confirmed_name", placeholder="Enter your name again")

    if not name_display:
        st.warning("Please confirm your name to continue.")
    elif name_display != st.session_state.user_name:
        st.error("The name you entered doesn't match the name from the previous page. Please try again.")
    else:
        st.success(f"Hi {name_display}, your resume has been uploaded successfully! Processing data....")

        # Show recommendations after 3 seconds
        current_time = time.time()
        elapsed = current_time - st.session_state.upload_time

        if not st.session_state.show_recommendations and elapsed >= 3:
            st.session_state.show_recommendations = True
            st.rerun()

        if st.session_state.show_recommendations:
            st.subheader("Here are the top 5 job recommendations you could pursue based on your uploaded resume:")
            recommendations = [
                "Data Scientist",
                "Software Engineer",
                "Product Manager",
                "UX Designer",
                "Marketing Specialist"
            ]
            for job in recommendations:
                st.write(f"- {job}")
