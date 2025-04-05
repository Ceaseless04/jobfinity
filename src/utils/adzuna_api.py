import requests
import os
from datetime import datetime
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY  # pulls from your .env via config.py

class AdzunaJobsAPI:
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id or ADZUNA_APP_ID
        self.app_key = app_key or ADZUNA_APP_KEY

        if not self.app_id or not self.app_key:
            raise ValueError("Missing Adzuna API credentials. Set ADZUNA_APP_ID and ADZUNA_APP_KEY in .env")

        self.base_url = "https://api.adzuna.com/v1/api/jobs/us/search/{}"

    def search_jobs(self, keywords, location=None, results_per_page=25, page=1):
        """Search for jobs based on keywords and optional location."""
        url = self.base_url.format(page)

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "what": keywords,
            "content-type": "application/json"
        }

        if location:
            params["where"] = location

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return self._process_jobs_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from Adzuna API: {e}")
            return []

    def _process_jobs_response(self, response_data):
        """Process the Adzuna API response and extract relevant job information."""
        processed_jobs = []

        for job in response_data.get("results", []):
            job_info = {
                "job_id": job.get("id", ""),
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "description": job.get("description", ""),
                "url": job.get("redirect_url", ""),
                "date_posted": self._format_date(job.get("created", "")),
                "employment_type": job.get("contract_time", ""),  # full_time / part_time
                "experience_level": "",  # Adzuna doesn’t provide this directly
                "industries": [job.get("category", {}).get("label", "")]
            }

            processed_jobs.append(job_info)

        return processed_jobs

    def _format_date(self, iso_string):
        """Convert ISO 8601 timestamp to YYYY-MM-DD format."""
        if not iso_string:
            return ""

        try:
            dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
        except Exception:
            return ""
