from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.privacy_gate import apply_privacy_gate, detect_sensitive_terms

text = "This includes diagnosis and private memory."
safe, hits = apply_privacy_gate(text, "public_safe")
assert hits, "Expected sensitive hits"
assert "diagnosis" not in safe.lower()
assert "private memory" not in safe.lower()
assert detect_sensitive_terms(text)
print("Stage 13 privacy test passed.")
