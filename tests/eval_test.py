from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.evaluator import evaluate_output
from app.review_runner import run_reviews
from app.mock_model import create_director_output, create_script_output, create_storyboard_output, create_visual_output, create_subtitle_music_output, create_final_output
from app.types import CreativeBrief

brief = CreativeBrief("A reel about rebuilding myself after survival mode", "Reels", "30s")
director = create_director_output(brief)
script = create_script_output(brief, director)
story = create_storyboard_output(script)
visual = create_visual_output(director)
sound = create_subtitle_music_output()
final = create_final_output(brief, director, script, story, visual, sound)
reviews = run_reviews(final)
evaluation = evaluate_output(final, reviews)
assert evaluation.decision in {"READY", "NEEDS_TUNING"}
print("Stage 13 evaluation test passed.")
