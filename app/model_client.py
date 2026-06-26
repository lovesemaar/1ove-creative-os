"""Local model connector layer for 1oVE Creative OS v1 Stage 7.

This module upgrades the Stage 6 mock-only skeleton into a safe mock-to-LLM
prototype. It supports:
- mock: no model required; deterministic fallback
- ollama: local Ollama HTTP API
- openai_compatible: LM Studio or any local OpenAI-compatible server

The privacy gate still runs before model calls. The runner also falls back to
mock outputs when the local model is unavailable or returns invalid JSON.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class ModelClientError(RuntimeError):
    """Raised when a local model backend cannot return a usable response."""


@dataclass
class ModelSettings:
    backend: str = "mock"
    safe_fallback_to_mock: bool = True
    timeout_seconds: int = 120

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    openai_compatible_base_url: str = "http://localhost:1234/v1"
    openai_compatible_model: str = "local-model"
    openai_compatible_api_key: str = "lm-studio"


def load_model_settings(config_path: str | None = None) -> ModelSettings:
    """Load model settings from config/model.json and environment variables.

    Environment variables override config file values:
    ONEVE_MODEL_BACKEND=mock|ollama|openai_compatible
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=...
    OPENAI_COMPATIBLE_BASE_URL=http://localhost:1234/v1
    OPENAI_COMPATIBLE_MODEL=...
    OPENAI_COMPATIBLE_API_KEY=...
    """

    data: dict[str, Any] = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    settings = ModelSettings(**{k: v for k, v in data.items() if k in ModelSettings.__annotations__})

    settings.backend = os.getenv("ONEVE_MODEL_BACKEND", settings.backend)
    settings.ollama_base_url = os.getenv("OLLAMA_BASE_URL", settings.ollama_base_url)
    settings.ollama_model = os.getenv("OLLAMA_MODEL", settings.ollama_model)
    settings.openai_compatible_base_url = os.getenv(
        "OPENAI_COMPATIBLE_BASE_URL", settings.openai_compatible_base_url
    )
    settings.openai_compatible_model = os.getenv(
        "OPENAI_COMPATIBLE_MODEL", settings.openai_compatible_model
    )
    settings.openai_compatible_api_key = os.getenv(
        "OPENAI_COMPATIBLE_API_KEY", settings.openai_compatible_api_key
    )

    return settings


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract a JSON object from a model response.

    Local models sometimes wrap JSON in prose or markdown fences. This function
    tries direct JSON first, then searches for the first {...} block.
    """

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    raise ModelClientError("Model response did not contain valid JSON.")


def http_post_json(url: str, payload: dict[str, Any], timeout: int, headers: dict[str, str] | None = None) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.URLError as exc:
        raise ModelClientError(f"HTTP request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ModelClientError("Backend returned non-JSON HTTP response.") from exc


class BaseModelClient:
    def generate_json(
        self,
        *,
        agent_name: str,
        system_prompt: str,
        user_prompt: str,
        schema_hint: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError


class MockModelClient(BaseModelClient):
    """Placeholder client. Agent runner uses Stage 6 mock functions directly."""

    def generate_json(
        self,
        *,
        agent_name: str,
        system_prompt: str,
        user_prompt: str,
        schema_hint: dict[str, Any],
    ) -> dict[str, Any]:
        return {"mock": True, "agent_name": agent_name}


class OllamaClient(BaseModelClient):
    def __init__(self, settings: ModelSettings) -> None:
        self.settings = settings

    def generate_json(
        self,
        *,
        agent_name: str,
        system_prompt: str,
        user_prompt: str,
        schema_hint: dict[str, Any],
    ) -> dict[str, Any]:
        url = self.settings.ollama_base_url.rstrip("/") + "/api/chat"
        payload = {
            "model": self.settings.ollama_model,
            "stream": False,
            "format": "json",
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt
                    + "\n\nReturn valid JSON only. Use this JSON shape:\n"
                    + json.dumps(schema_hint, indent=2),
                },
            ],
        }
        response = http_post_json(url, payload, self.settings.timeout_seconds)
        content = response.get("message", {}).get("content", "")
        if not content:
            raise ModelClientError("Ollama response missing message.content.")
        return extract_json_object(content)


class OpenAICompatibleClient(BaseModelClient):
    """Connector for LM Studio or other local OpenAI-compatible chat servers."""

    def __init__(self, settings: ModelSettings) -> None:
        self.settings = settings

    def generate_json(
        self,
        *,
        agent_name: str,
        system_prompt: str,
        user_prompt: str,
        schema_hint: dict[str, Any],
    ) -> dict[str, Any]:
        url = self.settings.openai_compatible_base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {self.settings.openai_compatible_api_key}"}
        payload = {
            "model": self.settings.openai_compatible_model,
            "temperature": 0.7,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt
                    + "\n\nReturn valid JSON only. Use this JSON shape:\n"
                    + json.dumps(schema_hint, indent=2),
                },
            ],
        }
        response = http_post_json(url, payload, self.settings.timeout_seconds, headers=headers)
        choices = response.get("choices", [])
        if not choices:
            raise ModelClientError("OpenAI-compatible response missing choices.")
        content = choices[0].get("message", {}).get("content", "")
        if not content:
            raise ModelClientError("OpenAI-compatible response missing message.content.")
        return extract_json_object(content)


def create_model_client(settings: ModelSettings) -> BaseModelClient:
    backend = settings.backend.lower().strip()
    if backend == "ollama":
        return OllamaClient(settings)
    if backend in {"openai_compatible", "lmstudio", "lm_studio"}:
        return OpenAICompatibleClient(settings)
    return MockModelClient()
