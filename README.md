# PS 44 – Student Attendance & Performance Tracker

**Rungta International Skills University – BCA (School of Information Technology)**
**Language:** Python 3 | **Libraries:** Pandas, Matplotlib

## Problem Statement
Analyse student attendance and marks from a CSV file, calculate attendance
percentage, identify students at risk and present the results with charts.
A student is **At Risk** if attendance is below **75%** or marks are below **40**.

## CSV Format
`Name, Classes_Held, Classes_Attended, Marks` (marks out of 100)

## How to Run
```
pip install pandas matplotlib
python attendance_tracker.py students.csv
```
Menu: `1` Report | `2` Summary and charts | `3` Exit

## Features
- Loads CSV using Pandas and cleans invalid rows (non-numeric values, attended > held,
  held <= 0, negative values, marks outside 0-100, missing name, missing file/columns)
- Attendance % = Classes_Attended / Classes_Held x 100 (Pandas column calculation)
- Boolean filtering to find At Risk students and calculate averages
- Two Matplotlib charts with title and labels: bar chart (attendance) and scatter chart (Attendance vs Marks)
- Charts are also saved as `bar_chart_attendance.png` and `scatter_attendance_vs_marks.png`

## Test Cases (files in `test_data/`)
| # | File | Menu | Result |
|---|------|------|--------|
| 1 | test_case_1_normal.csv | 1 | Aman 90.00% OK; Riya 70.00% At Risk (attendance); Karan 75.00% At Risk (marks) |
| 2 | test_case_2_boundary.csv | 1 | Neha 75.00% / Marks 40 -> OK |
| 3 | test_case_3_invalid.csv | 1 | Row 1 skipped (attended 45 > held 40); Row 2 skipped (invalid Marks 'abc'); No valid data to analyse |
| 4 | test_case_4_valid.csv | 2 | Avg attendance 78.33%, Avg marks 60.00, 2 At Risk (Riya, Karan), both charts shown |

Run a test: `python attendance_tracker.py test_data/test_case_3_invalid.csv`
