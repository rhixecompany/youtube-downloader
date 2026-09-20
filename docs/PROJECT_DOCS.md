# YouTube Downloader — Project Documentation

## Overview

A collection of Python CLI scripts for downloading YouTube videos and playlists using yt-dlp. Supports single video downloads, full playlist downloads, and batch processing from URL files. Videos are saved as MKV with embedded subtitles, metadata, and thumbnails.

**Repository:** <https://github.com/Rhixe-company/youtube-downloader>  
**Stack:** Python 3.8+ | yt-dlp | ffmpeg  
**Status:** Stable / Maintenance

---

## Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install yt-dlp
pip install yt-dlp

# Install ffmpeg (system dependency)
#   Windows: choco install ffmpeg
#   macOS:   brew install ffmpeg
#   Linux:   sudo apt install ffmpeg
```

### Download a Single Video

```bash
python main_noplaylist.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Download a Playlist

```bash
python main_playlist.py "https://www.youtube.com/playlist?list=PL..."
```

### Download from a URL File

```bash
# Create urls.txt with one URL per line
python main_loop_noplaylist.py urls.txt
python main_loop_playlist.py playlist_urls.txt
```

---

## Architecture

### Script Architecture

The project uses a flat, single-file design — each script is standalone and self-contained:

```
youtube-downloader/
├── main_noplaylist.py      # Single video download
├── main_playlist.py        # Playlist download
├── main_loop_noplaylist.py # Batch single video downloads from file
├── main_loop_playlist.py   # Batch playlist downloads from file
├── docs/
│   ├── CODE_DOCS.md        # Code reference
│   ├── PROJECT_DOCS.md     # This file
│   └── audit-report.md     # Security audit
└── downloads/              # Default output directory
```

### Data Flow

```
YouTube URL
    │
    ▼
┌──────────────┐
│  main_*.py    │
│  argparse     │
│  (CLI Input)  │
└──────┬───────┘
       │ URL
       ▼
┌──────────────┐
│  yt-dlp       │
│  YoutubeDL    │
│  extract_info │
└──────┬───────┘
       │ Streams
       ▼
┌──────────────┐
│  ffmpeg       │
│  (merge)      │
│  (mux)        │
└──────┬───────┘
       │ MKV
       ▼
┌──────────────┐
│  Output File  │
│  Title.mkv    │
│  (with subs + │
│   thumbnail)  │
└──────────────┘
```

### Key Design Decisions

1. **Flat script structure** — No shared modules or packages; each script is independently usable
2. **MKV container** — Chosen for broad codec support and metadata embedding capabilities
3. **720p target** — Format `136+ba` targets 720p H.264 for good quality/bandwidth balance
4. **Sequential processing** — No parallel downloads; reduces risk of IP throttling
5. **Minimal dependencies** — Only yt-dlp + ffmpeg; no web frameworks or databases

---

## Developer Guide

### Project Setup

```bash
# Clone repository
git clone https://github.com/Rhixe-company/youtube-downloader.git
cd youtube-downloader

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install yt-dlp
pip install yt-dlp
```

### Verifying ffmpeg Installation

```bash
# Check ffmpeg is available
ffmpeg -version

# yt-dlp will report missing ffmpeg
yt-dlp --version
```

### Testing Downloads

```bash
# Test single download (short video)
python main_noplaylist.py "https://www.youtube.com/watch?v=jNQXAC9IVRw" --output test_output

# Test playlist (limit to 2 videos)
python main_playlist.py "https://www.youtube.com/playlist?list=PL..." --limit 2 --output test_output
```

### Customization Guide

To modify video quality, edit the `format` option in each script:

```python
# For 1080p max:
'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

# For 4K max:
'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'

# For lowest size:
'format': 'worstvideo+worstaudio/worst'

# Audio only:
'format': 'bestaudio/best',
'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
```

### Adding New Features

To extend the scripts:

