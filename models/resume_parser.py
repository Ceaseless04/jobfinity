import io
import re
import nltk
import spacy
from collections import defaultdict
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter

class ResumeParser:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        self.nlp = spacy.load('en_core_web_md')

        # Skills categories (hardcoded instead of loaded from db)
        self.skills_db = {
            "programming_languages": ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go"],
            "frameworks": ["React", "Angular", "Vue", "Django", "Flask", "Spring", "Express", "TensorFlow", "PyTorch", "Scikit-learn"],
            "databases": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server", "Redis", "Cassandra", "DynamoDB"],
            "tools": ["Git", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "Jenkins", "Jira", "Confluence", "Slack"],
            "soft_skills": ["Communication", "Leadership", "Problem Solving", "Critical Thinking", "Teamwork", "Time Management"],
            "data_science": ["Machine Learning", "Data Analysis", "Statistics"]
        }

        self.skill_lookup = {skill.lower(): category for category, skills in self.skills_db.items() for skill in skills}

    def parse_pdf(self, file):
        text = self._extract_text_from_pdf(file)
        return self._process_text(text)

    def _extract_text_from_pdf(self, file):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, converter)

        for page in PDFPage.get_pages(file, check_extractable=True):
            interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text

    def _process_text(self, text):
        return {
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "education": self._extract_education(text),
        }

    def _extract_skills(self, text):
        doc = self.nlp(text.lower())
        skills_by_category = defaultdict(list)
        all_skills = []

        for token in doc:
            token_text = token.text.strip().lower()
            if token_text in self.skill_lookup:
                category = self.skill_lookup[token_text]
                if token_text not in skills_by_category[category]:
                    skills_by_category[category].append(token_text)
                    all_skills.append(token_text)

        return {
            "skills_by_category": dict(skills_by_category),
            "all_skills": all_skills
        }

    def _extract_experience(self, text):
        exp_section = re.search(r'(Work Experience|Experience|Professional Experience)(.*?)(Education|Projects|Skills|$)', text, re.DOTALL | re.IGNORECASE)
        exp_text = exp_section.group(2).strip() if exp_section else text

        exp_entries = re.findall(r'(?P<title>.+?) at (?P<company>.+?) \((?P<dates>[\d\-\u2013 ]+)\)', exp_text)
        exp_data = []

        for match in exp_entries:
            title, company, dates = match
            exp_data.append({
                "title": title.strip(),
                "company": company.strip(),
                "dates": dates.strip()
            })

        return exp_data

    def _extract_education(self, text):
        education_section = re.search(r'(Education)(.*?)(Experience|Skills|Projects|$)', text, re.DOTALL | re.IGNORECASE)
        education_text = education_section.group(2).strip() if education_section else text

        # Improved regex without trailing unescaped "("
        education_entries = re.findall(
            r'(?P<degree>Bachelor|Master|PhD|Associate)[^,\n]* in (?P<field>[^,\n]*)[,\n]+(?P<school>[^\n]+)', 
            education_text, re.IGNORECASE
        )

        education_data = []
        for match in education_entries:
            degree, field, school = match
            education_data.append({
                "degree": degree.strip(),
                "field": field.strip(),
                "school": school.strip()
            })

        return education_data

