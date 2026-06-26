from __future__ import annotations

import re
from typing import Any

from app.memory_store import iter_memories
from app.privacy_gate import filter_memory_for_prompt


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", (text or "").lower()))


def score_memory(query: str, item: dict[str, Any]) -> int:
    q = _tokenize(query)
    hay = _tokenize(" ".join([
        item.get("title", ""),
        item.get("category", ""),
        " ".join(item.get("tags", [])),
        item.get("text", ""),
    ]))
    return len(q & hay)


def retrieve_memory(query: str, privacy_mode: str = "public_safe", limit: int = 5) -> list[dict[str, Any]]:
    tiers = ["public", "project"]
    if privacy_mode == "private_draft":
        tiers.append("private")
    candidates = iter_memories(tiers=tiers)
    candidates = filter_memory_for_prompt(candidates, privacy_mode)
    ranked = sorted(candidates, key=lambda item: score_memory(query, item), reverse=True)
    return [item for item in ranked if score_memory(query, item) > 0][:limit]