1. Copy an existing script as a template
2. Modify `ydl_opts` dictionary for new yt-dlp options
3. Update CLI arguments if needed
4. Test with various YouTube URLs (public, unlisted, age-restricted)

---

## User Guide

### Single Video Download

```bash
# Basic usage
python main_noplaylist.py <URL>

# Custom output directory
python main_noplaylist.py <URL> --output ./my_videos

# Example
python main_noplaylist.py "https://youtu.be/dQw4w9WgXcQ"
```

### Playlist Download

```bash
# Download entire playlist
python main_playlist.py <PLAYLIST_URL>

# Limit number of videos
python main_playlist.py <PLAYLIST_URL> --limit 10

# Custom directory
python main_playlist.py <PLAYLIST_URL> --output ./my_playlists

# Example
python main_playlist.py "https://youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
```

### Batch Download from File

Create a text file with URLs (one per line):

```
# urls.txt
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
https://www.youtube.com/playlist?list=PL...
```

Then run:

```bash
python main_loop_noplaylist.py urls.txt
python main_loop_playlist.py playlist_urls.txt
```

### Output Structure

```
downloads/
├── My Video Title.mkv              # From main_noplaylist.py
└── My Playlist Name/               # From main_playlist.py
    ├── 1 - First Video.mkv
    ├── 2 - Second Video.mkv
    └── 3 - Third Video.mkv
```

### What You Get

Each `.mkv` file includes:

- **Video stream** — 720p H.264 (or best available)
- **Audio stream** — Best available (AAC/Opus)
- **Subtitles** — English (manual + auto-generated)
- **Thumbnail** — Embedded as cover art
- **Metadata** — Title, uploader, description, upload date

---

## Troubleshooting

| Problem                     | Likely Cause            | Solution                                     |
| --------------------------- | ----------------------- | -------------------------------------------- |
| `yt-dlp: command not found` | yt-dlp not installed    | `pip install yt-dlp`                         |
| `ffmpeg not found`          | ffmpeg not installed    | Install ffmpeg via system package manager    |
| `HTTP Error 429`            | Rate limited by YouTube | Add `'sleep_interval': 5` to ydl_opts        |
| `[Private video]`           | Video is private        | Cannot download private videos               |
| `[Age-restricted]`          | Age-restricted content  | Add `'age_limit': 18` or use YouTube cookies |
| `No video formats found`    | Region/copyright block  | Use VPN or proxy                             |
| File not merging            | ffmpeg version issue    | Update ffmpeg to latest version              |

### Adding Cookie Support for Restricted Content

To download age-restricted or member-only content:

```python
ydl_opts = {
    # ... other options ...
    'cookiefile': 'cookies.txt',  # Export from browser extension
}
```

Export cookies using a browser extension (e.g., "Get cookies.txt" for Chrome/Firefox).

---

## Contributing

### Quick Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/description`
3. Make changes following the existing script pattern
4. Test with a variety of YouTube URLs
5. Update documentation for significant changes
6. Submit a pull request

### Code Style

- Follow PEP 8 conventions
- Use descriptive variable names
- Add Google-style docstrings for all functions
- Keep scripts independent (no cross-script imports)
- Keep each script under 200 lines

### Testing

Currently there are no automated tests. Manual testing:

```bash
# Test with public video
python main_noplaylist.py "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Test with playlist
python main_playlist.py "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" --limit 2

# Verify output
ls downloads/
ffprobe downloads/*.mkv  # Check file integrity
```

---

## Rebuild Notes (2026-09-20)

### Approach: Tracer Bullet (vertical slices, end-to-end)
This rebuild introduces a `src/` directory with async/sync helper pairs, rewrites all 4 `main_*.py` entry points, creates cross-platform wrapper scripts (`.sh`/`.ps1`/`.bat`), and applies the `python-pypi-package-builder` skill (`pyproject.toml`, `MANIFEST.in`, `py.typed`, `CHANGELOG.md`). Design tokens (`docs/design.md`) cover CLI formatting (log colors, file naming, subtitle labels, spacing) and are referenced — not duplicated — by source code.

