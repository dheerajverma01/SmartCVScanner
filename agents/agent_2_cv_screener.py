import json
import os
from difflib import SequenceMatcher
from PyPDF2 import PdfReader

parsed_resumes_path = "data/parsed_resumes.json"
screened_output_path = "data/screened.json"
jd_path = "job_descriptions/operations_manager.pdf"

def read_jd_text(path):
    reader = PdfReader(path)
    text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    return text.lower()

def flatten_text(value):
    # Convert list or dict or str to string
    if isinstance(value, list):
        return " ".join([flatten_text(v) for v in value])
    elif isinstance(value, dict):
        return " ".join([flatten_text(v) for v in value.values()])
    elif isinstance(value, str):
        return value
    else:
        return ""

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def run_agent_2():
    jd_text = read_jd_text(jd_path)

    if not os.path.exists(parsed_resumes_path):
        print(f"❌ Parsed resumes file not found: {parsed_resumes_path}")
        return

    with open(parsed_resumes_path, "r", encoding="utf-8") as f:
        resumes = json.load(f)

    screened = []
    threshold = 0.002  # You can adjust this threshold

    for res in resumes:
        structured = res.get("structured_data", {})
        if isinstance(structured, str):
            # If still string (raw JSON as string), parse it
            try:
                import json as js
                structured = js.loads(structured)
            except:
                structured = {}

        # Concatenate all important fields into one string
        candidate_text = " ".join([
            flatten_text(structured.get("Experience", "")),
            flatten_text(structured.get("Education", "")),
            flatten_text(structured.get("Skills", "")),
            flatten_text(structured.get("Location", ""))
        ]).lower()

        score = similarity(jd_text, candidate_text)

        name = structured.get("Name", res.get("file", "Unknown"))

        print(f"Candidate: {name}, Similarity Score: {score:.2f}")

        if score > threshold:
            decision = "Shortlisted"
            reason = "Relevant experience and keywords matched"
        else:
            decision = "Rejected"
            reason = "Insufficient match with JD"

        screened.append({
            "full_name": name,
            "decision": decision,
            "reason": reason
        })

    with open(screened_output_path, "w", encoding="utf-8") as f:
        json.dump(screened, f, indent=2)

    print(f"✅ Screening complete. Results saved to: {screened_output_path}")

if __name__ == "__main__":
    run_agent_2()
