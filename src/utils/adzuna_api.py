# models/job_matcher.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def preprocess_job_descriptions(self, job_descriptions):
        # Preprocess job descriptions for matching
        job_texts = [job['description'] for job in job_descriptions]
        self.job_descriptions = job_descriptions
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        
    def match_resume(self, resume_data):
        # Extract relevant text from resume data
        resume_text = self._create_resume_text(resume_data)
        
        # Transform resume text to vector
        resume_vector = self.vectorizer.transform([resume_text])
        
        # Calculate similarity between resume and job descriptions
        similarities = cosine_similarity(resume_vector, self.job_vectors)[0]
        
        # Rank job matches
        job_matches = []
        for i, similarity in enumerate(similarities):
            job_match = self.job_descriptions[i].copy()
            job_match['similarity_score'] = similarity
            job_matches.append(job_match)
        
        # Sort by similarity score
        job_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return job_matches
    
    def _create_resume_text(self, resume_data):
        # Combine relevant parts of the resume into a single text
        resume_text = ""
        
        # Add skills
        if 'skills' in resume_data:
            resume_text += " ".join(resume_data['skills']) + " "
        
        # Add experience
        if 'experience' in resume_data:
            for exp in resume_data['experience']:
                resume_text += exp.get('title', '') + " "
                resume_text += exp.get('company', '') + " "
                resume_text += exp.get('description', '') + " "
        
        # Add education
        if 'education' in resume_data:
            for edu in resume_data['education']:
                resume_text += edu.get('degree', '') + " "
                resume_text += edu.get('field', '') + " "
                resume_text += edu.get('institution', '') + " "
        
        return resume_text