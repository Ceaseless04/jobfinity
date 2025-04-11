import streamlit as st
import time

# Function to simulate AI processing
def process_resume(name, resume):
    # Simulating processing time (e.g., AI model analysis)
    time.sleep(3)  # Simulate delay for processing
    st.write(f"Hi {name}, your resume has been uploaded successfully! Processing data....")
    time.sleep(2)  # Simulate some more time for processing

    # Displaying job recommendations (This would be dynamic once you integrate AI)
    st.write("AI Job Recommendations:")
    st.write("1. Data Scientist")
    st.write("2. Software Engineer")
    st.write("3. Product Manager")
    st.write("4. UX Designer")
    st.write("5. Marketing Specialist")

# Main UI
def main():
    st.title("AI Powered Resume Analyzer")

    # Step 1: Input name
    name = st.text_input("Enter your name:")
    
    # Step 2: File upload for resume
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX):", type=['pdf', 'docx'])

    if name and uploaded_file:
        # Once both name and file are entered, show processing message
        st.write(f"Hi {name}, your resume has been uploaded successfully! Processing data....")
        
        # Simulate processing time
        process_resume(name, uploaded_file)

    elif name == "":
        st.warning("Please enter your name.")
    elif uploaded_file is None:
        st.warning("Please upload your resume.")

# Run the app
if __name__ == "__main__":
    main()
