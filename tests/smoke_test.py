from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.orchestrator import run_workflow

out = run_workflow(
    idea="A reel about rebuilding myself after survival mode",
    platform="Instagram Reels",
    duration="30 seconds",
    privacy_mode="public_safe",
    use_memory=False,
    model_backend="mock",
)
assert out.exists(), "Output markdown was not created"
assert out.with_suffix(".json").exists(), "JSON output was not created"
assert out.with_suffix(".scorecard.json").exists(), "Scorecard output was not created"
print("Stage 13 smoke test passed.")
