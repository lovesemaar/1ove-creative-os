from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CreativeBrief:
    idea: str
    platform: str
    duration: str
    privacy_mode: str = "public_safe"
    use_memory: bool = False
    memory_context: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentOutput:
    agent_name: str
    content: dict[str, Any]


@dataclass
class ReviewOutput:
    reviewer_name: str
    status: str
    notes: list[str] = field(default_factory=list)
    score: int = 0


@dataclass
class EvaluationResult:
    decision: str
    total_score: int
    max_score: int
    category_scores: dict[str, int]
    issues: list[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    brief: CreativeBrief
    privacy_hits: list[str]
    memory_context: list[dict[str, Any]]
    agent_outputs: list[AgentOutput]
    review_outputs: list[ReviewOutput]
    evaluation: EvaluationResult
    final_content: dict[str, Any]
