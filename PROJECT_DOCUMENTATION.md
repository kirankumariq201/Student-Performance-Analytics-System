# Project Documentation
## Student Performance Analytics System

### 1. Introduction
The Student Performance Analytics System is a Python-based data-analysis project. It uses Pandas to load and organize student records and NumPy for numerical calculations. The system produces understandable summaries of marks, grades, results, rankings, subject averages, and attendance.

### 2. Objective
- Organize student academic records in a structured CSV file.
- Apply Python functions, conditions, and data validation.
- Use Pandas DataFrames for data handling and analysis.
- Use NumPy for numerical calculations.
- Summarize academic performance to make the records easier to interpret.

### 3. Tools and technologies
- Python 3
- Pandas
- NumPy
- CSV as the input/output data format
- GitHub for version control and project sharing

Install dependencies with `python -m pip install -r requirements.txt`.

### 4. Dataset description
The sample dataset contains 20 fictional student records. Each row has a student ID, student name, marks in Mathematics, Python, Statistics, and English (each out of 100), and attendance percentage (0–100). The data is illustrative and does not represent real students.

### 5. Methodology
1. Read the CSV file into a Pandas DataFrame.
2. Verify that all required columns exist and that identifiers, names, marks, and attendance are valid.
3. Calculate each student's total and mean marks across four subjects.
4. Map the mean to the project's grading thresholds.
5. Assign Pass only if every subject mark is at least 35; otherwise assign Fail.
6. Rank by average marks, assigning equal ranks to tied averages.
7. Calculate subject-level averages, maximums, and minimums using NumPy.
8. Display a console report and export two CSV reports.

### 6. Grade and pass rules
| Average mark | Grade |
|---:|:---|
| 90–100 | A+ |
| 80–<90 | A |
| 70–<80 | B |
| 60–<70 | C |
| 50–<60 | D |
| Below 50 | F |

A student passes when all four subject marks are at least 35/100. Attendance is analyzed separately and does not affect grades. These are explicit rules selected for this project; an institution's actual grading policy may differ.

### 7. Outputs
- A ranked student table containing total marks, average, grade, pass/fail result, and rank.
- Class average, pass count, fail count, and average attendance.
- Subject summary sorted by average marks.
- Top five rank positions, including ties at the cutoff.
- `reports/student_results.csv` and `reports/subject_summary.csv`.

### 8. Validation and testing
The program checks for missing required columns, empty data, blank identifiers/names, duplicate student IDs, non-numeric values, non-finite numbers, and marks/attendance outside the 0–100 range. Automated tests cover grade boundaries, pass/fail rules, ranking, subject summaries, and invalid data. Run them using:

```bash
python -m unittest discover -s tests -v
```

### 9. Limitations
The results depend on the supplied dataset and chosen grading rules. The project performs descriptive analysis only; it does not predict outcomes, establish causation, or use machine learning. Attendance is not used to modify marks.

### 10. Learning outcomes
This project demonstrates practical use of Python functions and conditionals, CSV data, Pandas DataFrames, NumPy calculations, input validation, sorting/ranking, CSV report generation, automated testing, and GitHub documentation.

### 11. Conclusion
The Student Performance Analytics System converts structured student records into useful summaries and individual results. Its modular functions and validation checks make the program easier to test, understand, and extend.

### 12. Academic integrity and privacy
The included dataset is fictional. Any real student data must be used only with appropriate authorization and handled according to applicable privacy requirements.
