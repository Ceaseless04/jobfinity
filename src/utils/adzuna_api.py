# src/utils/adzuna_api.py
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

class AdzunaJobsAPI:
    def __init__(self, country="us"):
        self.app_id = os.environ.get("ADZUNA_APP_ID")
        self.app_key = os.environ.get("ADZUNA_APP_KEY")
        self.country = country.lower()  # e.g., 'us', 'gb', 'ca'
        self.base_url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/1"

    def search_jobs(self, location=None, limit=100):
        """Search jobs via Adzuna API."""
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": limit,
            "category": "it-jobs",
            "content-type": "application/json",
        }

        if location:
            params["where"] = location

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()['results']

            # Debugging output to check the structure
            print(f"DEBUG: API Response: {data}")

            if not data:
                print("DEBUG: No jobs found in the response.")
            return self._process_jobs_response(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from Adzuna API: {e}")
            return []

    def _process_jobs_response(self, job_list):
        """Extract relevant job fields from the response results."""
        processed_jobs = []
        
        for job in job_list:
            print(job)
            job_info = {
                "title": job.get('title', ''),
                "company": job.get("company", {}).get("display_name", ''),
                "location": job.get('location', {}).get('display_name', ''),
                "description": job.get('description', ''),
                "url": job.get('redirect_url', ''),
                "date_posted": self._format_date(job.get('created', '')),
                "salary_min": job.get('salary_min', None),
                "salary_max": job.get('salary_max', None),
                "category": job.get('category', {}).get('label', ''),
            }

            processed_jobs.append(job_info)

        # Debugging to verify processed data
        print(f"DEBUG: Processed Jobs: {processed_jobs}")
        return processed_jobs

    def _format_date(self, iso_date):
        """Format ISO date to YYYY-MM-DD."""
        try:
            return datetime.fromisoformat(iso_date).strftime("%Y-%m-%d")
        except Exception:
            return ""


