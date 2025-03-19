# models/career_path.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CareerPathRecommender:
    def __init__(self):
        # Career paths with corresponding skills and roles
        self.career_paths = {
            "Software Development": {
                "skills": ["Python", "Java", "JavaScript", "C++", "React", "Angular", "Node.js", "Git", "CI/CD"],
                "roles": [
                    "Junior Developer",
                    "Software Engineer",
                    "Senior Software Engineer",
                    "Lead Developer",
                    "Software Architect",
                    "Technical Director"
                ],
                "description": "Career path focused on building software applications and systems."
            },
            "Data Science": {
                "skills": ["Python", "R", "SQL", "Machine Learning", "Data Analysis", "Statistics", "TensorFlow", "PyTorch"],
                "roles": [
                    "Data Analyst",
                    "Junior Data Scientist",
                    "Data Scientist",
                    "Senior Data Scientist",
                    "Lead Data Scientist",
                    "Chief Data Officer"
                ],
                "description": "Career path focused on extracting insights and building models from data."
            },
            "DevOps": {
                "skills": ["Linux", "Docker", "Kubernetes", "AWS", "Azure", "CI/CD", "Jenkins", "Terraform", "Ansible"],
                "roles": [
                    "IT Support",
                    "System Administrator",
                    "DevOps Engineer",
                    "Site Reliability Engineer",
                    "DevOps Architect",
                    "VP of Infrastructure"
                ],
                "description": "Career path focused on operations, infrastructure, and deployment."
            }
        }
    
    def recommend_career_paths(self, resume_data):
        """Recommend career paths based on the user's resume."""
        # Extract skills from resume
        user_skills = set([skill.lower() for skill in resume_data.get("skills", [])])
        
        # Calculate similarity scores for each career path
        path_scores = {}
        for path_name, path_data in self.career_paths.items():
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            
            # Calculate Jaccard similarity (intersection over union)
            intersection = len(user_skills.intersection(path_skills))
            union = len(user_skills.union(path_skills))
            
            if union > 0:
                similarity = intersection / union
            else:
                similarity = 0
            
            path_scores[path_name] = similarity
        
        # Sort paths by similarity score
        sorted_paths = sorted(path_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create recommendations with next steps
        recommendations = []
        for path_name, score in sorted_paths:
            path_data = self.career_paths[path_name]
            
            # Find missing skills
            path_skills = set([skill.lower() for skill in path_data["skills"]])
            missing_skills = path_skills - user_skills
            
            # Determine current and next role based on experience
            experience_years = self._calculate_total_experience(resume_data)
            current_role_index = min(int(experience_years / 2), len(path_data["roles"]) - 2)
            current_role = path_data["roles"][current_role_index]
            next_role = path_data["roles"][current_role_index + 1]
            
            recommendation = {
                "path_name": path_name,
                "similarity_score": score * 100,  # Convert to percentage
                "description": path_data["description"],
                "current_role": current_role,
                "next_role": next_role,
                "missing_skills": list(missing_skills)[:5],  # Top 5 missing skills
                "career_progression": path_data["roles"]
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_total_experience(self, resume_data):
        """Calculate total years of experience from resume."""
        total_years = 0
        
        for experience in resume_data.get("experience", []):
            # Try to extract duration
            duration = experience.get("duration", "")
            
            # Try to find years in duration string
            years_match = re.search(r'(\d+)\s*(?:years|year|yr)', duration, re.IGNORECASE)
            if years_match:
                total_years += int(years_match.group(1))
            
            # If no explicit years mentioned, assume 1 year
            else:
                total_years += 1
        
        return total_years
