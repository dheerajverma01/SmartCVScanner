import os
import json
from datetime import datetime

# Dummy message template
MESSAGE_TEMPLATE = """
Hi {name},

Thank you for applying to the role of {role}. We're excited to move forward with your application.

Please schedule your interview using the link below:
👉 {interview_link}

Best,
Hiring Team
"""

def run_agent_4():
    input_file = os.path.abspath("data/screened.json")
    outreach_log = os.path.abspath("data/outreach_log.json")
    role = "Senior Manager"
    interview_link = "https://calendly.com/demo-interview-slot"  # Replace with real or dummy link

    with open(input_file, "r") as f:
        candidates = json.load(f)

    outreach_results = []

    for candidate in candidates:
        if candidate.get("decision") == "Shortlisted":
            name = candidate.get("full_name", "Candidate")
            contact = candidate.get("email", "NA")  # Optional: email field if extracted earlier
            message = MESSAGE_TEMPLATE.format(name=name, role=role, interview_link=interview_link)

            print(f"\n📤 Sending message to {name}...")
            print(message)

            result = {
                "name": name,
                "email": contact,
                "sent": True,
                "timestamp": datetime.now().isoformat(),
                "interview_link": interview_link
            }
            outreach_results.append(result)

    with open(outreach_log, "w") as f:
        json.dump(outreach_results, f, indent=2)

    print("\n✅ Agent 4 done: Outreach log saved to data/outreach_log.json")

if __name__ == "__main__":
    run_agent_4()
