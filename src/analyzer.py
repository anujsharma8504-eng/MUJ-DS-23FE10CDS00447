"""
Resume analyzer core logic.

Loads prompt templates from prompts/prompts.yaml, formats them with
the resume text and job description, calls the LLM, and parses the
structured JSON response.
"""

import json
import re
from typing import Any

import yaml

from src.llm_client import LLMClient


class ResumeAnalyzer:
    """Orchestrates the resume-vs-job-description analysis."""

    def __init__(self, config_path: str = "config/config.yaml") -> None:
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        prompts_path = self.config["paths"]["prompts_file"]
        with open(prompts_path, "r", encoding="utf-8") as f:
            self.prompts = yaml.safe_load(f)

        self.llm = LLMClient(config_path)

        self.max_resume_chars: int = self.config["app"]["max_resume_chars"]
        self.max_job_chars: int = self.config["app"]["max_job_chars"]
        self.strip_fences: bool = self.config["output"]["strip_markdown_fences"]

    def _truncate(self, text: str, limit: int) -> str:
        text = text.strip()
        return text if len(text) <= limit else text[:limit] + "\n...[truncated]"

    def _clean_json_string(self, raw: str) -> str:
        """Remove markdown code fences and stray text around the JSON."""
        raw = raw.strip()

        if self.strip_fences:
            # Strip ```json ... ``` or ``` ... ```
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

        # Sometimes models prefix with "Here is the JSON:" — keep only
        # the substring from the first { to the last }
        first_brace = raw.find("{")
        last_brace = raw.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            raw = raw[first_brace : last_brace + 1]

        return raw.strip()

    def _build_system_prompt(self) -> str:
        """Combine the role-based system prompt with the few-shot example."""
        base = self.prompts["resume_analysis"]["system"].strip()
        example = self.prompts["resume_analysis"].get("few_shot_example", "").strip()

        if example:
            return f"{base}\n\n--- FEW-SHOT EXAMPLE ---\n{example}"

        return base

    def analyze(self, resume_text: str, job_description: str) -> dict[str, Any]:
        """
        Run the analysis and return a parsed JSON dict.

        Returns a dict with an 'error' key if parsing fails, so the UI
        can display a helpful message instead of crashing.
        """
        if not resume_text or not job_description:
            return {"error": "Both resume text and job description are required."}

        resume_text = self._truncate(resume_text, self.max_resume_chars)
        job_description = self._truncate(job_description, self.max_job_chars)

        system_prompt = self._build_system_prompt()
        user_prompt = self.prompts["resume_analysis"]["user"].format(
            resume_text=resume_text,
            job_description=job_description,
        )

        try:
            raw = self.llm.generate(system_prompt, user_prompt)
        except RuntimeError as e:
            return {"error": str(e)}

        cleaned = self._clean_json_string(raw)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            return {
                "error": f"LLM returned invalid JSON: {e}",
                "raw_response": raw,
            }