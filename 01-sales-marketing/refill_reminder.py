import ollama

MODEL = "llama3.2:3b"

patients = [
    {"name": "John Smith", "days_since": 32, "medication": "B12 1000mcg"},
    {"name": "Maria Garcia", "days_since": 45, "medication": "B12 500mcg"},
    {"name": "David Lee", "days_since": 28, "medication": "B12 1000mcg"},
    {"name": "Susan Park", "days_since": 60, "medication": "B12 1000mcg"},
    {"name": "James Brown", "days_since": 21, "medication": "B12 500mcg"},
]

def generate_reminder(patient):
    prompt = (
        "Write a short warm refill reminder email for a pharmacy patient. "
        "Patient name: " + patient['name'] + ". "
        "Medication: " + patient['medication'] + " injection. "
        "Days since last dose: " + str(patient['days_since']) + " days. "
        "Keep it under 100 words. "
        "Sign off as: Your Care Team at Rx Compound Pharmacy."
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

if __name__ == "__main__":
    print("Rx Compound Pharmacy - Refill Reminder Generator")
    print("=" * 50)
    for patient in patients:
        print("\nReminder for: " + patient['name'])
        print("-" * 50)
        reminder = generate_reminder(patient)
        print(reminder)
        print()