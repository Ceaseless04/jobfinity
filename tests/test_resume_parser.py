# tests/test_resume_parser.py
import unittest
import os
from models.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        self.test_pdf_path = os.path.join(os.path.dirname(__file__), "../data/sample_resumes/test_resume.pdf")
    
    def test_parse_pdf(self):
        with open(self.test_pdf_path, 'rb') as file:
            result = self.parser.parse_pdf(file)
        
        # Check if the parser returns a dictionary
        self.assertIsInstance(result, dict)

    def test_extract_skills(self):
        sample_text = "Experience with Python, JavaScript, and React. Proficient in data analysis and machine learning."
        skills = self.parser._extract_skills(sample_text)
        
        # Check if common skills are detected
        self.assertIn("Python", skills)
        self.assertIn("JavaScript", skills)
        self.assertIn("React", skills)
        self.assertIn("data analysis", skills)
        self.assertIn("machine learning", skills)
    
    def test_extract_experience(self):
        sample_text = "Work Experience:\nSoftware Engineer at Tech Corp (2018-2020)\nDeveloped web applications using React and Node.js\n\nData Scientist at Data Inc (2020-Present)\nBuilt machine learning models for recommendation systems"
        experience = self.parser._extract_experience(sample_text)
        
        # Check if we extract the correct number of experiences
        self.assertEqual(len(experience), 2)
        
        # Check if job titles are extracted correctly
        self.assertEqual(experience[0].get("title"), "Software Engineer")
        self.assertEqual(experience[1].get("title"), "Data Scientist")
        
        # Check if companies are extracted correctly
        self.assertEqual(experience[0].get("company"), "Tech Corp")
        self.assertEqual(experience[1].get("company"), "Data Inc")

    def test_extract_education(self):
        sample_text = "Education:\nBachelor of Science in Computer Science, University of Tech (2014-2018)\nMaster of Science in Data Science, Data University (2018-2020)"
        education = self.parser._extract_education(sample_text)
        
        # Check if we extract the correct number of education entries
        self.assertEqual(len(education), 2)
        
        # Check if degrees are extracted correctly
        self.assertEqual(education[0].get("degree"), "Bachelor of Science")
        self.assertEqual(education[1].get("degree"), "Master of Science")
        
        # Check if fields of study are extracted correctly
        self.assertEqual(education[0].get("field"), "Computer Science")
        self.assertEqual(education[1].get("field"), "Data Science")
