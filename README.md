# 📄 AI Resume Analyzer

An NLP project that uses a Large Language Model (LLM) via API calls to analyze a resume against a job description, producing structured feedback: a match score, missing skills, strengths, and improvement suggestions.

Built as an individual NLP course project.

---

## 🎯 Features

- **PDF resume parsing** — upload a PDF or paste resume text directly
- **LLM-powered analysis** via OpenRouter's OpenAI-compatible API
- **Structured JSON output** — match score, verdict, matching/missing skills, strengths, improvements, summary
- **Configurable** — model, temperature, and prompt templates live in YAML files, not hardcoded
- **Robust** — automatic model fallbacks and retries on rate limits or transient errors
- **Prompt engineering** — role-based system prompt + few-shot example for consistent output

---

## 🏗️ Project Structure

```
resume-analyzer/
├── app.py                      # Streamlit UI (entry point)
├── config/
│   └── config.yaml             # LLM + app settings
├── prompts/
│   └── prompts.yaml            # All prompt templates (externalized)
├── src/
│   ├── __init__.py
│   ├── llm_client.py           # LLM API wrapper with fallbacks
│   ├── analyzer.py             # Core analysis + JSON parsing
│   └── utils.py                # PDF text extraction
├── tests/
│   └── test_analyzer.py        # Unit tests (offline)
├── .env.example                # Template for API key
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repository

```
git clone <your-repo-url>
cd resume-analyzer
```

### 2. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env`:

```
copy .env.example .env
```

Then edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

Get a free key at https://openrouter.ai/keys

### 5. Run the app

```
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🔧 Configuration

All tunable settings are in `config/config.yaml`:

- **Provider** (OpenRouter)
- **Model** name
- **Fallback models**
- **Temperature** (0.3 for consistency)
- **Max tokens**

All LLM prompts are in `prompts/prompts.yaml` — including the role-based system prompt, the user template with a strict JSON schema, and a few-shot example.

This separation means prompts and settings can be changed without editing any Python code.

---

## 🧠 How the LLM Is Used

1. The user provides a job description and a resume (PDF upload or pasted text)
2. `analyzer.py` loads the prompt template from `prompts/prompts.yaml`
3. The template is filled with the resume text and job description (truncated to safe limits)
4. `llm_client.py` sends the prompt to OpenRouter's chat completions endpoint
5. The LLM returns structured JSON matching the enforced schema
6. `analyzer.py` cleans and parses the JSON (strips markdown fences, extracts `{...}` if needed)
7. The Streamlit UI renders the results: score card, verdict, skill lists, strengths, improvements, and a raw JSON view

---

## 🧪 Tests

```
pytest tests/ -v
```

The tests cover pure logic (JSON cleaning, truncation, input validation) and do not require an API key.

---

## 🛠️ Tech Stack

| Component | Purpose |
|---|---|
| Python 3.10+ | Language |
| Streamlit | Web UI |
| OpenAI Python SDK | Chat completions (OpenRouter is OpenAI-compatible) |
| PyYAML | Config + prompt file parsing |
| pypdf | PDF text extraction |
| python-dotenv | API key management |
| pytest | Testing |

---

## 📝 Prompt Engineering Notes

- **Role-based system prompt** ("expert technical recruiter") grounds the LLM in a specific persona, improving output relevance
- **Strict JSON schema** enforced in the user prompt for reliable parsing
- **Few-shot example** teaches the model the exact output format expected
- **Low temperature** (0.3) reduces variability
- **Rules section** explicitly forbids invented experience and markdown fences

---

## 📜 License

Educational project — free to use and modify.