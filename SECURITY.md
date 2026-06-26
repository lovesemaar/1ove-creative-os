# Security Policy

## Supported Status

This is a local prototype/release candidate package, not a hosted service.

## Reporting Security Issues

Before public release, security issues should be tracked privately in the creator's issue log.

## Local Safety Notes

- Do not commit `.env` files.
- Do not commit `outputs/`.
- Do not commit private memory JSONL files.
- Do not expose local model server endpoints publicly.
- Keep Ollama or LM Studio local unless you understand network exposure risks.
- Review `docs/public_sanitization.md` before publishing.

## Sensitive Data

Any memory file under `data/memory/private/` or sensitive memory locations should remain local and gitignored.
