from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.memory_store import MemoryEntry, append_memory, init_memory
from app.retriever import retrieve_memory

init_memory()
append_memory(MemoryEntry(
    title="Test Reconstruction Memory",
    tier="public",
    category="brand",
    tags=["reconstruction", "test"],
    text="Reconstruction means survival becoming structure.",
))
rows = retrieve_memory("reconstruction structure", privacy_mode="public_safe")
assert rows, "Expected memory retrieval result"
print("Stage 13 memory test passed.")
