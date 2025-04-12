# src/utils/adzuna_api.py
import requests
import os
from datetime import datetime

class AdzunaJobsAPI:
    def __init__(self, app_id=None, app_key=None, country="us"):
        self.app_id = app_id or os.environ.get("ADZUNA_APP_ID")
        self.app_key = app_key or os.environ.get("ADZUNA_APP_KEY")
        self.country = country.lower()  # e.g., 'us', 'gb', 'ca'
        self.base_url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/1"

    def search_jobs(self, keywords, location=None, limit=20):
        """Search jobs via Adzuna API."""
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": limit,
            "what": keywords,
            "content-type": "application/json",
        }

        if location:
            params["where"] = location

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return self._process_jobs_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from Adzuna API: {e}")
            return []

    def _process_jobs_response(self, data):
        """Extract relevant job fields from Adzuna's response."""
        processed_jobs = []

        for job in data.get("results", []):
            job_info = {
                "job_id": job.get("id", ""),
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "description": job.get("description", ""),
                "url": job.get("redirect_url", ""),
                "date_posted": self._format_date(job.get("created", "")),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "category": job.get("category", {}).get("label", ""),
            }

            processed_jobs.append(job_info)

        return processed_jobs

    def _format_date(self, iso_date):
        """Format ISO date to YYYY-MM-DD."""
        try:
            return datetime.fromisoformat(iso_date).strftime("%Y-%m-%d")
        except Exception:
            return ""