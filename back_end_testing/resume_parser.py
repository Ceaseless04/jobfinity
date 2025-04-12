import docx
import PyPDF2
from collections import defaultdict

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return " ".join(text)

# Function to extract text from a .pdf file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return " ".join(text)

# Function to extract skills (can be extended for other sections)
def extract_skills(text):
    # List of common skills for job matching (this can be expanded)
    skills_list = ['python', 'java', 'data analysis', 'machine learning', 'deep learning']
    skills = defaultdict(int)
    
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills[skill] += 1
    return skills

# Function to parse the resume
def parse_resume(file_obj):
    # Get the file extension from the file name
    file_name = file_obj.name  # .name returns the name of the uploaded file
    file_extension = file_name.split('.')[-1].lower()
    
    # Extract text based on the file type (pdf or docx)
    if file_extension == 'pdf':
        text = extract_text_from_pdf(file_obj)
    elif file_extension == 'docx':
        text = extract_text_from_docx(file_obj)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    # Extract skills from the resume text
    skills = extract_skills(text)

    # Returning parsed data (can include more sections like work experience, education, etc.)
    return {
        "skills": skills,
        "resume_text": text
    }
