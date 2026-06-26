from __future__ import annotations

from app.privacy_gate import detect_sensitive_terms
from app.types import EvaluationResult, ReviewOutput


REQUIRED_FIELDS = [
    "title",
    "platform",
    "duration",
    "hook",
    "voiceover_script",
    "visual_direction",
    "music_mood",
    "subtitle_style",
    "editing_style",
    "ending_line",
    "call_to_action",
    "review_notes",
    "final_video_prompt",
]


def evaluate_output(final_content: dict, reviews: list[ReviewOutput]) -> EvaluationResult:
    issues: list[str] = []
    scores: dict[str, int] = {}

    missing = [field for field in REQUIRED_FIELDS if field not in final_content]
    scores["required_format"] = 5 if not missing else 1
    if missing:
        issues.append(f"Missing required fields: {missing}")

    voiceover = final_content.get("voiceover_script", [])
    text = " ".join([
        str(final_content.get("hook", "")),
        " ".join(voiceover if isinstance(voiceover, list) else [str(voiceover)]),
        str(final_content.get("ending_line", "")),
        str(final_content.get("final_video_prompt", "")),
    ]).lower()

    scores["emotional_depth"] = 5 if len(voiceover) >= 5 and any(w in text for w in ["pain", "survival", "discipline", "identity"]) else 2
    scores["cinematic_visuals"] = 5 if final_content.get("visual_direction") and any(w in text for w in ["mirror", "eyes", "night", "script", "laptop", "shadow"]) else 2
    scores["brand_alignment"] = 5 if any(w in text for w in ["reconstruction", "survival", "identity", "discipline"]) else 2
    scores["production_usefulness"] = 5 if final_content.get("visual_direction") and final_content.get("music_mood") and final_content.get("editing_style") else 2

    sensitive_hits = detect_sensitive_terms(text)
    scores["privacy_safety"] = 1 if sensitive_hits else 5
    if sensitive_hits:
        issues.append(f"Sensitive terms detected: {sensitive_hits}")

    reviewer_min = min((r.score for r in reviews), default=0)
    scores["reviewer_minimum"] = reviewer_min

    total = sum(scores.values())
    max_score = 30

    if scores["privacy_safety"] <= 1:
        decision = "BLOCKED_PRIVACY"
    elif scores["required_format"] <= 1:
        decision = "FORMAT_FAIL"
    elif total >= 25 and reviewer_min >= 4:
        decision = "READY"
    elif total >= 18:
        decision = "NEEDS_TUNING"
    else:
        decision = "NOT_READY"

    return EvaluationResult(
        decision=decision,
        total_score=total,
        max_score=max_score,
        category_scores=scores,
        issues=issues,
    )
