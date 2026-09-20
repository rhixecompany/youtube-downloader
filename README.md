# youtube-downloader — CLI Video Downloader

> **Stack:** Python ≥3.11 + yt-dlp | **Type:** CLI utility | **Status:** Active | **License:** MIT

Python CLI for downloading YouTube videos (single, playlist, and loop modes) via yt-dlp and curl_cffi. No web deployment.

---

## Technology stack

| Category | Technology |
| --- | --- |
| Runtime | Python ≥3.11 |
| Download engine | yt-dlp |
| HTTP client | curl_cffi (via `yt-dlp[curl-cffi]`) |
| Media processing | FFmpeg (external) |
| Lint | ruff |
| Type check | pyright (primary); mypy optional |

## Architecture

```
User Command → main_*.py entrypoint
                    ↓
              src/ helpers + DEFAULT_YT_OPTS
                    ↓
                 yt-dlp API
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
    HTTP (curl_cffi)      FFmpeg merge/convert
        ↓                       ↓
    downloads/…          Console progress
```

## Project structure

```
youtube-downloader/
├── main_noplaylist.py          # Single video
├── main_playlist.py            # Playlist
├── main_loop_noplaylist.py     # Loop: single videos
├── main_loop_playlist.py       # Loop: playlists
├── test.py                     # CI/manual smoke (may download)
├── youtube-downloader.bat      # Windows wrapper → main_noplaylist
├── youtube-downloader.ps1
├── youtube-downloader.sh
├── src/
│   ├── config/yt_opts_defaults.py
│   └── helpers/                # download / CLI / file async+sync helpers
├── requirements/
│   ├── base.txt                # Shared/tooling pins (no yt-dlp alone)
│   └── local.txt               # Local install incl. yt-dlp[curl-cffi]
├── docs/
│   ├── SETUP.md
│   └── design.md               # CLI / output naming tokens
├── pyproject.toml
├── package.json                # bun wrappers: lint / typecheck
└── AGENTS.md                   # Agent project context
```

## Getting started

```bash
# Prerequisites: Python ≥3.11, FFmpeg on PATH

python -m venv myvenv
# Windows: myvenv\Scripts\activate
# Linux/macOS: source myvenv/bin/activate
# Wrappers (.bat/.ps1/.sh) expect the in-tree "myvenv" virtual environment.

pip install -r requirements/local.txt
# Or runtime only: pip install "yt-dlp[curl-cffi]"
# Dev tooling: pip install -e ".[dev]"

python main_noplaylist.py       # single video
python main_playlist.py         # playlist
python main_loop_noplaylist.py  # loop singles
python main_loop_playlist.py    # loop playlists

# Wrappers (single-video entry)
./youtube-downloader.sh
# youtube-downloader.bat / youtube-downloader.ps1 on Windows

python test.py                  # smoke (network)
ruff check .                    # or: bun run lint
pyright .                       # or: bun run typecheck
```

More detail: [`docs/SETUP.md`](docs/SETUP.md). Agent conventions: [`AGENTS.md`](AGENTS.md).

## Key features

- Single video, playlist, and loop modes
- Shared yt-dlp defaults (format, MKV merge, subtitles, thumbnails)
- curl_cffi fingerprinting via yt-dlp extra
- FFmpeg post-processing
- Cross-platform wrappers (`.bat` / `.ps1` / `.sh`)

## Scripts overview

| Script | Purpose |
| --- | --- |
| `main_noplaylist.py` | Download a single video |
| `main_playlist.py` | Download a playlist |
| `main_loop_noplaylist.py` | Batch loop of single-video URLs |
| `main_loop_playlist.py` | Batch loop of playlist URLs |
| `test.py` | Manual/CI smoke (not a unit suite) |

## Coding standards

- PEP 8, snake_case, 4-space indent, double quotes
- Prefer type annotations; primary check is pyright
- Copy `DEFAULT_YT_OPTS` per mode; keep tokens in sync with `docs/design.md`
- Explicit error handling for network/download failures

## Usage tips

- Keep yt-dlp updated: `pip install -U "yt-dlp[curl-cffi]"`
- FFmpeg is required for merge/conversion
- Prefer updating yt-dlp first when downloads fail
- Respect YouTube Terms of Service; personal use only

## Security

- Do not commit `.env`, cookies, credentials, or `downloads/`
- Treat URLs and downloaded files as untrusted
- No mass or commercial scraping use

## Dependencies

| Library | Purpose |
| --- | --- |
| **yt-dlp** | Download engine |
| **curl_cffi** | HTTP fingerprinting (yt-dlp extra) |
| **FFmpeg** | External merge / conversion |

## License

MIT — see [`LICENSE`](LICENSE).
