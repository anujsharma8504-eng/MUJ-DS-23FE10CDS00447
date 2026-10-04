"""
LLM client wrapper.

Loads configuration, sends chat completions to the configured
provider's OpenAI-compatible endpoint, and handles fallback models
when the primary model is temporarily unavailable.
"""

import os
import time
from typing import Optional

import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    """Thin wrapper around an OpenAI-compatible chat API."""

    def __init__(self, config_path: str = "config/config.yaml") -> None:
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        llm_cfg = self.config["llm"]
        self.base_url: str = llm_cfg["base_url"]
        self.model: str = llm_cfg["model"]
        self.fallback_models: list = llm_cfg.get("fallback_models", [])
        self.temperature: float = llm_cfg["temperature"]
        self.max_tokens: int = llm_cfg["max_tokens"]
        self.timeout: int = llm_cfg.get("timeout_seconds", 60)

        provider = llm_cfg.get("provider", "gemini")
        if provider == "openrouter":
            env_var = "OPENROUTER_API_KEY"
        else:
            env_var = "GEMINI_API_KEY"

        api_key = os.getenv(env_var)
        if not api_key:
            raise EnvironmentError(
                f"{env_var} is not set. Create a .env file with {env_var}=your_key_here"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    def _try_model(self, model: str, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Attempt a single completion call with one model."""
        try:
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }

            # Enable JSON mode if configured (OpenAI-compatible)
            if self.config["llm"].get("json_mode", False):
                kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            return content.strip() if content else None
        except Exception as e:
            print(f"[LLMClient] Model '{model}' failed: {type(e).__name__}: {e}")
            return None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a completion, trying the primary model then fallbacks.
        Retries once on failure with a short delay (for transient 503s).
        Raises RuntimeError if every model fails.
        """
        models_to_try = [self.model] + self.fallback_models

        for model in models_to_try:
            result = self._try_model(model, system_prompt, user_prompt)
            if result:
                return result

            time.sleep(2)
            result = self._try_model(model, system_prompt, user_prompt)
            if result:
                return result

        raise RuntimeError(
            f"All models failed: {models_to_try}. "
            "Check your API key, quota, or try again in a minute."
        )