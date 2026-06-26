# 1oVE Creative OS v1 — Local Creative Agent Runner

**Status:** v1.0.0 Release Locked  
**Universe:** The Reconstruction Era  
**Default mode:** local-first, privacy-first, public-safe

1oVE Creative OS v1 is a local creative operating system for building cinematic, emotionally intelligent, identity-driven short-form video concepts. It runs a structured creative workflow:

1. privacy gate
2. optional memory retrieval
3. six creative agents
4. four review agents
5. quality evaluation
6. Markdown/JSON output writing
7. content-history logging

This repository package is prepared from the locked master brain of **Master 1oVE Creative OS v1 — The Reconstruction Era**. It is release-locked as v1.0.0 after owner approval, Apache-2.0 license insertion, privacy boundary confirmation, and test validation.


## License

This project is released under the Apache License, Version 2.0.

SPDX-License-Identifier: Apache-2.0

See `LICENSE` and `NOTICE`.

## Quick Start

Extract to a short Windows path:

```text
C:\1ove_v1
```

Create a virtual environment:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the mock backend:

```bat
python run.py --backend mock --idea "A reel about rebuilding myself after survival mode"
```

Run all tests:

```bat
python tests\smoke_test.py
python tests\privacy_test.py
python tests\memory_test.py
python tests\eval_test.py
```

Outputs are written to:

```text
outputs/
```

## Local Model Backends

Supported backend modes:

- `mock` — safe offline test mode
- `ollama` — local Ollama server
- `openai_compatible` — LM Studio or other local OpenAI-compatible server

Example:

```bat
python run.py --backend ollama --idea "A cinematic reel about discipline after exhaustion"
```

## Privacy Default

The default privacy mode is `public_safe`.

Sensitive memory is not retrieved into prompts by default. Private memory is only allowed when using private draft modes. Public release packages must not contain private memory, sensitive JSONL logs, real names, addresses, phone numbers, or personal trauma details.

Read:

- `PRIVACY.md`
- `docs/public_sanitization.md`
- `docs/release_checklist.md`

## Important Release Blocker

This package is not publicly releasable until a license is selected.

Read:

- `LICENSE_PENDING.md`
- `docs/license_options.md`

## Repository Map

- `app/` — local runner modules
- `config/` — model, privacy, memory, evaluation, output schema configs
- `data/agents/` — creative agent cards
- `data/reviewers/` — review agent cards
- `data/knowledge/` — public-safe knowledge files
- `data/templates/` — output templates
- `data/workflows/` — workflow map
- `data/memory/` — local memory store folders, empty by default
- `docs/` — architecture, usage, privacy, release, and packaging docs
- `examples/` — sample ideas and expected workflow examples
- `scripts/` — Windows helper scripts
- `tests/` — smoke, privacy, memory, and evaluation tests
- `outputs/` — generated outputs, gitignored

## Current Stage

Stage 14 — Open-Source Repo Packaging.

Next stage:

```text
Stage 15 — v1 Release Candidate
```


## Stage 16 Status

This repo copy is packaged for final owner testing and public-release lock.

Current status:
- Local release candidate: READY_FOR_OWNER_TESTING
- Public release: HOLD until license is chosen and owner approval is signed
- License: PENDING_OWNER_DECISION

Start with:
- `release/OWNER_TEST_PLAN.md`
- `release/PUBLIC_RELEASE_LOCK_CHECKLIST.md`
- `release/OWNER_APPROVAL_GATE.md`
