"""
PS 44 - Student Attendance & Performance Tracker
Rungta International Skills University - BCA

Reads student data from a CSV file, calculates attendance percentage,
identifies At Risk students (attendance < 75% OR marks < 40),
and shows the results with Matplotlib charts.

CSV columns: Name, Classes_Held, Classes_Attended, Marks (out of 100)

Usage:  python attendance_tracker.py [csv_file]     (default: students.csv)
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

ATTENDANCE_LIMIT = 75   # minimum attendance percentage
MARKS_LIMIT = 40        # minimum marks
REQUIRED_COLUMNS = ["Name", "Classes_Held", "Classes_Attended", "Marks"]


# ---------------------------------------------------------------- loading
def load_and_clean(filename):
    """Load the CSV with Pandas and remove invalid rows.
    Returns a clean DataFrame (may be empty)."""
    try:
        raw = pd.read_csv(filename, dtype=str, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("Error: the CSV file is empty.")
        return pd.DataFrame()

    raw.columns = [c.strip() for c in raw.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        print("Error: missing column(s):", ", ".join(missing))
        return pd.DataFrame()

    good_rows = []
    for number, row in enumerate(raw.to_dict("records"), start=1):
        name = str(row["Name"]).strip()
        if name == "" or name.lower() == "nan":
            print(f"Row {number} skipped: Name is missing.")
            continue

        # check that the three numeric fields are valid numbers
        values, bad = {}, False
        for col in ["Classes_Held", "Classes_Attended", "Marks"]:
            text = str(row[col]).strip()
            try:
                values[col] = float(text)
            except ValueError:
                label = col.replace("_", " ")
                shown = "" if text.lower() == "nan" else text
                print(f"Row {number} skipped: invalid {label} '{shown}'.")
                bad = True
                break
        if bad:
            continue

        held, attended, marks = (values["Classes_Held"],
                                 values["Classes_Attended"], values["Marks"])
        if held <= 0:
            print(f"Row {number} skipped: classes held ({held:g}) must be above 0.")
        elif attended < 0:
            print(f"Row {number} skipped: classes attended ({attended:g}) cannot be negative.")
        elif attended > held:
            print(f"Row {number} skipped: attended ({attended:g}) cannot exceed held ({held:g}).")
        elif marks < 0 or marks > 100:
            print(f"Row {number} skipped: Marks ({marks:g}) must be between 0 and 100.")
        else:
            good_rows.append({"Name": name, "Classes_Held": held,
                              "Classes_Attended": attended, "Marks": marks})

    df = pd.DataFrame(good_rows, columns=REQUIRED_COLUMNS)
    if df.empty:
        return df

    # Attendance percentage using Pandas columns (vectorised)
    df["Attendance_%"] = df["Classes_Attended"] / df["Classes_Held"] * 100
    # Boolean flags used for filtering
    df["Low_Attendance"] = df["Attendance_%"] < ATTENDANCE_LIMIT
    df["Low_Marks"] = df["Marks"] < MARKS_LIMIT
    df["At_Risk"] = df["Low_Attendance"] | df["Low_Marks"]
    return df


# ---------------------------------------------------------------- report
def status_text(row):
    """Return the status string for one student."""
    if row["Low_Attendance"]:
        return f"At Risk (attendance below {ATTENDANCE_LIMIT}%)"
    if row["Low_Marks"]:
        return f"At Risk (marks below {MARKS_LIMIT})"
    return "OK"


def show_report(df):
    """Menu option 1 - one line per student."""
    if df.empty:
        print("No valid data to analyse.")
        return
    print("\n--- Attendance & Performance Report ---")
    for _, row in df.iterrows():
        print(f"{row['Name']}: {row['Attendance_%']:.2f}% | "
              f"Marks {row['Marks']:g} | {status_text(row)}")


# ---------------------------------------------------------------- summary
def show_summary(df):
    """Menu option 2 - averages, at risk list and two charts."""
    if df.empty:
        print("No valid data to analyse.")
        return

    at_risk = df[df["At_Risk"]]            # boolean filtering
    names = ", ".join(at_risk["Name"]) if not at_risk.empty else "None"

    print("\n--- Summary ---")
    print(f"Average attendance: {df['Attendance_%'].mean():.2f}% | "
          f"Average marks: {df['Marks'].mean():.2f}")
    print(f"At Risk students: {len(at_risk)} ({names})")
    print("Bar chart and scatter chart 'Attendance vs Marks' displayed")

    colours = ["red" if r else "green" for r in df["At_Risk"]]

    # Chart 1 - bar chart of attendance
    plt.figure(figsize=(7, 5))
    plt.bar(df["Name"], df["Attendance_%"], color=colours)
    plt.axhline(ATTENDANCE_LIMIT, color="orange", linestyle="--",
                label=f"{ATTENDANCE_LIMIT}% limit")
    plt.title("Attendance Percentage of Students")
    plt.xlabel("Student Name")
    plt.ylabel("Attendance (%)")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig("bar_chart_attendance.png")

    # Chart 2 - scatter chart of attendance vs marks
    plt.figure(figsize=(7, 5))
    plt.scatter(df["Attendance_%"], df["Marks"], c=colours, s=90)
    for _, row in df.iterrows():
        plt.annotate(row["Name"], (row["Attendance_%"], row["Marks"]),
                     textcoords="offset points", xytext=(6, 6))
    plt.axvline(ATTENDANCE_LIMIT, color="orange", linestyle="--")
    plt.axhline(MARKS_LIMIT, color="purple", linestyle="--")
    plt.title("Attendance vs Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Marks (out of 100)")
    plt.tight_layout()
    plt.savefig("scatter_attendance_vs_marks.png")

    plt.show()


# ---------------------------------------------------------------- main
def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "students.csv"
    df = load_and_clean(filename)

    while True:
        print("\n===== Student Attendance & Performance Tracker =====")
        print("1. Report")
        print("2. Summary and charts")
        print("3. Exit")
        try:
            choice = input("Enter your choice (1-3): ").strip()
        except EOFError:
            break
        if choice == "1":
            show_report(df)
        elif choice == "2":
            show_summary(df)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
