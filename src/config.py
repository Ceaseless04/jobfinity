# src/config.py
import os

# API keys and credentials
LINKEDIN_API_KEY = os.environ.get("LINKEDIN_API_KEY", "")

# Database configuration
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "mongodb://localhost:27017/")
DB_NAME = "jobify"

# Application settings
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

# NLP settings
NLP_MODEL = "en_core_web_md"  # spaCy model
DEFAULT_SIMILARITY_METHOD = "tfidf"  # Options: tfidf, spacy, word2vec

# Skills database path
SKILLS_DB_PATH = os.path.join(os.path.dirname(__file__), "../data/skills_db.json")
