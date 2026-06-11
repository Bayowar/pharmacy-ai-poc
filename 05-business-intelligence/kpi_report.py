import ollama
from datetime import date

MODEL = "llama3.2:3b"

#Define this month's KPI data ---
# This would pull from the POS or billing system
# For this POC we use realistic sample data
kpis = {
    "report_date": date.today().strftime("%B %d %Y"),
    "report_period": "June 2026",

    # Sales metrics
    "b12_units_sold": 1240,
    "total_revenue_usd": 18600,
    "revenue_vs_last_month": "+12%",
    "average_order_value": 15,

    # Prescriber metrics
    "active_prescribers": 18,
    "top_prescriber": "Dr. Sarah Kim (142 scripts)",
    "new_prescribers_this_month": 3,
    "lost_prescribers_this_month": 1,

    # Inventory metrics
    "batches_compounded_this_month": 38,
    "units_wasted_expired": 24,
    "low_stock_alert": "Methylcobalamin API less than 2 week supply",
    "inventory_value_usd": 4200,

    # Staff metrics
    "total_staff": 10,
    "overtime_hours_this_month": 14,
    "open_shifts": 2,

    # Patient metrics
    "active_patients": 312,
    "new_patients_this_month": 28,
    "refill_rate_percent": 73,
    "patients_overdue_refill": 41,
}

# Print the KPI dashboard 
def print_kpi_dashboard(kpis):
    print("\n" + "=" * 60)
    print("PHARMACY KPI DASHBOARD")
    print("Report Date: " + kpis["report_date"])
    print("Period: " + kpis["report_period"])
    print("=" * 60)

    print("\n--- SALES ---")
    print("  B12 Units Sold:          " + str(kpis["b12_units_sold"]))
    print("  Total Revenue:           $" + str(kpis["total_revenue_usd"]))
    print("  vs Last Month:           " + kpis["revenue_vs_last_month"])
    print("  Avg Order Value:         $" + str(kpis["average_order_value"]))

    print("\n--- PRESCRIBERS ---")
    print("  Active Prescribers:      " + str(kpis["active_prescribers"]))
    print("  Top Prescriber:          " + kpis["top_prescriber"])
    print("  New This Month:          " + str(kpis["new_prescribers_this_month"]))
    print("  Lost This Month:         " + str(kpis["lost_prescribers_this_month"]))

    print("\n--- INVENTORY ---")
    print("  Batches Compounded:      " + str(kpis["batches_compounded_this_month"]))
    print("  Units Wasted/Expired:    " + str(kpis["units_wasted_expired"]))
    print("  Inventory Value:         $" + str(kpis["inventory_value_usd"]))
    print("  LOW STOCK ALERT:         " + kpis["low_stock_alert"])

    print("\n--- STAFF ---")
    print("  Total Staff:             " + str(kpis["total_staff"]))
    print("  Overtime Hours:          " + str(kpis["overtime_hours_this_month"]))
    print("  Open Shifts:             " + str(kpis["open_shifts"]))

    print("\n--- PATIENTS ---")
    print("  Active Patients:         " + str(kpis["active_patients"]))
    print("  New This Month:          " + str(kpis["new_patients_this_month"]))
    print("  Refill Rate:             " + str(kpis["refill_rate_percent"]) + "%")
    print("  Overdue for Refill:      " + str(kpis["patients_overdue_refill"]))

# Write an executive summary
def generate_executive_summary(kpis):
    prompt = (
        "You are a pharmacy business analyst writing a monthly report "
        "for the pharmacy owner. Based on these KPIs, write a professional "
        "executive summary in 5 sentences. Cover: overall performance, "
        "biggest win, biggest risk, and one clear action item. "
        "Be specific and use the actual numbers provided. "
        "\n\nKPI Data:\n"
        "Period: " + kpis["report_period"] + "\n"
        "B12 units sold: " + str(kpis["b12_units_sold"]) + "\n"
        "Total revenue: $" + str(kpis["total_revenue_usd"]) + "\n"
        "Revenue change vs last month: " + kpis["revenue_vs_last_month"] + "\n"
        "Active prescribers: " + str(kpis["active_prescribers"]) + "\n"
        "New prescribers: " + str(kpis["new_prescribers_this_month"]) + "\n"
        "Top prescriber: " + kpis["top_prescriber"] + "\n"
        "Batches compounded: " + str(kpis["batches_compounded_this_month"]) + "\n"
        "Units wasted: " + str(kpis["units_wasted_expired"]) + "\n"
        "Low stock alert: " + kpis["low_stock_alert"] + "\n"
        "Active patients: " + str(kpis["active_patients"]) + "\n"
        "New patients: " + str(kpis["new_patients_this_month"]) + "\n"
        "Refill rate: " + str(kpis["refill_rate_percent"]) + "%\n"
        "Patients overdue for refill: " + str(kpis["patients_overdue_refill"]) + "\n"
        "Overtime hours: " + str(kpis["overtime_hours_this_month"]) + "\n"
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# Save the report to a text file
def save_report(dashboard_text, summary):
    filename = "05-business-intelligence/kpi_report_" + date.today().strftime("%Y_%m_%d") + ".txt"

    with open(filename, "w") as f:
        f.write("RX COMPOUND PHARMACY\n")
        f.write("MONTHLY KPI REPORT\n")
        f.write("Generated: " + date.today().strftime("%B %d %Y") + "\n")
        f.write("=" * 60 + "\n\n")
        f.write(dashboard_text)
        f.write("\n\nEXECUTIVE SUMMARY\n")
        f.write("=" * 60 + "\n")
        f.write(summary)

    return filename

# Run
if __name__ == "__main__":
    print("Generating pharmacy KPI report...")

    # Print dashboard to screen
    print_kpi_dashboard(kpis)

    # Generate executive summary
    print("\nGenerating AI executive summary...")
    summary = generate_executive_summary(kpis)

    print("\n" + "=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    print(summary)

    # Save full report to file
    from io import StringIO
    import sys

    # Capture dashboard output as text
    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    print_kpi_dashboard(kpis)
    sys.stdout = old_stdout
    dashboard_text = buffer.getvalue()

    filename = save_report(dashboard_text, summary)
    print("\n" + "=" * 60)
    print("Report saved to: " + filename)
    print("=" * 60)