# Copilot Instructions — youtube-downloader

**Workspace rules:** Read `../../AGENTS.md` before repository-wide work. It is the canonical source for shared safety, clarification, artifact, planning, and verification protocols. Preserve the existing `.cursorrules` and `AGENTS.md` references rather than duplicating workspace policy here.

## Project identity

- Python 3.11+ CLI utility built around `yt-dlp`, `curl_cffi`, and external FFmpeg.
- The supported product surface is command-line downloading; there is no web application, database, or service layer.
- Keep `.env`, cookies, credentials, and downloaded media out of commits. Treat URLs and downloaded content as untrusted input.

## Setup and quality commands

Run commands from the repository root.

```bash
# Install runtime dependencies
python -m pip install -r requirements/base.txt

# Install development tooling declared by the package
python -m pip install -e ".[dev]"

# Lint
ruff check .

# Type check
pyright .
# Alternative configured checker:
mypy *.py
```

Testing has two observed paths:

```bash
# CI/manual smoke test
python test.py

# Pytest configuration in pyproject.toml
python -m pytest

# Run one pytest test
python -m pytest tests/test_file.py::test_name
```

The CI workflow currently installs `ruff` and `yt-dlp`, then runs `ruff check .` and `python test.py`. Keep `test.py` working when changing download defaults or entry-point behavior. If adding pytest tests, place them under `tests/` so they are discovered by the configured `testpaths`.

CLI smoke runs require FFmpeg and may perform real network downloads. Prefer mocked/unit coverage or a narrowly scoped public fixture when validating behavior; do not commit downloaded files.

## Architecture

The four root entry points provide distinct CLI modes:

- `main_noplaylist.py`: one video, with interactive input by default or a URL argument in non-interactive use.
- `main_playlist.py`: one playlist, overriding shared options for playlist output naming.
- `main_loop_noplaylist.py`: repeated single-video downloads from multiple URLs.
- `main_loop_playlist.py`: repeated playlist downloads from multiple URLs.

Entry points use shared modules under `src/`:

- `src/config/yt_opts_defaults.py` owns the common yt-dlp options: format selection, MKV merging, subtitles, thumbnails, and the default `downloads/%(uploader)s/%(title)s.%(ext)s` template.
- `src/helpers/download_async.py` contains the blocking yt-dlp operation plus an async wrapper that runs it in an executor. `DownloadResult` carries the resulting media path and optional subtitle/thumbnail paths.
- `src/helpers/cli_input_async.py` provides matching async/sync interactive URL input helpers.
- `src/helpers/file_io_async.py` provides matching async/sync file operations for supporting workflows.

The data flow is CLI input → entry-point-specific yt-dlp options → shared download helper → yt-dlp/HTTP retrieval → FFmpeg post-processing → files under `downloads/`, with progress/log output on the console. Root `.sh`, `.ps1`, and `.bat` wrappers delegate to the Python entry points for cross-platform invocation.

## Repository-specific conventions

- Keep each download mode in its own `main_*.py` entry point; put reusable behavior in `src/helpers` or shared configuration rather than duplicating yt-dlp setup.
- Preserve the async/sync helper pairing when adding public helper behavior.
- Copy `DEFAULT_YT_OPTS` before per-mode changes. Playlist modes should override `noplaylist` and use the playlist-specific output template rather than mutating shared defaults.
- Interactive mode is the default when no URL argument is supplied; URL arguments are treated as non-interactive input. Preserve the existing `--interactive`/`--non-interactive` behavior.
- Preserve output conventions from `docs/design.md`: MKV container, SRT subtitles, uploader/title paths for videos, and playlist-title/index paths for playlists. Update code and design tokens together when naming or formatting changes.
- Use 4-space Python indentation, snake_case names, type annotations where practical, and the repository's Ruff configuration (120-character lines, import sorting, and selected correctness rules).
- Keep network/download failures explicit. Do not silently convert failed downloads or file writes into success-shaped results.
- Follow the focused commit style documented in `CONTRIBUTING.md` (`feat:`, `fix:`, `docs:`, etc.) and update directly related documentation for behavior or workflow changes.

## Related project guidance

- `README.md`: user-facing commands, dependencies, and feature overview.
- `CONTRIBUTING.md`: contribution flow and commit expectations.
- `docs/design.md`: CLI formatting and file naming tokens; do not duplicate token values in code.
- `docs/SETUP.md`: environment setup and common commands.
- `.cursorrules`: editor-specific conventions that also apply when editing Python here.
