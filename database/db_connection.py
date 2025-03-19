# database/db_connector.py
import pymongo
import pandas as pd

class DatabaseConnector:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["jobify"]
        
    def save_resume(self, user_id, resume_data):
        """Save parsed resume data to the database."""
        collection = self.db["resumes"]
        resume_document = {
            "user_id": user_id,
            "resume_data": resume_data,
            "created_at": pd.Timestamp.now()
        }
        result = collection.insert_one(resume_document)
        return result.inserted_id
    
    def save_job_matches(self, user_id, job_matches):
        """Save job matches to the database."""
        collection = self.db["job_matches"]
        job_match_document = {
            "user_id": user_id,
            "job_matches": job_matches,
            "created_at": pd.Timestamp.now()
        }
        result = collection.insert_one(job_match_document)
        return result.inserted_id
    
    def get_resume(self, user_id):
        """Retrieve the latest resume data for a user."""
        collection = self.db["resumes"]
        result = collection.find({"user_id": user_id}).sort("created_at", -1).limit(1)
        resume_documents = list(result)
        return resume_documents[0]["resume_data"] if resume_documents else None

    def get_job_matches(self, user_id):
        """Retrieve the latest job matches for a user."""
        collection = self.db["job_matches"]
        result = collection.find({"user_id": user_id}).sort("created_at", -1).limit(1)
        job_match_documents = list(result)
        return job_match_documents[0]["job_matches"] if job_match_documents else None
