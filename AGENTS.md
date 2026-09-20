# youtube-downloader — AGENTS.md

**Canonical workspace context:** [`../../AGENTS.md`](../../AGENTS.md)  
This file holds **only** youtube-downloader-specific overrides, commands, and conventions.

## Project identity

- Python **≥3.11** CLI utility around `yt-dlp`, `curl_cffi`, and external **FFmpeg**.
- Supported surface: command-line download only (no web app, database, or service layer).
- Keep `.env`, cookies, credentials, and `downloads/` out of commits. Treat URLs and media as untrusted.

## Project-specific commands

Run from this project root (`projects/youtube-downloader`).

```bash
# Setup
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements/local.txt
# Dev extras (ruff, mypy, pytest, …): pip install -e ".[dev]"

# Lint / typecheck (package.json wrappers)
ruff check .          # bun run lint
pyright .             # bun run typecheck
# Optional: mypy *.py

# Smoke (CI path — may hit the network / download)
python test.py

# Pytest (configured for tests/; directory may be empty)
python -m pytest
```

Entrypoints:

| Script | Purpose |
| --- | --- |
| `main_noplaylist.py` | Single video (interactive default or URL arg) |
| `main_playlist.py` | One playlist |
| `main_loop_noplaylist.py` | Repeated single-video URLs |
| `main_loop_playlist.py` | Repeated playlist URLs |
| `youtube-downloader.{bat,ps1,sh}` | Wrappers → `main_noplaylist.py` |

Console script (hatchling): `youtube-downloader` → `main_noplaylist:main`.

CI (`.github/workflows/ci.yml`): Python 3.11 → `ruff check .` → `python test.py`.

## Project-specific conventions

- Keep each download mode in its own `main_*.py`; put shared behavior under `src/` (`config/yt_opts_defaults.py`, `helpers/*_async.py`).
- Copy `DEFAULT_YT_OPTS` before per-mode changes; playlist modes override `noplaylist` and output templates.
- Sync naming/format tokens with [`docs/design.md`](docs/design.md) (MKV, SRT, uploader/title paths).
- Python: 4-space indent, double quotes, snake_case, Ruff line-length 120 (`ruff check .`).
- Prefer `pyright .` as the primary typecheck; mypy is optional.
- Do not invent verification results; do not write `.env` or commit downloads.
- Multi-file changes (≥5 files): see [`../../SOUL.md`](../../SOUL.md).

## Honest gaps

- Wrappers do not implement `--dry-run` yet (SandBox multi-wrapper convention).
- `tests/` may be absent; `test.py` is a live smoke script, not a unit suite.
- `requirements/base.txt` alone does **not** install yt-dlp; use `requirements/local.txt` or `yt-dlp[curl-cffi]`.

## Adapters

| File | Role |
| --- | --- |
| [`.cursorrules`](.cursorrules) | Cursor IDE adapter |
| [`CLAUDE.md`](CLAUDE.md) | Claude thin pointer |
| [`.hermes.md`](.hermes.md) | Hermes thin pointer → [`../../.hermes.md`](../../.hermes.md) |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Copilot project adapter |
| [`README.md`](README.md) | User-facing overview |

---

*Shared safety, clarification, artifacts, and toolchain: [`../../AGENTS.md`](../../AGENTS.md).*
