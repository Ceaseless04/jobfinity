from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample job descriptions (these could be loaded from a database or API)
job_descriptions = [
    "We are looking for a Python developer with experience in machine learning and deep learning.",
    "Seeking a data scientist with expertise in statistical analysis, Python, and machine learning.",
    "Hiring for a software engineer proficient in Java, algorithms, and software development."
]

# Function to match resume skills with job descriptions
def match_jobs(resume_skills, job_descriptions):
    # Convert job descriptions and resume skills into TF-IDF vectors
    corpus = job_descriptions + [resume_skills]  # Add resume skills to the corpus
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    
    # Compute cosine similarity between the resume and job descriptions
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Create a result dictionary with job descriptions and match scores
    job_matches = {
        job_descriptions[i]: similarity_scores[0][i] * 100  # Match percentage
        for i in range(len(job_descriptions))
    }
    
    return job_matches

