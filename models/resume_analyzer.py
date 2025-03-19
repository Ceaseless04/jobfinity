# models/resume_analyzer.py
from collections import Counter
import re

class ResumeAnalyzer:
    def __init__(self):
        # Common action verbs for resumes
        self.action_verbs = [
            "achieved", "improved", "trained", "maintained", "managed", "created",
            "resolved", "volunteered", "influenced", "increased", "decreased",
            "researched", "formulated", "developed", "designed", "revamped",
            "eliminated", "strengthened", "accelerated", "enhanced", "optimized"
        ]
        
        # Common weak words to avoid
        self.weak_words = [
            "responsible for", "worked on", "helped with", "assisted", "participated in",
            "duties included", "was involved in", "handled", "successfully", "effectively"
        ]
    
    def analyze_resume(self, resume_data):
        """Analyze resume and provide improvement suggestions."""
        suggestions = []
        
        # Check for action verbs in experience descriptions
        action_verb_count = 0
        weak_word_count = 0
        
        for experience in resume_data.get("experience", []):
            description = experience.get("description", "").lower()
            
            # Count action verbs
            for verb in self.action_verbs:
                if verb in description:
                    action_verb_count += 1
            
            # Count weak words
            for word in self.weak_words:
                if word in description:
                    weak_word_count += 1
        
        # Suggest using more action verbs if needed
        if action_verb_count < 3 and resume_data.get("experience"):
            suggestions.append({
                "category": "Action Verbs",
                "suggestion": "Use more action verbs in your experience descriptions to showcase your achievements.",
                "examples": ", ".join(self.action_verbs[:5])
            })
        
        # Suggest avoiding weak words if needed
        if weak_word_count > 0:
            suggestions.append({
                "category": "Weak Words",
                "suggestion": "Avoid using weak or passive phrases in your experience descriptions.",
                "examples": "Replace phrases like '" + "', '".join(self.weak_words[:3]) + "' with stronger action verbs."
            })
        
        # Check for skills relevance
        if resume_data.get("skills"):
            skills_count = len(resume_data["skills"])
            if skills_count < 5:
                suggestions.append({
                    "category": "Skills",
                    "suggestion": "Consider adding more relevant skills to your resume.",
                    "examples": "Technical skills, soft skills, and domain-specific knowledge."
                })
        
        # Check for education details
        if not resume_data.get("education"):
            suggestions.append({
                "category": "Education",
                "suggestion": "Add your educational background to your resume.",
                "examples": "Include degrees, certifications, and relevant coursework."
            })
        
        # Check for contact information
        if not resume_data.get("contact"):
            suggestions.append({
                "category": "Contact Information",
                "suggestion": "Ensure your contact information is included and up-to-date.",
                "examples": "Email, phone number, LinkedIn profile, and location."
            })
        
        return suggestions