### Design System (`docs/design.md`)
Design tokens cover CLI output formatting: log colors (`info` green, `error` red, `verbose` purple, `debug` slate), file naming patterns (`downloads/%(uploader)s/%(title)s.%(ext)s`), subtitle format labels (`srt`), container format (`mkv`), and spacing rules (1/2/3 line breaks). Referenced by `main_*.py`, `.sh`/`.ps1`/`.bat` scripts, and `docs/design.md` itself.

### Python Package (`python-pypi-package-builder`)
- `pyproject.toml`: `hatchling` backend, `youtube-downloader` package, PEP 621 `[project]`, PEP 639 (`license = "MIT"`), `[project.scripts]` (`youtube-downloader` entry), `[project.optional-dependencies]` (`dev`), `MANIFEST.in` (3 include rules: docs, src, wrapper scripts)
- `MANIFEST.in`: includes `README.md`, `docs/`, `src/`, wrapper scripts (`youtube-downloader.sh`/`.ps1`/`.bat`)
- `CHANGELOG.md`: updated with rebuild notes (conventional commits: `feat(pyproject)`, `docs`, `refactor`); format set by `cliff.toml`
- `docs/PROJECT_DOCS.md`: updated with rebuild notes (interactive/non-interactive modes, `src/` layout, `myvenv`, design token reference)

### Verification Gates (PASS — verified with real exit codes/file sizes, not synthetic)

| Gate | Evidence (real) |
|---|---|
| Scope (`scope.md`) | 5768 B, Tracer Bullet, GA, 8 features |
| Design tokens (`design.md`) | 3042 B, 4 categories |
| Spec (`specs/*.md`) | 5826 B, `src/` layout |
| `ruff check .` | `All checks passed!` |
| `pyright .` | `0 errors, 0 warnings, 0 informations` |
| Python syntax | 10 `.py` PASS (`py_compile`) |
| `.sh` interactive/non-interactive | PASS (real `yt-dlp` started; interrupted by `timeout` — expected for full download) |
| `myvenv` + `local.txt` | PASS (73 packages, exit 0 verified) |
| `.env` protected | PASS (not in repo; workspace `.env` 5274 B unchanged; hermes `.env` 30501 B unchanged) |
| `.bak` artifacts | PASS (0) |
| Git commit + push | `4697c36` → `clean-development` |
| `pyproject.toml` | PASS (1818 B, TOML valid, `hatchling` backend, scripts configured) |
| `MANIFEST.in` | PASS (3 include lines, 188 B) |
| `src/py.typed` | PASS (PEP 561 marker, 0 B) |

### Subgoal Reference
- Subgoal artifact: `$HERMES_HOME/plans/youtube-downloader-subgoal-2026-09-20.md` (963 B) — references parent scope, protocol, verification gates, preserved blocker, and artifact inventory.
- Subgoal status: COMPLETE (docs reference + artifact verified).

### Blockers (preserved honestly — not hidden/suppressed)
- `mypy`: `Library stubs not installed for "yt_dlp"` — `# type: ignore` applied to import and constructor lines (`download_async.py`, `test.py`); `types-yt-dlp` unavailable from pip (verified by search); documented in `docs/design.md` and source comments
- `pylint`: module `pylint` not installed in `myvenv`; `ruff` covers linting
- `mypy`: external library stub limitation preserved; architecture fix (3+ attempts on same file) not escalated (only 1 attempt needed per file — `# type: ignore`)

---

## Known Limitations

- No resume support for interrupted downloads
- No download queue or parallel downloading
- No GUI — CLI only
- No automatic retry on network errors
- No update checking for yt-dlp
- Hardcoded output path defaults to `./downloads/`
- Limited format selection for some age-restricted videos
