from __future__ import annotations

from pathlib import Path

from app.config import DATA_DIR


def load_markdown_dir(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for file in path.glob("*.md"):
        data[file.stem] = file.read_text(encoding="utf-8")
    return data


def load_agent_cards() -> dict[str, str]:
    return load_markdown_dir(DATA_DIR / "agents")


def load_reviewer_cards() -> dict[str, str]:
    return load_markdown_dir(DATA_DIR / "reviewers")


def load_knowledge() -> dict[str, str]:
    return load_markdown_dir(DATA_DIR / "knowledge")
