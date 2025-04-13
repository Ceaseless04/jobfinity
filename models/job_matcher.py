# models/job_matcher.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        resume_text = ""

        # Skills
        if isinstance(resume_data.get("skills"), dict):
            resume_text += " ".join(resume_data["skills"].get("all_skills", [])) + " "

        # Experience
        for exp in resume_data.get("experience", []):
            resume_text += exp.get("title", "") + " "
            resume_text += exp.get("company", "") + " "
            resume_text += exp.get("description", "") + " "

        # Education
        for edu in resume_data.get("education", []):
            resume_text += edu.get("degree", "") + " "
            resume_text += edu.get("field", "") + " "
            resume_text += edu.get("school", "") + " "

        return resume_text.strip()

