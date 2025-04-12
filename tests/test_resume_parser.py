import unittest
import os
import json
from models.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        self.resume_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/sample_resumes/data/data/INFORMATION-TECHNOLOGY")
        )
        self.resume_files = [f for f in os.listdir(self.resume_dir) if f.endswith(".pdf")]

        # Optional: create output directory for logs
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_outputs"))
        os.makedirs(self.output_dir, exist_ok=True)

    def test_bulk_resume_parsing(self):
        failed_files = []

        for file_name in self.resume_files:
            file_path = os.path.join(self.resume_dir, file_name)
            try:
                with open(file_path, "rb") as file:
                    result = self.parser.parse_pdf(file)

                    # Assert result format
                    self.assertIsInstance(result, dict)
                    self.assertIn("skills", result)
                    self.assertIn("experience", result)
                    self.assertIn("education", result)

                    # Optional: log parsed results for review
                    output_file = os.path.join(self.output_dir, f"{file_name}.json")
                    with open(output_file, "w") as out:
                        json.dump(result, out, indent=2)

            except Exception as e:
                print(f"❌ Error parsing {file_name}: {e}")
                failed_files.append(file_name)

        total = len(self.resume_files)
        failed = len(failed_files)
        print(f"\n✅ Parsed {total - failed} of {total} resumes successfully. ❌ {failed} failed.")
        if failed:
            print("Failed files:")
            for name in failed_files:
                print(f" - {name}")

        self.assertEqual(failed, 0, f"{failed} resume(s) failed to parse.")

if __name__ == "__main__":
    unittest.main()

