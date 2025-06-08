import json
import csv
import os
from collections import Counter

def run_agent_3():
    input_path = os.path.join("data", "screened.json")
    output_path = os.path.join("data", "feedback_summary.csv")

    if not os.path.exists(input_path):
        print("❌ Error: screened.json file not found.")
        return

    with open(input_path, "r", encoding="utf-8") as infile:
        candidates = json.load(infile)

    if not candidates:
        print("⚠️ No candidates found in screened.json.")
        return

    with open(output_path, "w", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Decision", "Reason"])

        reasons = []
        for candidate in candidates:
            name = candidate.get("full_name", "Unknown")
            decision = candidate.get("decision", "Undecided")
            reason = candidate.get("reason", "No reason provided")
            reasons.append(reason)
            writer.writerow([name, decision, reason])

    print(f"✅ Feedback summary saved to: {output_path}")
    reason_counts = Counter(reasons)
    print("\n📊 Reason Summary:")
    for reason, count in reason_counts.items():
        print(f"- {reason}: {count} candidates")

if __name__ == "__main__":
    run_agent_3()
