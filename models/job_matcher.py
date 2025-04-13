# models/job_matcher.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    def __init__(self):
        self.vectorizer = None
        self.job_vectors = None
        self.jobs = []
        self.job_descriptions = []

    def preprocess_job_descriptions(self, jobs):
        valid_jobs = [
            job for job in jobs
            if job.get("description") and len(job["description"].strip()) > 20
        ]

        if not valid_jobs:
            raise ValueError("No valid job information to vectorize. Please check job data.")

        self.job_descriptions = [job["description"] for job in valid_jobs]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.job_vectors = self.vectorizer.fit_transform(self.job_descriptions)
        self.jobs = valid_jobs

    def match_resume(self, resume_data):
        resume_text = self._create_resume_text(resume_data)
        if not resume_text.strip():
            raise ValueError("Resume text is empty.")

        resume_vector = self.vectorizer.transform([resume_text])

        if self.job_vectors is None or self.job_vectors.shape[0] == 0:
            raise ValueError("No job vectors available for similarity comparison.")

        similarities = cosine_similarity(resume_vector, self.job_vectors)[0]

        matched_jobs = []
        for i, similarity in enumerate(similarities):
            job_match = self.jobs[i].copy()
            job_match["similarity"] = similarity
            matched_jobs.append(job_match)

        matched_jobs.sort(key=lambda x: x["similarity"], reverse=True)
        return matched_jobs


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
