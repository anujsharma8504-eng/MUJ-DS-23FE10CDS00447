# AI Resume Analyzer — Project Presentation

**Student:** Anuj Sharma
**Registration No:** 23FE10CDS00447
**Branch:** B.Tech Computer Science (Data Science)
**Batch:** Batch F
**GitHub:** anujsharma8504-eng
**Repository:** MUJ-DS-23FE10CDS00447

---

## Slide 1 — Title

# AI Resume Analyzer
### An NLP project powered by Large Language Models

Anuj Sharma - 23FE10CDS00447 - Batch F

---

## Slide 2 — Problem Statement

The problem:
- Recruiters spend 6-8 seconds scanning each resume
- Candidates don't know why they're rejected
- Manually comparing a resume to a job description is slow and subjective

The goal:
Build an LLM-powered tool that objectively scores a resume against a job description and gives actionable feedback in seconds.

---

## Slide 3 — Solution Overview

What it does:
1. User pastes a job description
2. User uploads a PDF resume (or pastes text)
3. App sends both to an LLM via API
4. LLM returns structured JSON feedback
5. UI displays the result in a clean format

Output:
- Match score (0-100)
- Verdict (Strong / Moderate / Weak)
- Matching skills & missing skills
- Strengths & improvements
- Plain-English summary

---

## Slide 4 — Architecture

Streamlit UI (app.py)
       |
       v
ResumeAnalyzer (src/analyzer.py)
- loads prompts
- fills templates
- parses JSON
       |
       v
LLMClient (src/llm_client.py)
- API wrapper
- fallback models
- retry logic
       |
       v
OpenRouter API (OpenAI-compatible)

Config: config/config.yaml
Prompts: prompts/prompts.yaml

---

## Slide 5 — LLM Integration

Provider: OpenRouter (OpenAI-compatible endpoint)

Models used:
- Primary: auto-routed via openrouter/free
- Fallbacks configured for reliability

Key techniques:
- Role-based system prompt (expert technical recruiter)
- Strict JSON schema enforced in the prompt
- Few-shot example to lock in output format
- Low temperature (0.3) for consistency
- Automatic fallbacks on transient errors (503, rate limits)

---

## Slide 6 — Prompt Engineering

System prompt:
You are an expert technical recruiter with 10+ years of experience...

User prompt structure:
1. Job description (delimited)
2. Resume text (delimited)
3. Strict JSON schema
4. Explicit rules (don't invent experience, no markdown fences)

Few-shot example:
A worked example showing input and expected output JSON - teaches the model the exact format.

Why this matters:
- Consistency across different resumes
- Machine-parseable output
- No post-processing hacks needed

---

## Slide 7 — Tech Stack

Language:        Python 3.10+
UI:              Streamlit
LLM Access:      OpenRouter (OpenAI-compatible API)
PDF Parsing:     pypdf
Config & Prompts: YAML
Testing:         pytest
Version Control: Git + GitHub

---

## Slide 8 — Demo

Live demo steps:
1. Paste job description
2. Upload resume PDF
3. Click Analyze
4. View structured results

Screenshot: see ../resources/demo.png

---

## Slide 9 — Challenges & Solutions

Challenge 1: LLMs sometimes return prose instead of JSON
Solution: Few-shot example + strict schema + JSON mode flag

Challenge 2: Free-tier rate limits
Solution: Automatic fallback across multiple models + retry logic

Challenge 3: Retired model names
Solution: Centralized model config in config.yaml, easy to swap

Challenge 4: Long resumes overflowing context
Solution: Truncation with markers, configurable limits

---

## Slide 10 — Individual Contribution

All work completed individually:

- Design - project scope, architecture, requirements
- Data preparation - sample resumes, job descriptions, edge cases
- Prompt engineering - system prompt, schema, few-shot example
- Coding - LLM client, analyzer, PDF parser, Streamlit UI
- Testing - unit tests for pure logic
- Documentation - README, capstone doc, inline docstrings
- Workflow - branches, PRs, issues, commits

GitHub activity:
- 5+ commits
- 5 issues created and assigned
- 1 Pull Request created, reviewed, merged

---

## Slide 11 — Results & Evaluation

Performance:
- Analysis time: 5-15 seconds per resume
- Handles PDFs up to several pages
- Structured JSON output - no manual parsing

Test coverage:
- JSON cleaning (markdown fence stripping)
- Truncation logic
- Input validation
- All tests run offline (no API calls)

Reliability:
- Automatic fallback across multiple models
- Retries on transient errors
- Graceful error messages in the UI

---

## Slide 12 — Future Scope

Potential improvements:
1. RAG over a job database - analyze against many jobs at once
2. Multi-language support - resumes in Hindi, Spanish, etc.
3. Fine-tuned scoring model - train on recruiter-labeled data
4. Cover letter generator - auto-draft tailored letters
5. Cloud deployment - Streamlit Cloud or Hugging Face Spaces
6. User accounts - save & compare multiple analyses

---

## Slide 13 — Conclusion

What we built:
A working NLP application that meaningfully integrates an LLM via API calls to solve a real problem.

Key learnings:
- Prompt engineering for reliable structured output
- Error handling for real-world API failures
- Clean architecture: config, prompts, code separated
- GitHub workflow: issues, branches, PRs

The tool:
- Takes a resume + job description
- Returns objective, structured feedback in seconds
- Helps candidates improve before applying

---

## Slide 14 — Thank You

Questions?

- Repository: github.com/anujsharma8504-eng/MUJ-DS-23FE10CDS00447
- Contact: anujsharma8504@gmail.com
