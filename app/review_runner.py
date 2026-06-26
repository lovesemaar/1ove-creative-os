from __future__ import annotations

from app.privacy_gate import detect_sensitive_terms
from app.types import ReviewOutput


def _text_blob(final_content: dict) -> str:
    return " ".join([
        str(final_content.get("title", "")),
        str(final_content.get("hook", "")),
        " ".join(final_content.get("voiceover_script", [])),
        str(final_content.get("ending_line", "")),
        str(final_content.get("final_video_prompt", "")),
    ])


def run_reviews(final_content: dict) -> list[ReviewOutput]:
    text_blob = _text_blob(final_content).lower()
    visuals = final_content.get("visual_direction", [])
    voiceover = final_content.get("voiceover_script", [])

    reviews: list[ReviewOutput] = []

    if len(voiceover) >= 5 and any(word in text_blob for word in ["pain", "survival", "discipline", "identity"]):
        reviews.append(ReviewOutput("Emotional Depth Reviewer", "Pass", ["Voiceover has emotional movement and restraint."], 4))
    else:
        reviews.append(ReviewOutput("Emotional Depth Reviewer", "Revise", ["Voiceover needs deeper emotional movement."], 2))

    symbolic_hits = sum(1 for item in ["mirror", "eyes", "night", "script", "laptop", "gym", "shadow"] if item in text_blob)
    if visuals and symbolic_hits >= 2:
        reviews.append(ReviewOutput("Cinematic Visual Reviewer", "Pass", ["Scene-by-scene symbolic visuals are present."], 4))
    else:
        reviews.append(ReviewOutput("Cinematic Visual Reviewer", "Revise", ["Needs stronger 1oVE visual symbols."], 2))

    if "reconstruction" in text_blob or "survival" in text_blob or "1ove" in text_blob:
        reviews.append(ReviewOutput("Personal Brand Reviewer", "Pass", ["Aligned with The Reconstruction Era."], 4))
    else:
        reviews.append(ReviewOutput("Personal Brand Reviewer", "Revise", ["Needs clearer brand alignment."], 2))

    sensitive_hits = detect_sensitive_terms(text_blob)
    if sensitive_hits:
        reviews.append(ReviewOutput("Sensitive Identity Reviewer", "Revise", [f"Sensitive terms detected: {sensitive_hits}"], 2))
    else:
        reviews.append(ReviewOutput("Sensitive Identity Reviewer", "Pass", ["Public-safe language check passed."], 5))

    return reviews
