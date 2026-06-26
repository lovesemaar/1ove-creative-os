from __future__ import annotations

from app.types import CreativeBrief


def choose_world(idea: str) -> str:
    text = idea.lower()
    if "ai" in text or "system" in text or "prompt" in text:
        return "Pain Into Architecture"
    if "acting" in text or "actor" in text or "monologue" in text:
        return "The Man in Reconstruction"
    if "love" in text or "duality" in text or "lucky" in text:
        return "Love, Lucky, and 1oVE"
    if "gym" in text or "discipline" in text or "body" in text:
        return "Dark Cinematic Transformation World"
    return "The Reconstruction Era"


def memory_note(brief: CreativeBrief) -> str:
    if not brief.memory_context:
        return "No memory context used."
    titles = ", ".join(item.get("title", "memory") for item in brief.memory_context[:3])
    return f"Memory context used: {titles}"


def create_director_output(brief: CreativeBrief) -> dict:
    world = choose_world(brief.idea)
    return {
        "emotional_angle": "survival turning into disciplined identity",
        "audience_feeling": "quiet recognition, tension, and hope",
        "primary_world": world,
        "supporting_world": "Pain Into Architecture" if brief.use_memory else "The Man in Reconstruction",
        "transformation_arc": "from inner pressure to controlled reconstruction",
        "content_category": "cinematic personal-brand reel",
        "approval_notes": f"Proceed with restrained, emotionally intelligent direction. {memory_note(brief)}",
    }


def create_script_output(brief: CreativeBrief, director: dict) -> dict:
    return {
        "hook": "Some men do not change because life inspires them. They change because staying the same becomes unbearable.",
        "voiceover": [
            "I am not trying to look like a new man.",
            "I am rebuilding the one survival almost buried.",
            "The silence, the late nights, the pressure — it all became material.",
            "Not for sympathy.",
            "For structure.",
            "For discipline.",
            "For the version of me that refuses to disappear.",
        ],
        "ending_line": "I did not escape the pain. I gave it a direction.",
        "pause_points": ["after 'buried'", "after 'Not for sympathy'", "before final line"],
    }


def create_storyboard_output(script: dict) -> dict:
    return {
        "scenes": [
            {"time": "0-3s", "visual": "Dark room, close-up eyes, phone light on face.", "actor_action": "silent stare", "transition": "slow fade"},
            {"time": "3-8s", "visual": "Mirror reflection, one side of face in shadow.", "actor_action": "controlled breath", "transition": "hard cut"},
            {"time": "8-15s", "visual": "Hands writing on script page; laptop glow beside notebook.", "actor_action": "writes one line", "transition": "match cut"},
            {"time": "15-25s", "visual": "Gym close-ups: grip, breath, controlled repetition.", "actor_action": "controlled set", "transition": "rhythmic cut"},
            {"time": "25-35s", "visual": "Night walk, streetlight, slow push-in.", "actor_action": "walks forward", "transition": "slow push"},
            {"time": "35-45s", "visual": "Final still frame: direct eye contact in mirror.", "actor_action": "calm eye contact", "transition": "hold"},
        ]
    }


def create_visual_output(director: dict) -> dict:
    return {
        "color_mood": "midnight blue, black, charcoal grey, soft warm desk light",
        "lighting": "low-key lighting with controlled shadows and one practical light",
        "camera": "slow push-ins, static mirror frame, close-up eyes, side profile",
        "symbols": ["mirror", "script page", "laptop glow", "gym grip", "night street"],
        "final_frame": "calm direct eye contact; not broken, not fake, reconstructed",
    }


def create_subtitle_music_output() -> dict:
    return {
        "music_mood": "dark ambient piano with slow cinematic pulse, restrained rise",
        "subtitle_style": "clean white subtitles, minimal, highlight words: pain, structure, discipline, direction",
        "sound_design": "room tone, breath, soft keyboard clicks, subtle silence before final line",
        "pacing": "slow emotional start, rising tension, controlled final pause",
    }


def create_final_output(
    brief: CreativeBrief,
    director: dict,
    script: dict,
    storyboard: dict,
    visual: dict,
    subtitle_music: dict,
) -> dict:
    return {
        "title": "I Gave the Pain a Direction",
        "platform": brief.platform,
        "duration": brief.duration,
        "hook": script["hook"],
        "voiceover_script": script["voiceover"],
        "visual_direction": storyboard["scenes"],
        "music_mood": subtitle_music["music_mood"],
        "subtitle_style": subtitle_music["subtitle_style"],
        "editing_style": subtitle_music["pacing"],
        "ending_line": script["ending_line"],
        "call_to_action": "Follow the reconstruction.",
        "review_notes": [memory_note(brief)],
        "final_video_prompt": (
            "Create a dark cinematic short-form video about a man rebuilding himself "
            "from survival into disciplined identity. Use mirror reflections, close-up eyes, "
            "script pages, laptop glow, gym details, night streets, and a calm final frame. "
            "Keep the tone emotional, restrained, masculine, and public-safe."
        ),
        "director_notes": director,
        "visual_notes": visual,
        "sound_notes": subtitle_music,
    }
