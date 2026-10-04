# Capstone Project — AI Resume Analyzer

**Team:** Solo
**Member:** Anuj Sharma (23FE10CDS00447)
**Branch:** B.Tech Computer Science (Data Science)
**GitHub:** anujsharma8504-eng

---

## Project Title

AI Resume Analyzer — An NLP application that uses a Large Language Model (LLM) via API to analyze a resume against a job description.

---

## Description

The analyzer takes a job description and a resume (PDF or pasted text), sends them to an LLM through an API call, and returns structured feedback:

- **Match score** (0–100) and verdict (Strong / Moderate / Weak Match)
- **Matching skills** found in the resume
- **Missing skills** required by the job
- **Strengths** identified in the resume
- **Actionable improvements** for the candidate
- **Plain-English summary** of the fit

The LLM is instructed with a role-based system prompt and a few-shot example to produce reliable, structured JSON output.

---

## Tech Stack

- **Language:** Python 3.10+
- **UI:** Streamlit
- **LLM Access:** OpenRouter (OpenAI-compatible API)
- **Config & Prompts:** YAML files (`config/config.yaml`, `prompts/prompts.yaml`)
- **PDF Parsing:** pypdf
- **Testing:** pytest

---

## Deliverables

| Deliverable | Location |
|---|---|
| Source code | `../code/` |
| Configuration | `../code/config/config.yaml` |
| Prompt file | `../code/prompts/prompts.yaml` |
| Tests | `../code/tests/` |
| Installation guide | `../README.md` |
| Presentation | `../presentations/` |
| Resources | `../resources/` |

---

## Team Contribution

All work — design, prompt engineering, coding, testing, and documentation — was completed individually by Anuj Sharma.

---

## How to Run

See the main `README.md` in the repository root for full setup instructions.

**Quick start:**

```bash
cd code
pip install -r requirements.txt
# create .env with OPENROUTER_API_KEY=your_key_here
streamlit run app.py