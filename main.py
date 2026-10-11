"""Student Performance Analytics System.

Analyze student marks and attendance using Python, NumPy, and Pandas.
Run: python main.py
Optional: python main.py --input students.csv --output-dir reports
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ID_COLUMN = "Student_ID"
NAME_COLUMN = "Student_Name"
SUBJECTS = ["Mathematics", "Python", "Statistics", "English"]
ATTENDANCE_COLUMN = "Attendance_Percent"
REQUIRED_COLUMNS = [ID_COLUMN, NAME_COLUMN, *SUBJECTS, ATTENDANCE_COLUMN]


class DatasetError(ValueError):
    """Raised when the input dataset does not meet project requirements."""


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    """Load and validate a student CSV dataset."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise DatasetError("The CSV file is empty.") from exc
    except pd.errors.ParserError as exc:
        raise DatasetError(f"Could not parse CSV file: {exc}") from exc

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise DatasetError("Missing required column(s): " + ", ".join(missing_columns))
    if df.empty:
        raise DatasetError("The dataset must contain at least one student record.")

    df = df[REQUIRED_COLUMNS].copy()
    if df[ID_COLUMN].isna().any() or df[NAME_COLUMN].isna().any():
        raise DatasetError("Student IDs and names cannot be blank.")
    df[ID_COLUMN] = df[ID_COLUMN].astype(str).str.strip()
    df[NAME_COLUMN] = df[NAME_COLUMN].astype(str).str.strip()
    if (df[ID_COLUMN] == "").any() or (df[NAME_COLUMN] == "").any():
        raise DatasetError("Student IDs and names cannot be blank.")
    if df[ID_COLUMN].duplicated().any():
        duplicates = df.loc[df[ID_COLUMN].duplicated(), ID_COLUMN].tolist()
        raise DatasetError(f"Student IDs must be unique. Duplicate(s): {duplicates}")

    numeric_columns = [*SUBJECTS, ATTENDANCE_COLUMN]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    if df[numeric_columns].isna().any().any():
        raise DatasetError("Marks and attendance must contain valid numeric values.")
    if not np.isfinite(df[numeric_columns].to_numpy(dtype=float)).all():
        raise DatasetError("Marks and attendance must be finite numbers.")
    for subject in SUBJECTS:
        if not df[subject].between(0, 100).all():
            raise DatasetError(f"{subject} marks must be between 0 and 100.")
    if not df[ATTENDANCE_COLUMN].between(0, 100).all():
        raise DatasetError("Attendance_Percent must be between 0 and 100.")
    return df


def assign_grade(average: float) -> str:
    """Return a grade using the documented average-mark thresholds."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"


def analyze_students(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with totals, averages, grades, pass status, and rank."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise DatasetError("Missing required column(s): " + ", ".join(missing_columns))
    result = df.copy()
    marks = result[SUBJECTS].apply(pd.to_numeric, errors="coerce")
    if marks.isna().any().any() or not marks.apply(lambda col: col.between(0, 100).all()).all():
        raise DatasetError("All subject marks must be numeric values between 0 and 100.")

    result["Total_Marks"] = marks.sum(axis=1)
    result["Average_Marks"] = marks.mean(axis=1).round(2)
    result["Grade"] = result["Average_Marks"].map(assign_grade)
    result["Result"] = np.where(marks.ge(35).all(axis=1), "Pass", "Fail")
    # method='min' gives tied students the same rank without arbitrarily breaking ties.
    result["Rank"] = result["Average_Marks"].rank(method="min", ascending=False).astype(int)
    return result.sort_values(["Rank", NAME_COLUMN]).reset_index(drop=True)


def summarize_subjects(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize subject averages and score ranges."""
    rows = []
    for subject in SUBJECTS:
        scores = pd.to_numeric(df[subject], errors="coerce")
        rows.append({
            "Subject": subject,
            "Average_Marks": round(float(np.mean(scores)), 2),
            "Highest_Marks": float(np.max(scores)),
            "Lowest_Marks": float(np.min(scores)),
        })
    return pd.DataFrame(rows).sort_values("Average_Marks", ascending=False).reset_index(drop=True)


def print_report(analysis: pd.DataFrame, subject_summary: pd.DataFrame) -> None:
    """Print readable summaries to the terminal."""
    print("\n" + "=" * 64)
    print("          STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 64)
    print(f"Students analyzed: {len(analysis)}")
    print(f"Class average: {analysis['Average_Marks'].mean():.2f}/100")
    print(f"Pass count: {(analysis['Result'] == 'Pass').sum()}")
    print(f"Fail count: {(analysis['Result'] == 'Fail').sum()}")
    print(f"Average attendance: {analysis[ATTENDANCE_COLUMN].mean():.2f}%")

    print("\nSTUDENT RESULTS (sorted by rank)")
    columns = [ID_COLUMN, NAME_COLUMN, "Total_Marks", "Average_Marks", "Grade", "Result", "Rank"]
    print(analysis[columns].to_string(index=False))

    print("\nSUBJECT SUMMARY (highest average first)")
    print(subject_summary.to_string(index=False))

    print("\nTOP PERFORMERS (top five rank positions, including ties)")
    cutoff = min(5, len(analysis))
    top = analysis[analysis["Rank"] <= cutoff][[ID_COLUMN, NAME_COLUMN, "Average_Marks", "Grade", "Rank"]]
    print(top.to_string(index=False))
    print("=" * 64)


def save_reports(analysis: pd.DataFrame, subject_summary: pd.DataFrame, output_dir: str | Path) -> None:
    """Save analysis tables as CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    analysis.to_csv(output_path / "student_results.csv", index=False)
    subject_summary.to_csv(output_path / "subject_summary.csv", index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze student marks and attendance.")
    parser.add_argument("--input", default="students.csv", help="Path to the input CSV (default: students.csv)")
    parser.add_argument("--output-dir", default="reports", help="Folder for generated CSV reports (default: reports)")
    args = parser.parse_args()

    try:
        students = load_dataset(args.input)
        if len(students) < 15:
            print(f"Warning: dataset has {len(students)} records; the assignment target is at least 15–20.")
        analysis = analyze_students(students)
        subject_summary = summarize_subjects(students)
        print_report(analysis, subject_summary)
        save_reports(analysis, subject_summary, args.output_dir)
        print(f"\nReports saved to: {Path(args.output_dir).resolve()}")
        return 0
    except (DatasetError, FileNotFoundError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
