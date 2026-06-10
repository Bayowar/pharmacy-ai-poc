import ollama
from datetime import date, timedelta

MODEL = "llama3.2:3b"

#List of current pharmacy batches
# Each batch has an ID, compound name, date it was made, and BUD in days
# USP 797 allows up to 30 days BUD for most sterile compounds like B12
batches = [
    {
        "id": "B001",
        "compound": "B12 1000mcg/mL",
        "made_on": date.today() - timedelta(days=28),
        "bud_days": 30
    },
    {
        "id": "B002",
        "compound": "B12 500mcg/mL",
        "made_on": date.today() - timedelta(days=25),
        "bud_days": 30
    },
    {
        "id": "B003",
        "compound": "MIC Injection",
        "made_on": date.today() - timedelta(days=10),
        "bud_days": 30
    },
    {
        "id": "B004",
        "compound": "Glutathione IV",
        "made_on": date.today() - timedelta(days=12),
        "bud_days": 14
    },
    {
        "id": "B005",
        "compound": "B12 1000mcg/mL",
        "made_on": date.today() - timedelta(days=2),
        "bud_days": 30
    },
]

#Check each batch and assign a status
def check_batches(batches):
    today = date.today()
    results = []

    for batch in batches:
        expiry_date = batch["made_on"] + timedelta(days=batch["bud_days"])
        days_left = (expiry_date - today).days

        # Assign urgency status based on days remaining
        if days_left <= 0:
            status = "EXPIRED"
            icon = "X"
        elif days_left <= 3:
            status = "URGENT"
            icon = "!"
        elif days_left <= 7:
            status = "WARNING"
            icon = "~"
        else:
            status = "OK"
            icon = "+"

        results.append({
            "id": batch["id"],
            "compound": batch["compound"],
            "made_on": batch["made_on"].strftime("%B %d %Y"),
            "expiry_date": expiry_date.strftime("%B %d %Y"),
            "days_left": days_left,
            "status": status,
            "icon": icon
        })

    return results

#Display the batch status table 
def print_batch_table(results):
    print("\n" + "=" * 60)
    print("BATCH EXPIRY STATUS REPORT")
    print("Date: " + date.today().strftime("%B %d %Y"))
    print("=" * 60)
    print("{:<6} {:<20} {:<12} {:<10} {}".format(
        "ID", "Compound", "Expires", "Days Left", "Status"
    ))
    print("-" * 60)

    for r in results:
        print("{:<6} {:<20} {:<12} {:<10} [{}] {}".format(
            r["id"],
            r["compound"],
            r["expiry_date"],
            r["days_left"],
            r["icon"],
            r["status"]
        ))

#Build a summary for the AI
def build_summary(results):
    lines = []
    for r in results:
        lines.append(
            r["id"] + " | " +
            r["compound"] + " | " +
            str(r["days_left"]) + " days left | " +
            r["status"]
        )
    return "\n".join(lines)

#Ask AI to write a compliance report
def generate_compliance_report(summary):
    prompt = (
        "You are a USP 797 pharmacy compliance officer. "
        "Review these batch expiry statuses and write a formal "
        "action report with clear priorities and specific instructions "
        "for the pharmacy team. Keep it under 150 words: "
        "\n\n" + summary
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# Run
if __name__ == "__main__":
    print("Running batch expiry check...")

    # Check all batches
    results = check_batches(batches)

    # Print the status table
    print_batch_table(results)

    # Count alerts
    expired = [r for r in results if r["status"] == "EXPIRED"]
    urgent = [r for r in results if r["status"] == "URGENT"]
    warning = [r for r in results if r["status"] == "WARNING"]
    ok = [r for r in results if r["status"] == "OK"]

    print("\nSUMMARY:")
    print("  Expired:  " + str(len(expired)))
    print("  Urgent:   " + str(len(urgent)))
    print("  Warning:  " + str(len(warning)))
    print("  OK:       " + str(len(ok)))

    # Generate AI compliance report
    print("\nGenerating AI compliance report...")
    summary = build_summary(results)
    report = generate_compliance_report(summary)

    print("\n" + "=" * 60)
    print("AI COMPLIANCE REPORT")
    print("=" * 60)
    print(report)
