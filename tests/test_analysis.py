"""Unit tests for the Student Performance Analytics System."""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from main import (
    DatasetError,
    SUBJECTS,
    analyze_students,
    assign_grade,
    load_dataset,
    summarize_subjects,
)


def sample_frame():
    return pd.DataFrame([
        {
            "Student_ID": "T001", "Student_Name": "Asha",
            "Mathematics": 90, "Python": 80, "Statistics": 70, "English": 60,
            "Attendance_Percent": 90,
        },
        {
            "Student_ID": "T002", "Student_Name": "Bala",
            "Mathematics": 35, "Python": 35, "Statistics": 35, "English": 34,
            "Attendance_Percent": 70,
        },
        {
            "Student_ID": "T003", "Student_Name": "Charu",
            "Mathematics": 90, "Python": 80, "Statistics": 70, "English": 60,
            "Attendance_Percent": 95,
        },
    ])


class GradeTests(unittest.TestCase):
    def test_grade_boundaries(self):
        self.assertEqual(assign_grade(100), "A+")
        self.assertEqual(assign_grade(90), "A+")
        self.assertEqual(assign_grade(89.99), "A")
        self.assertEqual(assign_grade(80), "A")
        self.assertEqual(assign_grade(70), "B")
        self.assertEqual(assign_grade(60), "C")
        self.assertEqual(assign_grade(50), "D")
        self.assertEqual(assign_grade(49.99), "F")
        self.assertEqual(assign_grade(0), "F")


class AnalysisTests(unittest.TestCase):
    def test_totals_averages_and_results(self):
        result = analyze_students(sample_frame()).set_index("Student_ID")
        self.assertEqual(result.loc["T001", "Total_Marks"], 300)
        self.assertEqual(result.loc["T001", "Average_Marks"], 75.0)
        self.assertEqual(result.loc["T001", "Result"], "Pass")
        self.assertEqual(result.loc["T002", "Result"], "Fail")

    def test_tied_students_share_rank(self):
        result = analyze_students(sample_frame()).set_index("Student_ID")
        self.assertEqual(result.loc["T001", "Rank"], result.loc["T003", "Rank"])

    def test_subject_summary_has_all_subjects(self):
        summary = summarize_subjects(sample_frame())
        self.assertEqual(set(summary["Subject"]), set(SUBJECTS))
        self.assertEqual(len(summary), 4)

    def test_invalid_marks_are_rejected(self):
        data = sample_frame()
        data.loc[0, "Mathematics"] = 101
        with self.assertRaises(DatasetError):
            analyze_students(data)

    def test_duplicate_ids_are_rejected(self):
        data = sample_frame()
        data.loc[1, "Student_ID"] = "T001"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.csv"
            data.to_csv(path, index=False)
            with self.assertRaises(DatasetError):
                load_dataset(path)

    def test_missing_column_is_rejected(self):
        data = sample_frame().drop(columns=["English"])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.csv"
            data.to_csv(path, index=False)
            with self.assertRaises(DatasetError):
                load_dataset(path)


if __name__ == "__main__":
    unittest.main()
