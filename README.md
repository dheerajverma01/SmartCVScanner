# 🧠 Auto CV Screener & Interview Outreach System

This project automates end-to-end CV screening and interview scheduling using a **multi-agent AI system**. Ideal for hiring in mid-level or frontline roles.

## 🧩 Agents Overview

### 1️⃣ Agent 1: Resume Ingestion & Extraction
- Inputs PDFs from `data/raw_resumes/`
- Extracts structured data (name, skills, education, etc.)
- Logs unprocessable files
- Checks for duplicate screening (30-day window)

### 2️⃣ Agent 2: CV Screener Agent
- Matches against location, experience, domain
- Classifies as **Shortlisted** or **Rejected**
- Saves decision + reason to `data/screened.json`

### 3️⃣ Agent 3: Feedback Generator
- Adds natural language reasons
- Updates a final `Google Sheet` or summary table
- Logs patterns (e.g., “Most rejections due to experience”)

### 4️⃣ Agent 4: Interview Outreach Agent
- Picks "Shortlisted" candidates
- Generates WhatsApp/email-style messages (prints to console)
- Logs outreach in `data/outreach_log.json`

---

## 🔧 Tech Stack

- **Python 3.8+**
- OpenAI API (GPT-4 or GPT-3.5-turbo)
- PyPDF2 or pdfplumber (PDF parsing)
- JSON, datetime, os
- Optional: Google Sheets API, email libraries (commented out)

---

## ▶️ How to Run

1. **Place resumes in:**  
   `data/raw_resumes/`

2. **Run each agent in order:**
```bash
python agents/agent_1_resume_extractor.py
python agents/agent_2_cv_screener.py
python agents/agent_3_feedback_generator.py
python agents/agent_4_interview_outreach.py
