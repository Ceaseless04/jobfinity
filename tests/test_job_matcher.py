import unittest
import os
import json
from collections import Counter
from models.job_matcher import JobMatcher

class TestJobMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = JobMatcher()

        # Load pre-parsed resume data from test_outputs directory
        self.resume_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../test_outputs")
        )
        self.resume_files = [f for f in os.listdir(self.resume_dir) if f.endswith(".json")]

        # Expanded and realistic job descriptions for broader testing
        self.job_descriptions = [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "Looking for a software engineer with experience in Python, JavaScript, ReactJS, Git, and Agile development. Strong communication and problem-solving skills are required."
            },
            {
                "title": "Data Scientist",
                "company": "Data Inc",
                "description": "Seeking a data scientist with expertise in machine learning, data analysis, statistics, Python, TensorFlow, and SQL. Must have experience presenting insights to stakeholders."
            },
            {
                "title": "Frontend Developer",
                "company": "Web Solutions",
                "description": "Need a frontend developer with advanced skills in HTML, CSS, JavaScript, React, Vue, and UI/UX principles. Knowledge of accessibility standards is a plus."
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudOps",
                "description": "Looking for a DevOps engineer experienced in Docker, Kubernetes, AWS, Terraform, Jenkins, Ansible, CI/CD pipelines, and system monitoring tools like Prometheus and Grafana."
            },
            {
                "title": "Backend Developer",
                "company": "Backendify",
                "description": "Searching for backend developers skilled in Django, Flask, SQL, PostgreSQL, REST APIs, caching strategies, and scalability patterns."
            },
            {
                "title": "Cloud Architect",
                "company": "SkyNet Solutions",
                "description": "We need a cloud architect with deep experience in Azure, AWS, GCP, Kubernetes, infrastructure as code, and secure cloud design patterns."
            },
            {
                "title": "QA Engineer",
                "company": "TestLabs",
                "description": "Hiring QA engineers proficient in manual testing, Selenium, JUnit, writing test plans, bug tracking, and continuous integration tools."
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Innovations",
                "description": "Looking for machine learning engineers with experience in Python, PyTorch, TensorFlow, model optimization, and deployment at scale."
            }
        ]

        self.matcher.preprocess_job_descriptions(self.job_descriptions)

    def test_bulk_resume_matching(self):
        failed = []
        top_match_counter = Counter()

        for file_name in self.resume_files:
            path = os.path.join(self.resume_dir, file_name)
            try:
                with open(path, "r") as f:
                    resume_data = json.load(f)

                job_matches = self.matcher.match_resume(resume_data)

                # Basic checks
                self.assertEqual(len(job_matches), len(self.job_descriptions))
                self.assertIn("similarity_score", job_matches[0])
                self.assertTrue(all(0 <= job["similarity_score"] <= 1 for job in job_matches))

                # Log top matches for the resume
                print(f"\nResume: {file_name}")
                for i, job in enumerate(job_matches[:3]):
                    print(f"  Match {i+1}: {job['title']} at {job['company']} (Score: {job['similarity_score']:.4f})")

                top_title = job_matches[0]["title"]
                top_match_counter[top_title] += 1

            except Exception as e:
                print(f"❌ Failed on {file_name}: {e}")
                failed.append(file_name)

        print(f"\n✅ Matched {len(self.resume_files) - len(failed)} / {len(self.resume_files)} resumes.")
        if failed:
            print("❌ Failed resumes:")
            for name in failed:
                print(f" - {name}")

        print("\n🔝 Top job title matches across all resumes:")
        for title, count in top_match_counter.most_common():
            print(f" - {title}: {count} matches")

        self.assertEqual(len(failed), 0, f"Some resumes failed to match: {failed}")

if __name__ == "__main__":
    unittest.main()
