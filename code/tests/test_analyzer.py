"""
Basic tests for the analyzer's JSON parsing logic.

These tests don't call the LLM — they only verify the pure logic
(truncation, JSON cleaning, prompt construction), so they run offline.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analyzer import ResumeAnalyzer


def test_clean_json_strips_markdown_fences():
    """The cleaner should remove ```json ... ``` fences."""
    a = ResumeAnalyzer()
    raw = '```json\n{"match_score": 80, "verdict": "Strong Match"}\n```'
    cleaned = a._clean_json_string(raw)
    assert cleaned.startswith("{")
    assert cleaned.endswith("}")
    assert "```" not in cleaned


def test_clean_json_extracts_json_from_preamble():
    """If the model adds chit-chat before the JSON, keep only the JSON."""
    a = ResumeAnalyzer()
    raw = 'Here is the JSON:\n{"match_score": 50, "verdict": "Moderate Match"}'
    cleaned = a._clean_json_string(raw)
    assert cleaned.startswith("{")
    assert "Here is the JSON" not in cleaned


def test_truncate_long_text():
    """Truncation should cap long text and append a marker."""
    a = ResumeAnalyzer()
    long_text = "x" * 20000
    result = a._truncate(long_text, 100)
    assert len(result) < 20000
    assert "truncated" in result


def test_analyze_returns_error_when_inputs_missing():
    """Empty resume or job description should return an error dict."""
    a = ResumeAnalyzer()
    result = a.analyze("", "some job")
    assert "error" in result

    result = a.analyze("some resume", "")
    assert "error" in result