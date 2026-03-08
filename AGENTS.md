# AGENTS.md

## Cursor Cloud specific instructions

This is a minimal Python CLI chatbot that talks to the GigaChat API (Sber's LLM service). There is a single entry point: `main.py`.

### Project structure

- `main.py` — Interactive console chatbot (the only source file)
- `requirements.txt` — Python dependencies
- `.env.example` — Template for environment variables
- `.env` — Local env file (not committed); copy from `.env.example`

### Running the app

```bash
python main.py
```

Requires `GIGACHAT_CREDENTIALS` in `.env` (a Base64-encoded authorization key from https://developers.sber.ru/studio/). Without valid credentials, the app starts but API calls fail with a 400 auth error.

### Key caveats

- **No test suite or lint config exists.** Use `python -m py_compile main.py` to check syntax and `python -m pyflakes main.py` for basic linting.
- **No build step.** The app runs directly with `python main.py`.
- The GigaChat SDK does not validate credentials at startup — only when an actual API call is made. The app will appear to start fine with placeholder credentials.
- The `GIGACHAT_CREDENTIALS` environment variable (injected as a secret) must be written into `.env` before running `main.py`, since the app reads credentials via `python-dotenv` from that file, not directly from the shell environment.
- Standard commands are documented in `README.md`.
