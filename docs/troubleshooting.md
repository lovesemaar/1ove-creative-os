# Troubleshooting

## Error: Path too long

Extract to:

```text
C:\1ove_s14
```

## Local model fails

Run mock first:

```bat
python run.py --backend mock --idea "test"
```

Then check `config/model.json`.

## Output rejected

Open the generated evaluation scorecard inside `outputs/`. Rejections usually come from:

- missing required sections
- generic voice
- weak cinematic visuals
- privacy risk
- low production usefulness

## Memory not found

Add public/project memory first:

```bat
python memory_cli.py add --title "Brand rule" --tier public --category brand --tags brand --text "Every output must feel like The Reconstruction Era."
```
