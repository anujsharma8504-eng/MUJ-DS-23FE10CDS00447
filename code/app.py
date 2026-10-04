"""
AI Resume Analyzer — Streamlit UI.

Run with:  streamlit run app.py
"""

import yaml
import streamlit as st

from src.analyzer import ResumeAnalyzer
from src.utils import extract_text_from_pdf


# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
with open("config/config.yaml", "r", encoding="utf-8") as f:
    APP_CONFIG = yaml.safe_load(f)


# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(
    page_title=APP_CONFIG["app"]["title"],
    page_icon="📄",
    layout="wide",
)


@st.cache_resource
def get_analyzer() -> ResumeAnalyzer:
    """Cache the analyzer so we only load config/models once."""
    return ResumeAnalyzer()


# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("📄 " + APP_CONFIG["app"]["title"])
st.caption(APP_CONFIG["app"]["description"])


# ------------------------------------------------------------------
# Inputs
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    job_desc = st.text_area(
        "Paste the job description here",
        height=320,
        placeholder="e.g. We are looking for a Python developer with Django, REST APIs, and AWS experience...",
        label_visibility="collapsed",
    )

with col2:
    st.subheader("Resume")
    uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    pasted_resume = st.text_area(
        "…or paste resume text",
        height=200,
        placeholder="Or just paste the resume text here…",
        label_visibility="collapsed",
    )


# ------------------------------------------------------------------
# Analyze button
# ------------------------------------------------------------------
analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze_clicked:
    # Resolve resume text: prefer PDF upload, fall back to pasted text
    resume_text = ""
    if uploaded is not None:
        with st.spinner("Extracting text from PDF…"):
            resume_text = extract_text_from_pdf(uploaded)
        if not resume_text:
            st.error("Could not extract text from that PDF. Try pasting the resume instead.")
            st.stop()
    elif pasted_resume.strip():
        resume_text = pasted_resume.strip()

    if not job_desc.strip() or not resume_text:
        st.warning("Please provide both a job description and a resume (PDF or pasted text).")
        st.stop()

    analyzer = get_analyzer()

    with st.spinner("Analyzing with the LLM…"):
        result = analyzer.analyze(resume_text, job_desc)

    # ---------------- Error path ----------------
    if "error" in result:
        st.error(result["error"])
        if "raw_response" in result:
            with st.expander("Show raw LLM response"):
                st.code(result["raw_response"])
        st.stop()

    # ---------------- Results ----------------
    st.divider()
    st.subheader("Results")

    score = result.get("match_score", 0)
    verdict = result.get("verdict", "N/A")

    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("Match Score", f"{score}/100")
    with c2:
        st.markdown(f"### {verdict}")
        st.write(result.get("summary", ""))

    st.divider()

    colA, colB = st.columns(2)
    with colA:
        st.markdown("### ✅ Matching Skills")
        for s in result.get("matching_skills", []) or ["—"]:
            st.markdown(f"- {s}")
    with colB:
        st.markdown("### ❌ Missing Skills")
        for s in result.get("missing_skills", []) or ["—"]:
            st.markdown(f"- {s}")

    st.divider()

    colC, colD = st.columns(2)
    with colC:
        st.markdown("### 💪 Strengths")
        for s in result.get("strengths", []) or ["—"]:
            st.markdown(f"- {s}")
    with colD:
        st.markdown("### 🚀 Improvements")
        for s in result.get("improvements", []) or ["—"]:
            st.markdown(f"- {s}")

    with st.expander("Raw JSON response"):
        st.json(result)