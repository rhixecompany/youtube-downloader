# 🏗 Technology Stack Blueprint - youtube-downloader

**Project Path:** `projects/youtube-downloader`
**Generated:** 2026-07-28
**Status:** Active — Python CLI Tool (yt-dlp + curl_cffi)

---

## Core Technologies

| Category         | Technology | Version                 | License   |
| ---------------- | ---------- | ----------------------- | --------- |
| **Language**     | Python     | 3.x (3.11+ recommended) | PSF       |
| **Core Library** | yt-dlp     | Latest                  | Unlicense |
| **HTTP Client**  | curl_cffi  | Latest                  | MIT       |
| **External**     | FFmpeg     | Latest                  | GPL/LGPL  |

---

## Architecture

**Pattern:** Single-file CLI scripts with shared utilities

```
youtube-downloader/
├── main_noplaylist.py      # Single video download
├── main_playlist.py        # Playlist download
├── main_loop_noplaylist.py # Batch single videos
├── main_loop_playlist.py   # Batch playlists
├── test.py                 # Test suite
└── requirements.txt        # (inferred)
```

### Script Purposes

| Script                    | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| `main_noplaylist.py`      | Download single video/audio               |
| `main_playlist.py`        | Download entire playlist                  |
| `main_loop_noplaylist.py` | Loop: download multiple single URLs       |
| `main_loop_playlist.py`   | Loop: download multiple playlists         |
| `test.py`                 | Verify installation & basic functionality |

---

## Dependencies

### Python Packages

```text
yt-dlp>=2024.1.0
curl_cffi>=0.7.0
```

### System Dependencies

```bash
# FFmpeg (required for post-processing)
# macOS: brew install ffmpeg
# Ubuntu: apt install ffmpeg
# Windows: choco install ffmpeg or download from ffmpeg.org

# Python 3.11+
```

### Optional Quality Tools

```text
ruff>=0.1.0      # Linting
mypy>=1.0.0      # Type checking
pytest>=7.0.0    # Testing
```

---

## Usage

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install yt-dlp curl_cffi

# Verify FFmpeg
ffmpeg -version
```

### Commands

| Task                | Command                                                           |
| ------------------- | ----------------------------------------------------------------- |
| **Single video**    | `python main_noplaylist.py "https://youtube.com/watch?v=..."`     |
| **Playlist**        | `python main_playlist.py "https://youtube.com/playlist?list=..."` |
| **Batch singles**   | `python main_loop_noplaylist.py urls.txt`                         |
| **Batch playlists** | `python main_loop_playlist.py playlists.txt`                      |
| **Run tests**       | `python test.py`                                                  |
| **Lint**            | `ruff check .`                                                    |
| **Type check**      | `mypy *.py`                                                       |

### Input Files Format

```
# urls.txt (one per line)
https://youtube.com/watch?v=abc123
https://youtube.com/watch?v=def456

# playlists.txt (one per line)
https://youtube.com/playlist?list=PLxxx
https://youtube.com/playlist?list=PLyyy
```

---

## Key Features

### yt-dlp Capabilities

- **400+ sites** supported (YouTube, Vimeo, Twitter, etc.)
- **Format selection**: best, worst, specific codecs, audio-only
- **Subtitles**: Download, embed, convert formats
- **Metadata**: Embed thumbnail, chapters, info.json
- **Post-processors**: FFmpeg for conversion, merging, thumbnails
- **SponsorBlock**: Remove sponsored segments
- **Cookies**: Browser cookie extraction for private content

### curl_cffi Benefits

- **TLS fingerprinting** bypasses some bot detection
- **HTTP/2** support
- **Browser-like** request profiles (Chrome, Firefox, Safari)

---

## Coding Conventions

| Convention      | Standard                                                       |
| --------------- | -------------------------------------------------------------- |
| **Style**       | PEP 8                                                          |
| **Indentation** | 4 spaces                                                       |
| **Quotes**      | Double quotes (`"`)                                            |
| **Naming**      | `snake_case` for functions/variables, `PascalCase` for classes |
| **Type Hints**  | Encouraged for new scripts                                     |
| **Docstrings**  | Module-level + function docstrings                             |
| **Entry Point** | `if __name__ == "__main__":`                                   |

---

## Quality Tools Configuration

### Ruff (`.ruff.toml` or `pyproject.toml`)

```toml
[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "ARG", "RUF"]
ignore = ["E501", "N818"]
```

### MyPy

```toml
[tool.mypy]
python_version = "3.11"
check_untyped_defs = true
warn_unused_ignores = true
```

### Black

```toml
[tool.black]
line-length = 119
target-version = ['py312']
```

---

## CI/CD

**Workflow:** `.github/workflows/youtube-downloader-ci.yml`

```yaml
- pip install yt-dlp curl_cffi
- python test.py
- ruff check .
- mypy *.py
```

---

## License

Individual scripts may have different licenses. Default: MIT for new scripts.
yt-dlp: Unlicense | curl_cffi: MIT | FFmpeg: GPL/LGPL

---

_Generated by Hermes Agent Technology Stack Blueprint Generator_
