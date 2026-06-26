from __future__ import annotations

import json
from typing import Any

from app.config import CONFIG_DIR
from app.loaders import load_agent_cards, load_knowledge
from app.mock_model import (
    create_director_output,
    create_final_output,
    create_script_output,
    create_storyboard_output,
    create_subtitle_music_output,
    create_visual_output,
)
from app.model_client import ModelClientError, create_model_client, load_model_settings
from app.types import AgentOutput, CreativeBrief


AGENT_ORDER = [
    ("1oVE Director", "1ove_director"),
    ("Scriptwriter Agent", "scriptwriter"),
    ("Storyboard Agent", "storyboard"),
    ("Visual Director Agent", "visual_director"),
    ("Subtitle & Music Agent", "subtitle_music"),
    ("Final Polish Agent", "final_polish"),
]


SCHEMA_HINTS: dict[str, dict[str, Any]] = {
    "1oVE Director": {
        "emotional_angle": "string",
        "audience_feeling": "string",
        "primary_world": "string",
        "supporting_world": "string",
        "transformation_arc": "string",
        "content_category": "string",
        "approval_notes": "string",
    },
    "Scriptwriter Agent": {
        "hook": "string",
        "voiceover": ["line 1", "line 2"],
        "ending_line": "string",
        "pause_points": ["string"],
    },
    "Storyboard Agent": {
        "scenes": [{"time": "0-3s", "visual": "string", "actor_action": "string", "transition": "string"}]
    },
    "Visual Director Agent": {
        "color_mood": "string",
        "lighting": "string",
        "camera": "string",
        "symbols": ["string"],
        "final_frame": "string",
    },
    "Subtitle & Music Agent": {
        "music_mood": "string",
        "subtitle_style": "string",
        "sound_design": "string",
        "pacing": "string",
    },
    "Final Polish Agent": {
        "title": "string",
        "platform": "string",
        "duration": "string",
        "hook": "string",
        "voiceover_script": ["string"],
        "visual_direction": [{"time": "0-3s", "visual": "string"}],
        "music_mood": "string",
        "subtitle_style": "string",
        "editing_style": "string",
        "ending_line": "string",
        "call_to_action": "string",
        "review_notes": ["string"],
        "final_video_prompt": "string",
    },
}


def _mock_agent_outputs(brief: CreativeBrief) -> list[AgentOutput]:
    director = create_director_output(brief)
    script = create_script_output(brief, director)
    storyboard = create_storyboard_output(script)
    visual = create_visual_output(director)
    subtitle_music = create_subtitle_music_output()
    final = create_final_output(brief, director, script, storyboard, visual, subtitle_music)

    return [
        AgentOutput("1oVE Director", director),
        AgentOutput("Scriptwriter Agent", script),
        AgentOutput("Storyboard Agent", storyboard),
        AgentOutput("Visual Director Agent", visual),
        AgentOutput("Subtitle & Music Agent", subtitle_music),
        AgentOutput("Final Polish Agent", final),
    ]


def _build_system_prompt(agent_name: str, agent_card: str, knowledge: dict[str, str]) -> str:
    core_identity = knowledge.get("core_identity", "")
    privacy_lock = knowledge.get("privacy_lock", "")
    return f"""
You are {agent_name} inside 1oVE Creative OS v1 — The Reconstruction Era.

CORE IDENTITY:
{core_identity}

PRIVACY LOCK:
{privacy_lock}

AGENT CARD:
{agent_card}

Rules:
- cinematic, emotionally intelligent, identity-driven output
- no fake alpha tone
- no generic motivation
- no private trauma exposure by default
- use public-safe symbolic language
- every output must support The Reconstruction Era
- return JSON only, no markdown
""".strip()


def _build_user_prompt(brief: CreativeBrief, previous_outputs: list[AgentOutput]) -> str:
    memory_context = json.dumps(brief.memory_context, indent=2, ensure_ascii=False)
    prev = json.dumps([{"agent": o.agent_name, "content": o.content} for o in previous_outputs], indent=2, ensure_ascii=False)
    return f"""
CREATIVE BRIEF
Idea: {brief.idea}
Platform: {brief.platform}
Duration: {brief.duration}
Privacy mode: {brief.privacy_mode}

MEMORY CONTEXT
{memory_context}

PREVIOUS AGENT OUTPUTS
{prev}

TASK
Create your next agent output. Stay cinematic, usable, and public-safe.
""".strip()


def _fallback_with_note(mock_output: AgentOutput, error: Exception) -> AgentOutput:
    content = dict(mock_output.content)
    content["_llm_fallback"] = True
    content["_llm_error"] = str(error)
    return AgentOutput(mock_output.agent_name, content)


def run_agents(brief: CreativeBrief, model_backend: str | None = None) -> list[AgentOutput]:
    settings = load_model_settings(str(CONFIG_DIR / "model.json"))
    if model_backend:
        settings.backend = model_backend

    if settings.backend.lower() == "mock":
        return _mock_agent_outputs(brief)

    client = create_model_client(settings)
    agent_cards = load_agent_cards()
    knowledge = load_knowledge()
    mock_outputs = _mock_agent_outputs(brief)

    outputs: list[AgentOutput] = []

    for idx, (agent_name, card_key) in enumerate(AGENT_ORDER):
        card_text = agent_cards.get(card_key, "")
        try:
            content = client.generate_json(
                agent_name=agent_name,
                system_prompt=_build_system_prompt(agent_name, card_text, knowledge),
                user_prompt=_build_user_prompt(brief, outputs),
                schema_hint=SCHEMA_HINTS[agent_name],
            )

            if agent_name == "Final Polish Agent":
                required = ["title", "hook", "voiceover_script", "visual_direction", "final_video_prompt"]
                missing = [field for field in required if field not in content]
                if missing:
                    raise ModelClientError(f"Final output missing required fields: {missing}")

            outputs.append(AgentOutput(agent_name, content))
        except Exception as exc:
            if settings.safe_fallback_to_mock:
                outputs.append(_fallback_with_note(mock_outputs[idx], exc))
            else:
                raise

    return outputs
