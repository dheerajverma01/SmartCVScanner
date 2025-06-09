import os
import json
import openai
import docx
from PyPDF2 import PdfReader
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

resumes_folder = "resumes"
output_path = "data/parsed_resumes.json"
memory_file = "data/processed_candidates.json"

parsed_resumes = []

# Load memory of processed candidates
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        processed_memory = json.load(f)
else:
    processed_memory = []

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        text = " ".join([para.text for para in doc.paragraphs])
    else:
        raise Exception("Unsupported file type: " + filepath)
    return text

def clean_structured_data(raw_text):
    # Remove markdown json code fences (```json ... ```)
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    return cleaned

def parse_with_openai(text):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured JSON data from resumes."},
            {"role": "user", "content": (
                "Extract the following details from this resume text as JSON with these keys: "
                "Name, Experience, Education, Location, Skills. "
                "If any field is missing, use an empty string for its value.\n\nResume Text:\n" + text
            )}
        ]
    )
    return response.choices[0].message.content

def run_agent_1():
    for filename in os.listdir(resumes_folder):
        path = os.path.join(resumes_folder, filename)

        if filename in processed_memory:
            print(f"✅ Already processed: {filename}")
            continue

        try:
            print(f"🧠 Parsing {filename} with GPT...")
            text = extract_text_from_file(path)
            structured_data_raw = parse_with_openai(text)
            structured_data_clean = clean_structured_data(structured_data_raw)

            try:
                structured_json = json.loads(structured_data_clean)
            except json.JSONDecodeError:
                print(f"⚠️ Warning: Failed to parse JSON for {filename}. Saving raw cleaned text.")
                structured_json = {"raw_data": structured_data_clean}

            parsed_resumes.append({"file": filename, "structured_data": structured_json})
            processed_memory.append(filename)
        except Exception as e:
            print(f"❌ Failed to parse {filename}: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(parsed_resumes, f, indent=2)

    with open(memory_file, "w") as f:
        json.dump(processed_memory, f)

    print(f"✅ Agent 1 complete. Parsed resumes saved to {output_path}")

if __name__ == "__main__":
    run_agent_1()
