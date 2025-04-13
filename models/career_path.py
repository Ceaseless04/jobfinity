import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity

class CareerPathRecommender:
    def __init__(self, job_descriptions):
        # Dynamically extract career paths from job descriptions
        self.career_paths = self._extract_paths_from_jobs(job_descriptions)

    def _extract_paths_from_jobs(self, jobs):
        grouped = {
            "Software Development": {
                "keywords": ["software", "developer", "programmer", "engineer"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on building software applications and systems."
            },
            "Data Science": {
                "keywords": ["data", "machine learning", "ai", "scientist"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on extracting insights and building models from data."
            },
            "DevOps": {
                "keywords": ["devops", "infrastructure", "cloud", "kubernetes", "docker"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on operations, infrastructure, and deployment."
            },
            "Frontend Development": {
                "keywords": ["frontend", "ui", "ux", "react", "css", "html"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on building modern, interactive web interfaces."
            },
            "Backend Development": {
                "keywords": ["backend", "server", "api", "django", "flask"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on building server-side applications and APIs."
            },
            "Cloud Architecture": {
                "keywords": ["cloud", "aws", "azure", "architect"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on designing and managing cloud infrastructure."
            },
            "QA & Testing": {
                "keywords": ["qa", "test", "testing", "automation"],
                "skills": set(),
                "roles": set(),
                "description": "Career path focused on ensuring software quality and reliability."
            }
        }

        for job in jobs:
            title = job["title"].lower()
            desc = job["description"].lower()
            matched = False

            for path, data in grouped.items():
                if any(k in title or k in desc for k in data["keywords"]):
                    data["skills"].update(desc.split())
                    data["roles"].add(job["title"])
                    matched = True
                    break

            if not matched:
                grouped.setdefault("Other", {
                    "keywords": [],
                    "skills": set(),
                    "roles": set(),
                    "description": "Uncategorized career path."
                })["roles"].add(job["title"])

        # Convert to usable format
        final = {}
        for k, v in grouped.items():
            final[k] = {
                "skills": list(v["skills"]),
                "roles": list(v["roles"] or ["Entry Level"]),
                "description": v["description"]
            }
        return final

    def recommend_career_paths(self, resume_data):
        user_skills = set([skill.lower() for skill in resume_data.get("skills", {}).get("all_skills", [])])

        path_scores = {}
        for path_name, path_data in self.career_paths.items():
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            intersection = len(user_skills.intersection(path_skills))
            union = len(user_skills.union(path_skills))
            similarity = intersection / union if union > 0 else 0
            path_scores[path_name] = similarity

        # Get sorted path list
        sorted_paths = sorted(path_scores.items(), key=lambda x: x[1], reverse=True)

        # Recommend 2nd to 5th best paths
        recommendations = []
        for path_name, score in sorted_paths[1:5]:
            path_data = self.career_paths[path_name]
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            missing_skills = path_skills - user_skills

            experience_years = self._calculate_total_experience(resume_data)
            current_role_index = min(int(experience_years / 2), len(path_data["roles"]) - 2)
            current_role = path_data["roles"][current_role_index]
            next_role = path_data["roles"][current_role_index + 1]

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
        for experience in resume_data.get("experience", []):
            duration = experience.get("duration", "")
            match = re.search(r'(\d+)\s*(years|year|yr)', duration, re.IGNORECASE)
            if match:
                total_years += int(match.group(1))
            else:
                total_years += 1
        return total_years

