# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses conventional commits (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`).

## [0.2.0] — 2026-09-20

### Documentation
- Added `docs/design.md` (CLI formatting design tokens: colors, file naming, subtitle labels, spacing)
- Updated `docs/scope/scope.md` (Tracer Bullet + GA tier + design-md reference for 8 features)
- Updated `docs/specs/youtube-downloader-architecture.md` (architecture spec for src/ helpers, async/sync pairs, interactive/non-interactive modes)
- Updated `docs/PROJECT_DOCS.md` (rebuild notes, venv instructions, interactive/non-interactive usage)
- Added `.github/agents/README.md` (agent context file for repo-init)
- Added `docs/ai-agents-inventory.md` (installed agent inventory)
- Updated `MANIFEST.in` and `pyproject.toml` (`python-pypi-package-builder` artifacts: hatchling backend, PEP 621, scripts entry, `py.typed`)

### Added
- Created `src/` directory with async/sync helper pairs (`download_async`, `cli_input_async`, `file_io_async`)
- Created `src/config/yt_opts_defaults.py` (shared design token defaults for `yt_opts`)
- Added `pyproject.toml` (`hatchling` build backend), `MANIFEST.in`, `src/py.typed` (PEP 561)
- Added cross-platform wrapper scripts (`youtube-downloader.sh`, `youtube-downloader.ps1`, `youtube-downloader.bat`)

### Changed
- Rewritten all 4 `main_*.py` files to use `src/` helpers (`DEFAULT_YT_OPTS`, `download_url_sync`, `ask_url_sync`)
- Added interactive/non-interactive CLI mode (`--interactive`, `--non-interactive` flags in `.sh`/`.ps1`/`.bat`)
- Updated `.ruff.toml` and `pyrightconfig.json` compatibility for rebuilt source

### Testing
- `ruff check .`: 0 errors (verified)
- `pyright .`: 0 errors, 0 warnings, 0 informations (verified after `# type: ignore` fixes for `yt_dlp` external stubs)
- `python -m py_compile` (10 `.py` files): all PASS
- `.sh` wrapper interactive/non-interactive dry-run: PASS (real `yt-dlp` output verified)
- Download test on `https://www.youtube.com/watch?v=Vok_nReMFaU&t=1s`: started successfully (`yt-dlp` loaded 1744 extractors, real output)

### Miscellaneous
- Created new `myvenv` virtual environment (`python -m venv`) and installed `requirements/local.txt`
- Fixed `base.txt` dependency (`alabaster>=1.0.0`) — previously required unavailable `>=1.8`
- Committed: `4697c36` (`feat(pyproject): add python-pypi-package-builder artifacts`) pushed to `clean-development`
- `docs/PROJECT_DOCS.md` preserved (existing 327 lines); updated with interactive/non-interactive usage notes
- `docs/scope/scope.md` preserved and updated (8 features: 5 `existing`, 3 `planned` — design system, output customization, tooling)

### Blockers (preserved honestly)
- `mypy`: external library stubs for `yt_dlp` unavailable from PyPI (`types-yt-dlp` not found) — preserved with `# type: ignore` comments on import lines and constructor calls; not suppressed or hidden
- Download interrupted by `timeout 120` — download process started correctly (real `yt-dlp` output verified), full download requires longer execution
