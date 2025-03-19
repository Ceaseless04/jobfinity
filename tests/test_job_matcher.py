# tests/test_job_matcher.py
import unittest
from models.job_matcher import JobMatcher

class TestJobMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = JobMatcher()
        
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
            },
            {
                "title": "Frontend Developer",
                "company": "Web Solutions",
                "description": "Need a frontend developer with HTML, CSS, JavaScript, and React experience."
            }
        ]
        
        # Sample resume data
        self.resume_data = {
            "skills": ["Python", "JavaScript", "React", "Machine Learning", "SQL"],
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Dev Corp",
                    "description": "Developed web applications using React and Node.js"
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "institution": "University of Tech"
                }
            ]
        }
    
    def test_preprocess_job_descriptions(self):
        self.matcher.preprocess_job_descriptions(self.job_descriptions)
        
        # Check if the job descriptions are stored
        self.assertEqual(self.matcher.job_descriptions, self.job_descriptions)
        
        # Check if the job vectors are created
        self.assertIsNotNone(self.matcher.job_vectors)
        
        # Check dimensions of job vectors
        self.assertEqual(self.matcher.job_vectors.shape[0], len(self.job_descriptions))
    
    def test_match_resume(self):
        # Preprocess job descriptions
        self.matcher.preprocess_job_descriptions(self.job_descriptions)
        
        # Match resume
        job_matches = self.matcher.match_resume(self.resume_data)
        
        # Check if we get the correct number of matches
        self.assertEqual(len(job_matches), len(self.job_descriptions))
        
        # Check if each match has a similarity score
        for job_match in job_matches:
            self.assertIn("similarity_score", job_match)
            self.assertIsInstance(job_match["similarity_score"], float)
            self.assertTrue(0 <= job_match["similarity_score"] <= 1)
        
        # Check if matches are sorted by similarity score
        scores = [job["similarity_score"] for job in job_matches]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_create_resume_text(self):
        resume_text = self.matcher._create_resume_text(self.resume_data)
        
        # Check if skills are included in the resume text
        for skill in self.resume_data["skills"]:
            self.assertIn(skill, resume_text)
        
        # Check if experience details are included
        self.assertIn(self.resume_data["experience"][0]["title"], resume_text)
        self.assertIn(self.resume_data["experience"][0]["company"], resume_text)
        
        # Check if education details are included
        self.assertIn(self.resume_data["education"][0]["degree"], resume_text)
        self.assertIn(self.resume_data["education"][0]["field"], resume_text)
