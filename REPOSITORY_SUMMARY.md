# REPOSITORY_SUMMARY.md

# YouTube Downloader — Python CLI Tool

**Generated:** 2026-07-25  
**Project:** `projects/youtube-downloader/`  
**Type:** Python CLI (yt-dlp wrapper)  
**Status:** Active

---

## Architecture

| Property    | Value                              |
| ----------- | ---------------------------------- |
| **Type**    | Single-file Python CLI scripts     |
| **Pattern** | Wrapper around yt-dlp + curl_cffi  |
| **Modes**   | Single video, playlist, loop/batch |

---

## Technology Stack

| Layer        | Technology                                   |
| ------------ | -------------------------------------------- |
| **Language** | Python 3.x                                   |
| **Core**     | `yt-dlp`, `curl_cffi`                        |
| **Quality**  | `ruff` (lint), `mypy` (type check, optional) |
| **External** | FFmpeg (for post-processing)                 |

---

## Project Structure

```
youtube-downloader/
├── main_noplaylist.py      # Single video download
├── main_playlist.py        # Playlist download
├── main_loop_playlist.py   # Batch loop mode
├── main_loop_noplaylist.py # Batch single videos
├── test.py                 # Test script
├── requirements.txt
├── .gitignore
└── README.md (inferred)
```

---

## Commands

```bash
pip install yt-dlp curl_cffi
# FFmpeg required for format conversion

# Single video
python main_noplaylist.py

# Playlist
python main_playlist.py

# Loop modes (batch)
python main_loop_playlist.py
python main_loop_noplaylist.py

# Quality
ruff check . && mypy *.py
python test.py
```

---

## Modes

| Script                    | Purpose                               |
| ------------------------- | ------------------------------------- |
| `main_noplaylist.py`      | Download single video                 |
| `main_playlist.py`        | Download entire playlist              |
| `main_loop_playlist.py`   | Batch download multiple playlists     |
| `main_loop_noplaylist.py` | Batch download multiple single videos |

---

## Conventions

- Pure CLI — no web UI, no framework
- `.env` / URLs never committed
- Keep yt-dlp updated for site compatibility
- FFmpeg required for format conversions
- Polite delays between requests

---

## CI/CD

**Workflow:** `.github/workflows/youtube-downloader-ci.yml`  
**Jobs:** Install → Ruff → MyPy → CLI help test → Dry-run download test
