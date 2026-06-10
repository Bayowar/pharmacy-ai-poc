import ollama
import pandas as pd
from datetime import date

MODEL = "llama3.2:3b"

# Define the staff roster
# This should come from HR system
# Roles: Pharmacist, Compounder, Technician, Admin
staff = [
    {"name": "Alice Morgan",   "role": "Pharmacist",  "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
    {"name": "Bob Chen",       "role": "Pharmacist",  "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
    {"name": "Carmen Diaz",    "role": "Compounder",  "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
    {"name": "Rodney Cabrera Joseph",      "role": "Compounder",  "max_hours": 40, "days": ["Tue","Wed","Thu","Fri","Sat"]},
    {"name": "Bayowa O",    "role": "Compounder",  "max_hours": 32, "days": ["Mon","Wed","Fri","Sat"]},
    {"name": "Frank Lopez",    "role": "Technician",  "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
    {"name": "Bayowa O",      "role": "Technician",  "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
    {"name": "Henry Brown",    "role": "Technician",  "max_hours": 32, "days": ["Mon","Wed","Thu","Sat"]},
    {"name": "Janee White",  "role": "Technician",  "max_hours": 40, "days": ["Tue","Wed","Thu","Fri","Sat"]},
    {"name": "James Wilson",   "role": "Admin",       "max_hours": 40, "days": ["Mon","Tue","Wed","Thu","Fri"]},
]

# Working days of the week
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Hours per shift
SHIFT_HOURS = 8

#Build the weekly schedule 
def build_schedule(staff, days):
    schedule = []

    for day in days:
        for person in staff:
            if day in person["days"]:
                schedule.append({
                    "Day": day,
                    "Name": person["name"],
                    "Role": person["role"],
                    "Hours": SHIFT_HOURS
                })

    return pd.DataFrame(schedule)

#Calculate weekly hours per person 
def calculate_hours(df):
    hours = df.groupby(["Name", "Role"])["Hours"].sum().reset_index()
    hours.columns = ["Name", "Role", "Total Hours"]
    return hours

#Flag overtime risks
def flag_overtime(hours_df, staff):
    flags = []

    for _, row in hours_df.iterrows():
        # Find this person's max hours from staff roster
        person = next(p for p in staff if p["name"] == row["Name"])
        scheduled = row["Total Hours"]
        maximum = person["max_hours"]

        if scheduled > maximum:
            flags.append(row["Name"] + " is OVER by " + str(scheduled - maximum) + " hours")
        elif scheduled == maximum:
            flags.append(row["Name"] + " is AT maximum (" + str(maximum) + " hrs)")
        else:
            flags.append(row["Name"] + " is OK (" + str(scheduled) + "/" + str(maximum) + " hrs)")

    return flags

#Print the full schedule table
def print_schedule(df):
    print("\n" + "=" * 60)
    print("WEEKLY STAFF SCHEDULE")
    print("Week of: " + date.today().strftime("%B %d %Y"))
    print("=" * 60)

    for day in days_of_week:
        day_staff = df[df["Day"] == day]
        if not day_staff.empty:
            print("\n" + day + ":")
            print("-" * 40)
            for _, row in day_staff.iterrows():
                print("  {:<20} {}".format(row["Name"], row["Role"]))

#Ask AI for scheduling recommendation
def generate_schedule_report(hours_df, flags):
    hours_summary = hours_df.to_string(index=False)
    flags_summary = "\n".join(flags)

    prompt = (
        "You are a pharmacy operations manager. "
        "Review this weekly staff schedule and hours, "
        "then write a 4 sentence recommendation covering: "
        "workload balance, overtime risks, coverage gaps, and one improvement suggestion. "
        "\n\nHours per staff member:\n" + hours_summary +
        "\n\nOvertime flags:\n" + flags_summary
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

#Run
if __name__ == "__main__":
    print("Building weekly pharmacy staff schedule...")

    # Build schedule
    schedule_df = build_schedule(staff, days_of_week)

    # Print schedule
    print_schedule(schedule_df)

    # Calculate hours
    hours_df = calculate_hours(schedule_df)

    # Print hours summary
    print("\n" + "=" * 60)
    print("WEEKLY HOURS SUMMARY")
    print("=" * 60)
    print(hours_df.to_string(index=False))

    # Flag overtime
    flags = flag_overtime(hours_df, staff)
    print("\n" + "=" * 60)
    print("OVERTIME FLAGS")
    print("=" * 60)
    for flag in flags:
        print("  " + flag)

    # Total labor hours
    total_hours = hours_df["Total Hours"].sum()
    print("\nTotal scheduled hours this week: " + str(total_hours))

    # AI recommendation
    print("\nGenerating AI scheduling recommendation...")
    report = generate_schedule_report(hours_df, flags)

    print("\n" + "=" * 60)
    print("AI SCHEDULING RECOMMENDATION")
    print("=" * 60)
    print(report)