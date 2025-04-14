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
                "company": "MockCorp",
                "description": "Experience with Python, JavaScript, and Agile development.",
                "location": "Remote",
                "url": "https://mockjob.com/job/001",
                "job_id": "mock001",
                "date_posted": "2025-04-12",
                "salary_min": 95000,
                "salary_max": 120000,
                "category": "IT Jobs",
            },
            {
                "title": "Data Scientist",
                "company": "DataGenix",
                "description": "Seeking expert in Python, Pandas, Scikit-learn, and data visualization.",
                "location": "New York, NY",
                "url": "https://mockjob.com/job/002",
                "job_id": "mock002",
                "date_posted": "2025-04-10",
                "salary_min": 100000,
                "salary_max": 130000,
                "category": "IT Jobs",
            },
            {
                "title": "Frontend Developer",
                "company": "PixelPushers",
                "description": "Expert in React, Tailwind CSS, and TypeScript. Strong UX mindset.",
                "location": "Austin, TX",
                "url": "https://mockjob.com/job/003",
                "job_id": "mock003",
                "date_posted": "2025-04-09",
                "salary_min": 85000,
                "salary_max": 110000,
                "category": "IT Jobs",
            },
            {
                "title": "Backend Engineer",
                "company": "ServerSide Solutions",
                "description": "Experience with Django, REST APIs, PostgreSQL, and containerized deployments.",
                "location": "Seattle, WA",
                "url": "https://mockjob.com/job/004",
                "job_id": "mock004",
                "date_posted": "2025-04-11",
                "salary_min": 95000,
                "salary_max": 125000,
                "category": "IT Jobs",
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudSmiths",
                "description": "Proficient with Kubernetes, CI/CD, Docker, Terraform, and AWS.",
                "location": "San Francisco, CA",
                "url": "https://mockjob.com/job/005",
                "job_id": "mock005",
                "date_posted": "2025-04-08",
                "salary_min": 110000,
                "salary_max": 140000,
                "category": "IT Jobs",
            },
            {
                "title": "Machine Learning Engineer",
                "company": "NeuroNet AI",
                "description": "TensorFlow, PyTorch, model deployment, and real-time inference pipelines.",
                "location": "Boston, MA",
                "url": "https://mockjob.com/job/006",
                "job_id": "mock006",
                "date_posted": "2025-04-10",
                "salary_min": 120000,
                "salary_max": 150000,
                "category": "IT Jobs",
            },
            {
                "title": "QA Automation Engineer",
                "company": "Testify QA",
                "description": "Automate test suites using Selenium, PyTest, and Jenkins CI.",
                "location": "Chicago, IL",
                "url": "https://mockjob.com/job/007",
                "job_id": "mock007",
                "date_posted": "2025-04-07",
                "salary_min": 80000,
                "salary_max": 100000,
                "category": "IT Jobs",
            },
            {
                "title": "Cloud Architect",
                "company": "SkyBuilders",
                "description": "Design scalable solutions on AWS, Azure, and GCP. IaC with Terraform.",
                "location": "Denver, CO",
                "url": "https://mockjob.com/job/008",
                "job_id": "mock008",
                "date_posted": "2025-04-06",
                "salary_min": 130000,
                "salary_max": 160000,
                "category": "IT Jobs",
            },
            {
                "title": "Full Stack Developer",
                "company": "StackSavvy",
                "description": "Skilled in MERN stack, REST/GraphQL APIs, Docker.",
                "location": "Miami, FL",
                "url": "https://mockjob.com/job/009",
                "job_id": "mock009",
                "date_posted": "2025-04-05",
                "salary_min": 90000,
                "salary_max": 115000,
                "category": "IT Jobs",
            },
            {
                "title": "Security Engineer",
                "company": "SecureNet",
                "description": "Experience with threat modeling, penetration testing, and incident response.",
                "location": "Washington, DC",
                "url": "https://mockjob.com/job/010",
                "job_id": "mock010",
                "date_posted": "2025-04-04",
                "salary_min": 105000,
                "salary_max": 135000,
                "category": "IT Jobs",
            },
            {
                "title": "Mobile App Developer",
                "company": "AppVerse",
                "description": "iOS/Android developer using Flutter and React Native.",
                "location": "Los Angeles, CA",
                "url": "https://mockjob.com/job/011",
                "job_id": "mock011",
                "date_posted": "2025-04-03",
                "salary_min": 85000,
                "salary_max": 110000,
                "category": "IT Jobs",
            },
            {
                "title": "Site Reliability Engineer",
                "company": "UptimeOps",
                "description": "Manage SLAs, observability, Prometheus, Grafana, and distributed systems.",
                "location": "Portland, OR",
                "url": "https://mockjob.com/job/012",
                "job_id": "mock012",
                "date_posted": "2025-04-02",
                "salary_min": 115000,
                "salary_max": 140000,
                "category": "IT Jobs",
            },
            {
                "title": "Data Engineer",
                "company": "Pipeline Pros",
                "description": "ETL pipelines, Airflow, BigQuery, Spark, and Kafka.",
                "location": "Atlanta, GA",
                "url": "https://mockjob.com/job/013",
                "job_id": "mock013",
                "date_posted": "2025-04-01",
                "salary_min": 100000,
                "salary_max": 130000,
                "category": "IT Jobs",
            },
            {
                "title": "AI Research Engineer",
                "company": "FutureAI Labs",
                "description": "Research LLMs, generative models, and NLP tasks using PyTorch and Transformers.",
                "location": "Remote",
                "url": "https://mockjob.com/job/014",
                "job_id": "mock014",
                "date_posted": "2025-03-30",
                "salary_min": 130000,
                "salary_max": 165000,
                "category": "IT Jobs",
            },
            {
                "title": "IT Support Specialist",
                "company": "HelpdeskPro",
                "description": "Windows, Linux support, ticketing systems, and end-user assistance.",
                "location": "Phoenix, AZ",
                "url": "https://mockjob.com/job/015",
                "job_id": "mock015",
                "date_posted": "2025-03-28",
                "salary_min": 60000,
                "salary_max": 80000,
                "category": "IT Jobs",
            },
            {
                "title": "Database Administrator",
                "company": "DataKeepers",
                "description": "Manage PostgreSQL, MySQL, backups, tuning, and data security.",
                "location": "Dallas, TX",
                "url": "https://mockjob.com/job/016",
                "job_id": "mock016",
                "date_posted": "2025-03-27",
                "salary_min": 90000,
                "salary_max": 115000,
                "category": "IT Jobs",
            },
            {
                "title": "UI/UX Designer",
                "company": "Designify",
                "description": "Figma, usability testing, user research, and accessibility standards.",
                "location": "Orlando, FL",
                "url": "https://mockjob.com/job/017",
                "job_id": "mock017",
                "date_posted": "2025-03-25",
                "salary_min": 75000,
                "salary_max": 95000,
                "category": "IT Jobs",
            },
            {
                "title": "Product Manager (Tech)",
                "company": "VisionStack",
                "description": "Agile/Scrum, product roadmaps, user stories, stakeholder communication.",
                "location": "San Diego, CA",
                "url": "https://mockjob.com/job/018",
                "job_id": "mock018",
                "date_posted": "2025-03-23",
                "salary_min": 110000,
                "salary_max": 140000,
                "category": "IT Jobs",
            },
            {
                "title": "Technical Writer",
                "company": "DocuFlow",
                "description": "API documentation, user guides, developer onboarding materials.",
                "location": "Remote",
                "url": "https://mockjob.com/job/019",
                "job_id": "mock019",
                "date_posted": "2025-03-20",
                "salary_min": 70000,
                "salary_max": 90000,
                "category": "IT Jobs",
            },
            {
                "title": "Game Developer",
                "company": "LevelUp Studios",
                "description": "Unity, C#, shader programming, and multiplayer networked games.",
                "location": "Salt Lake City, UT",
                "url": "https://mockjob.com/job/020",
                "job_id": "mock020",
                "date_posted": "2025-03-18",
                "salary_min": 95000,
                "salary_max": 115000,
                "category": "IT Jobs",
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
