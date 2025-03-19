# tests/test_integration.py
import unittest
import os
import tempfile
from models.resume_parser import ResumeParser
from models.job_matcher import JobMatcher
from database.db_connector import DatabaseConnector

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.resume_parser = ResumeParser()
        self.job_matcher = JobMatcher()
        self.db_connector = DatabaseConnector()
        
        # Create a temporary test database
        self.db_connector.db = self.db_connector.client["jobify_test"]
        
        # Sample job descriptions
        self.job_descriptions = [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "Looking for a software engineer with experience in Python, JavaScript, and ReactJS."
            },
            {
                "title": "Data Scientist",
                "company": "Data Inc",
                "description": "Seeking a data scientist with machine learning experience and Python skills."
            }
        ]
        
        # Path to sample resume
        self.test_pdf_path = os.path.join(os.path.dirname(__file__), "../data/sample_resumes/test_resume.pdf")
    
    def tearDown(self):
        # Clean up the test database
        self.db_connector.client.drop_database("jobify_test")
    
    def test_end_to_end_flow(self):
        # Parse resume
        with open(self.test_pdf_path, 'rb') as file:
            resume_data = self.resume_parser.parse_pdf(file)
        
        # Check if resume parsing worked
        self.assertIsNotNone(resume_data)
        self.assertIn("skills", resume_data)
        
        # Save resume to database
        user_id = "test_user"
        resume_id = self.db_connector.save_resume(user_id, resume_data)
        
        # Check if resume was saved
        self.assertIsNotNone(resume_id)
        
        # Preprocess job descriptions
        self.job_matcher.preprocess_job_descriptions(self.job_descriptions)
        
        # Match resume with job descriptions
        job_matches = self.job_matcher.match_resume(resume_data)
        
        # Check if job matching worked
        self.assertIsNotNone(job_matches)
        self.assertEqual(len(job_matches), len(self.job_descriptions))
        
        # Save job matches to database
        match_id = self.db_connector.save_job_matches(user_id, job_matches)
        
        # Check if job matches were saved
        self.assertIsNotNone(match_id)
        
        # Retrieve resume from database
        retrieved_resume = self.db_connector.get_resume(user_id)
        
        # Check if retrieved resume matches original
        self.assertEqual(retrieved_resume, resume_data)
        
        # Retrieve job matches from database
        retrieved_matches = self.db_connector.get_job_matches(user_id)
        
        # Check if retrieved matches match original
        self.assertEqual(len(retrieved_matches), len(job_matches))
