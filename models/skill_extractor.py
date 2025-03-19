# models/skill_extractor.py
import json
import os
import spacy
from collections import defaultdict

class SkillExtractor:
    def __init__(self, skills_db_path=None):
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_md')
        
        # Load skills database
        self.skills_db = self._load_skills_db(skills_db_path)
        
        # Create skill patterns for matching
        self._create_skill_patterns()
    
    def _load_skills_db(self, path=None):
        """Load skills database from JSON file or use default."""
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        else:
            # Default skills database with common tech skills
            return {
                "programming_languages": ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go"],
                "frameworks": ["React", "Angular", "Vue", "Django", "Flask", "Spring", "Express", "TensorFlow", "PyTorch", "Scikit-learn"],
                "databases": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server", "Redis", "Cassandra", "DynamoDB"],
                "tools": ["Git", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "Jenkins", "Jira", "Confluence", "Slack"],
                "soft_skills": ["Communication", "Leadership", "Problem Solving", "Critical Thinking", "Teamwork", "Time Management"]
            }
    
    def _create_skill_patterns(self):
        """Create patterns for skill matching."""
        self.skill_patterns = []
        self.skill_dict = {}
        
        # Flatten skills from categories
        for category, skills in self.skills_db.items():
            for skill in skills:
                # Create pattern for exact matching
                pattern = [{"LOWER": token.lower()} for token in skill.split()]
                self.skill_patterns.append({"label": category, "pattern": pattern})
                
                # Add to dictionary for faster lookup
                self.skill_dict[skill.lower()] = category
    
    def extract_skills(self, text):
        """Extract skills from text using pattern matching and NLP."""
        doc = self.nlp(text)
        
        # Results dictionary
        results = {
            "skills_by_category": defaultdict(list),
            "all_skills": []
        }
        
        # Process text to find skills
        processed_text = text.lower()
        
        # Check for exact matches
        for skill, category in self.skill_dict.items():
            if skill in processed_text:
                # Avoid adding duplicates
                if skill not in results["skills_by_category"][category]:
                    results["skills_by_category"][category].append(skill)
                    results["all_skills"].append(skill)
        
        # Check for phrase matches
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if chunk_text in self.skill_dict:
                category = self.skill_dict[chunk_text]
                if chunk_text not in results["skills_by_category"][category]:
                    results["skills_by_category"][category].append(chunk_text)
                    results["all_skills"].append(chunk_text)
        
        return results
