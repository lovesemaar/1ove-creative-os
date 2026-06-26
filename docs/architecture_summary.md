# Architecture Summary

1oVE Creative OS v1 runs as a local creative pipeline.

## Flow

User idea
↓
Privacy gate
↓
Optional memory retrieval
↓
Creative agents
↓
Review agents
↓
Evaluation scorecard
↓
Output writer
↓
Content-history memory log

## Core Components

- `app/privacy_gate.py`
- `app/memory_store.py`
- `app/retriever.py`
- `app/model_client.py`
- `app/agent_runner.py`
- `app/review_runner.py`
- `app/evaluator.py`
- `app/output_writer.py`
- `app/orchestrator.py`

## Design Principle

The system should remain local-first, privacy-aware, cinematic, identity-driven, and modular.
