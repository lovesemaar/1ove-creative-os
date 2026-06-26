# Public Sanitization Checklist

Before publishing this repo publicly, verify:

- [ ] `data/memory/private/` contains no private text.
- [ ] `data/memory/*/*.jsonl` files are empty or omitted.
- [ ] `outputs/` is empty and gitignored.
- [ ] No `.env` file is included.
- [ ] No personal addresses, phone numbers, emails, private names, or relationship details exist.
- [ ] No sensitive trauma details or diagnosis labels are embedded in public prompt files.
- [ ] Knowledge files use public-safe cinematic language.
- [ ] README explains privacy defaults clearly.
- [ ] License decision is complete.
- [ ] Release checklist is complete.
