# Setup Guide

## Prerequisites

- Python 3.11 or newer: `python --version`
- FFmpeg on PATH: `ffmpeg -version`
- Git: `git --version`

## One-time setup

Run from this project root (`projects/youtube-downloader`).

```bash
python -m venv myvenv
# Windows cmd:    myvenv\Scripts\activate
# PowerShell:    myvenv\Scripts\Activate.ps1
# Git bash / Linux / macOS: source myvenv/bin/activate

pip install -r requirements/local.txt
# Dev extras (ruff, pyright, pytest, build tooling): pip install -e ".[dev]"
```

The wrapper scripts (`.bat`, `.ps1`, `.sh`) expect the in-tree `myvenv` folder.
If it is missing they print a guard message instead of running.

## Usage

| Mode | Command |
| --- | --- |
| Interactive (prompts) | `./youtube-downloader.sh` · `youtube-downloader.bat` · `.\youtube-downloader.ps1` |
| Non-interactive with URL | `./youtube-downloader.sh --non-interactive "https://youtube.com/watch?v=xxx"` (same flag on `.bat` / `.ps1`) |
| Direct, single video | `python main_noplaylist.py "URL"` (URL omitted = interactive) |
| Direct, playlist | `python main_playlist.py "URL"` |
| Direct, loop from file | `python main_loop_noplaylist.py urls.txt` · `python main_loop_playlist.py urls.txt` |

## Checks

| Check | Command |
| --- | --- |
| Lint | `ruff check .` (config: `.ruff.toml`) or `bun run lint` |
| Typecheck | `pyright .` (config: `pyrightconfig.json`) or `bun run typecheck` |
| Smoke test | `python test.py` (interactive, may hit the network) |

There is no `tests/` directory; `python -m pytest` finds nothing.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: No module named 'yt_dlp'` | `pip install -U "yt-dlp[curl-cffi]"` (or reinstall `requirements/local.txt`) |
| Wrapper prints a virtual environment guard | Create `myvenv` (see setup above) |
| `cmd` splits the URL at `&` | Quote the URL: `youtube-downloader.bat --non-interactive "https://...?v=x&t=1s"` |
| Old `.bat` says `was unexpected at this time.` | Use the current wrapper (fixed parse error) |
| `ffmpeg not found` | Install FFmpeg and add it to PATH |