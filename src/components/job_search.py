# src/utils/linkedin_api.py
import requests
import json
import os
from datetime import datetime

class LinkedInJobsAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('LINKEDIN_API_KEY')
        self.base_url = "https://api.linkedin.com/v2/jobs-search"
        
    def search_jobs(self, keywords, location=None, limit=25):
        """Search for jobs based on keywords and location."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "keywords": keywords,
            "count": limit
        }
        
        if location:
            params["location"] = location
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            return self._process_jobs_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from LinkedIn API: {e}")
            return []
    
    def _process_jobs_response(self, response_data):
        """Process the API response and extract relevant job information."""
        processed_jobs = []
        
        for job in response_data.get("elements", []):
            # Extract basic job info
            job_info = {
                "job_id": job.get("entityUrn", "").split(":")[-1],
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("name", ""),
                "location": job.get("locationName", ""),
                "description": job.get("description", {}).get("text", ""),
                "url": f"https://www.linkedin.com/jobs/view/{job.get('entityUrn', '').split(':')[-1]}",
                "date_posted": self._format_date(job.get("postedAt", "")),
                "employment_type": job.get("employmentStatus", ""),
                "experience_level": job.get("experienceLevel", ""),
                "industries": [ind.get("name", "") for ind in job.get("industries", [])]
            }
            
            processed_jobs.append(job_info)
        
        return processed_jobs
    
    def _format_date(self, timestamp):
        """Format timestamp to readable date."""
        if not timestamp:
            return ""
        
        try:
            dt = datetime.fromtimestamp(timestamp / 1000)  # Convert from milliseconds
            return dt.strftime("%Y-%m-%d")
        except:
            return ""
