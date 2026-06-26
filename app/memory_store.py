from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import MEMORY_DIR


VALID_TIERS = {"public", "project", "private", "sensitive", "runs", "content_history"}


@dataclass
class MemoryEntry:
    title: str
    tier: str
    category: str
    tags: list[str]
    text: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path_for_tier(tier: str) -> Path:
    if tier not in VALID_TIERS:
        raise ValueError(f"Invalid tier: {tier}")
    if tier == "content_history":
        return MEMORY_DIR / "content_history" / "content_history.jsonl"
    if tier == "sensitive":
        return MEMORY_DIR / "private" / "sensitive_memory.jsonl"
    return MEMORY_DIR / tier / "memory.jsonl"


def init_memory() -> None:
    for tier in VALID_TIERS:
        path = _path_for_tier(tier)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("", encoding="utf-8")


def append_memory(entry: MemoryEntry) -> Path:
    init_memory()
    path = _path_for_tier(entry.tier)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
    return path


def iter_memories(tiers: list[str] | None = None) -> list[dict[str, Any]]:
    init_memory()
    selected = tiers or ["public", "project", "private", "sensitive", "runs", "content_history"]
    rows: list[dict[str, Any]] = []
    for tier in selected:
        path = _path_for_tier(tier)
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def log_run_memory(title: str, text: str, tags: list[str] | None = None) -> None:
    append_memory(MemoryEntry(
        title=title,
        tier="runs",
        category="run",
        tags=tags or ["run", "stage13"],
        text=text,
    ))


def log_content_history(title: str, text: str, tags: list[str] | None = None) -> None:
    append_memory(MemoryEntry(
        title=title,
        tier="content_history",
        category="content_history",
        tags=tags or ["content", "stage13"],
        text=text,
    ))
