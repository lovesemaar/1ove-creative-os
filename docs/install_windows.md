# Windows Install Guide

## 1. Extract to short path

```text
C:\1ove_s14
```

## 2. Open terminal

```bat
cd C:\1ove_s14
```

## 3. Create environment

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run mock backend

```bat
python run.py --backend mock --idea "A reel about rebuilding myself after survival mode"
```

## 5. Run tests

```bat
python tests\smoke_test.py
python tests\privacy_test.py
python tests\memory_test.py
python tests\eval_test.py
```

## 6. Optional local model

Install Ollama or run LM Studio locally, then update `config/model.json`.
