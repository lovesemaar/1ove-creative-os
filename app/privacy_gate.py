from __future__ import annotations

import re
from typing import Iterable

SENSITIVE_PATTERNS = [
    r"\bdiagnosis\b",
    r"\bclinical\b",
    r"trauma details?",
    r"self[- ]harm",
    r"suicide",
    r"real name",
    r"family details?",
    r"private memory",
    r"medical record",
    r"address",
    r"phone number",
]

PUBLIC_SAFE_REPLACEMENTS = {
    "diagnosis": "inner conflict",
    "clinical": "human",
    "trauma": "survival",
    "private memory": "old memory",
    "family details": "personal history",
    "real name": "someone",
    "medical record": "private record",
    "address": "private place",
    "phone number": "private contact",
}


def detect_sensitive_terms(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text or "", flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def make_public_safe(text: str) -> str:
    safe = text or ""
    for raw, replacement in PUBLIC_SAFE_REPLACEMENTS.items():
        safe = re.sub(raw, replacement, safe, flags=re.IGNORECASE)
    return safe


def apply_privacy_gate(text: str, mode: str = "public_safe") -> tuple[str, list[str]]:
    hits = detect_sensitive_terms(text)
    if mode == "private_draft":
        return text, hits
    return make_public_safe(text), hits


def filter_memory_for_prompt(memories: Iterable[dict], privacy_mode: str = "public_safe") -> list[dict]:
    allowed: list[dict] = []
    for item in memories:
        tier = item.get("tier", "public")
        if tier == "sensitive":
            continue
        if privacy_mode == "public_safe" and tier == "private":
            continue
        safe_text, hits = apply_privacy_gate(item.get("text", ""), privacy_mode)
        copy = dict(item)
        copy["text"] = safe_text
        copy["privacy_hits"] = hits
        allowed.append(copy)
    return allowed
