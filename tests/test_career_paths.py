import unittest
import os
import json
from models.job_matcher import JobMatcher
from models.career_path import CareerPathRecommender

class TestCareerPathRecommender(unittest.TestCase):
    def setUp(self):
        self.resume_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../test_outputs")
        )
        self.resume_files = [f for f in os.listdir(self.resume_dir) if f.endswith(".json")]

        with open(os.path.join(os.path.dirname(__file__), "../tests/sample_jobs.json"), "r") as f:
            self.sample_jobs = json.load(f)

        self.matcher = JobMatcher()
        self.matcher.preprocess_job_descriptions(self.sample_jobs)

    def test_recommend_career_paths_from_resume(self):
        for file_name in self.resume_files:
            resume_path = os.path.join(self.resume_dir, file_name)
            with open(resume_path, 'r') as f:
                resume_data = json.load(f)

            matched_jobs = self.matcher.match_resume(resume_data)[:20]

            recommender = CareerPathRecommender(matched_jobs)
            recommendations = recommender.recommend_career_paths(resume_data)

            print(f"\nCareer path recommendations for: {file_name}")
            for rec in recommendations:
                print(f" - {rec['path_name']} (Score: {rec['similarity_score']:.2f}%)")

            self.assertEqual(len(recommendations), 4)
            self.assertTrue(all("similarity_score" in r for r in recommendations))
            self.assertTrue(all(r["similarity_score"] < 100.0 for r in recommendations))

if __name__ == "__main__":
    unittest.main()

