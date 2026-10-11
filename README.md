# Student Performance Analytics System

A beginner-friendly academic data-analysis project built with **Python, NumPy, and Pandas**. It analyzes fictional student marks and attendance, assigns grades, identifies pass/fail status, ranks students, and exports CSV reports.

## Features

- Loads and validates student data from CSV.
- Checks required columns, missing/non-numeric values, duplicate student IDs, and score ranges.
- Calculates total and average marks for four subjects.
- Assigns grades using documented average-mark thresholds.
- Marks a student as Pass only when every subject score is at least 35/100.
- Ranks students, preserving tied ranks.
- Summarizes class results, attendance, and subject-level averages/highest/lowest marks.
- Exports detailed results and subject summaries to CSV.

## Project files

- `main.py` — analysis program.
- `students.csv` — 20 fictional sample records.
- `tests/test_analysis.py` — automated tests for core logic.
- `PROJECT_DOCUMENTATION.md` — methodology, rules, and limitations.
- `requirements.txt` — required Python libraries.

## Run on Android or a computer

1. Install Python and the packages in `requirements.txt`. In Pydroid 3, install NumPy and Pandas through its package/Pip tools if they are not already installed.
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

   ```bash
   python main.py
   ```

   Optional arguments:

   ```bash
   python main.py --input students.csv --output-dir reports
   ```

4. Find generated files in `reports/student_results.csv` and `reports/subject_summary.csv`.

If running in Google Colab, upload `main.py` and `students.csv` into the same notebook working directory, then run `!python main.py`.

## Grading rules

| Average mark | Grade |
|---:|:---|
| 90–100 | A+ |
| 80–<90 | A |
| 70–<80 | B |
| 60–<70 | C |
| 50–<60 | D |
| <50 | F |

**Pass rule:** every subject must have a score of at least 35/100. Attendance is summarized separately and does not alter marks or grades. These are project-defined rules, not universal institutional standards.

## Testing

Run the test suite from the project folder:

```bash
python -m unittest discover -s tests -v
```

## Data and academic integrity

All names and records in `students.csv` are fictional sample data for demonstration. Replace them only with data you are authorized to use. Do not upload private student information to a public repository.

## Scope and limitations

This is a command-line analytics project, not a machine-learning prediction system. It reports descriptive statistics from the supplied records; it does not infer causes or predict future grades.
