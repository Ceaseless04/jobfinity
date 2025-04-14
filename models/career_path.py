import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import defaultdict
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

class CareerPathRecommender:
    def __init__(self, job_descriptions):
        self.job_descriptions = job_descriptions
        self.career_paths = self._extract_paths_from_jobs(job_descriptions)

    def recommend_career_paths(self, resume_data):
        user_skills = set([skill.lower() for skill in resume_data.get("skills", {}).get("all_skills", [])])

        path_scores = {}
        for path_name, path_data in self.career_paths.items():
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            intersection = len(user_skills.intersection(path_skills))
            union = len(user_skills.union(path_skills))
            similarity = intersection / union if union else 0
            path_scores[path_name] = similarity

        sorted_paths = sorted(path_scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = []

        for path_name, score in sorted_paths[1:5]:  # Skip top path (assumed served by job matcher)
            path_data = self.career_paths[path_name]
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            missing_skills = path_skills - user_skills

            experience_years = self._calculate_total_experience(resume_data)
            current_index = min(int(experience_years / 2), len(path_data["roles"]) - 2)
            current_role = path_data["roles"][current_index]
            next_role = path_data["roles"][current_index + 1]

            recommendations.append({
                "path_name": path_name,
                "similarity_score": score * 100,
                "description": path_data["description"],
                "current_role": current_role,
                "next_role": next_role,
                "missing_skills": list(missing_skills)[:5],
                "career_progression": path_data["roles"]
            })

        return recommendations

    def _calculate_total_experience(self, resume_data):
        total_years = 0
        for exp in resume_data.get("experience", []):
            duration = exp.get("duration", "")
            match = re.search(r'(\d+)\s*(?:years|year|yr)', duration, re.IGNORECASE)
            if match:
                total_years += int(match.group(1))
            else:
                total_years += 1
        return total_years

    def _extract_paths_from_jobs(self, jobs):
        keyword_categories = {
            "Software Development": ["developer", "engineer", "software", "full stack", "backend", "frontend"],
            "Data Science": ["data scientist", "machine learning", "ai", "analyst"],
            "DevOps": ["devops", "site reliability", "infrastructure", "cloud", "ci/cd", "sre"],
            "QA": ["qa", "quality assurance", "test", "automation"],
            "Cloud Engineering": ["cloud", "aws", "azure", "gcp", "architect"],
            "Frontend Development": ["frontend", "react", "vue", "html", "css", "ui"],
            "Backend Development": ["backend", "django", "flask", "node", "sql", "database"],
            "Product Management": [
                "product manager", "product owner", "roadmap", "stakeholders", "market research",
                "requirements", "product strategy", "go-to-market", "product lifecycle"
            ],
            "Project Management": [
                "project manager", "scrum master", "agile", "waterfall", "timeline", "milestones",
                "budget", "risk management", "status reporting", "resource allocation"
            ]
        }

        common_skills = {
            "python", "java", "c++", "javascript", "react", "angular", "node.js",
            "git", "docker", "kubernetes", "aws", "sql", "flask", "django",
            "machine learning", "tensorflow", "pytorch", "css", "html", "linux",
            "ci/cd", "jenkins", "vue", "azure", "gcp", "jira", "selenium"
        }

        path_data = defaultdict(lambda: {
            "skills": set(),
            "roles": set(),
            "description": "",
        })

        for job in jobs:
            title = job.get("title", "").lower()
            desc = job.get("description", "").lower()
            combined = f"{title} {desc}"

            for category, keywords in keyword_categories.items():
                if any(k in combined for k in keywords):
                    path_data[category]["roles"].add(job.get("title", "Unknown Role"))
                    path_data[category]["description"] = f"Auto-generated from Adzuna job titles/descriptions for {category}"
                    matched_skills = [s for s in common_skills if s in desc]
                    path_data[category]["skills"].update(matched_skills)

        return {k: {
            "skills": list(v["skills"]),
            "roles": list(v["roles"]),
            "description": v["description"]
        } for k, v in path_data.items() if v["skills"] and v["roles"]}

