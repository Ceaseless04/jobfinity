# Jobify - AI-Powered Resume Analyzer

## 🚀 Welcome to Jobify!

Jobify is an AI-powered resume analyzer that helps CS students find more accurate job matches based on their interests and resume content. Our platform uses advanced NLP and machine learning techniques to parse resumes and provide tailored job recommendations.

## 👥 Team Members

- **Kristian Vazquez**: Team Lead / ML Engineer / Full-Stack Dev
- **Miguel Garcia**: ML Engineer / Full-Stack Dev
- **Alejandro Garcia**: ML / Full-Stack Dev
- **Elijah Chin**: Backend & Frontend Developer
- **Baire Diaz**: Backend & Frontend Developer

## 🎯 Project Objectives

- Build an ML model that can accurately parse user resumes
- Provide job recommendations based on users' skills, experience, and interests
- Create an intuitive, aesthetically pleasing UI with Streamlit
- Implement advanced NLP techniques for better job matching

## 🛠️ Tech Stack

- **Frontend**: Streamlit, HTML, CSS
- **Backend**: Python
- **Database**: MongoDB
- **ML & NLP Libraries**: 
  - pyresparser, pdfminer3
  - NLTK, spaCy
  - scikit-learn, TensorFlow/PyTorch
  - TF-IDF, Word2Vec, GloVe

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jobify.git
   cd jobify
   ```

2. **Create and activate a virtual environment**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   
   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install NLTK data**
   ```python
   # Run this in Python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

5. **Set up MongoDB**
   - Install MongoDB Community Edition from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Start the MongoDB service
   - Update the connection string in `config.py` if necessary

6. **Run the application**
   ```bash
   cd src
   streamlit run app.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:8501`

## 📁 Project Structure

```
jobify/
├── README.md                 # Project overview
├── requirements.txt          # Dependencies
├── data/                     # Sample data for testing
│   ├── sample_resumes/
│   └── sample_job_descriptions/
├── models/                   # ML models
│   ├── resume_parser.py
│   └── job_matcher.py
├── src/                      # Source code
│   ├── app.py                # Main Streamlit application
│   ├── config.py             # Configuration settings
│   ├── utils/                # Utility functions
│   └── components/           # Streamlit UI components
├── database/                 # Database connectors
└── tests/                    # Unit and integration tests
```

## ⚙️ Development Workflow

1. **Pull the latest changes**
   ```bash
   git pull origin main
   ```

2. **Create a new branch for your feature**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit them**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

4. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request on GitHub**
   - Navigate to the repository on GitHub
   - Click on "Pull Requests" and then "New Pull Request"
   - Select your branch and create the PR with a description of your changes

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 📊 Project Milestones

1. **Data Collection** - Gather sample resumes and job descriptions
2. **Repository Setup** - Initialize project structure and version control
3. **Frontend Prototype** - Develop initial Streamlit UI
4. **Model Prototype** - Implement basic resume parsing and job matching
5. **Model Fine-tuning** - Improve model accuracy and performance
6. **Job Recommendation Integration** - Connect with job APIs and implement recommendation logic

## 📋 Weekly Meetings

- We follow a sprint model with weekly standups
- Each team member reports on:
  - What they accomplished since the last meeting
  - What they plan to work on next
  - Any blockers or challenges they're facing

## 🔍 Documentation Resources

- **ML Model Documentation**: Check `/docs/ml_models.md` for details on our ML pipeline
- **API Documentation**: Check `/docs/api.md` for API endpoint details
- **UI Components**: Check `/docs/ui_components.md` for UI component documentation

## 🤝 Contributing Guidelines

1. Follow PEP 8 style guidelines for Python code
2. Write meaningful commit messages
3. Update documentation alongside code changes
4. Add unit tests for new functionality
5. Conduct code reviews for all PRs

## 🔗 Useful Links

- [Project Proposal Document](docs/proposal.pdf)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [spaCy Documentation](https://spacy.io/usage)
- [LinkedIn Jobs API Documentation](https://developer.linkedin.com/docs/jobs-api)

## 🆘 Getting Help

If you're stuck or have questions:
1. Check the project documentation
2. Ask in the team Slack channel
3. Reach out to the responsible team member based on the component you're working on
4. Contact Kristian (Team Lead) for overall project questions

---

Happy coding! Let's build something amazing together! 🚀
