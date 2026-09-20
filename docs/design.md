# Design System — CLI Formatting Tokens

Created: 2026-09-20 | Scope ref: feature 6 (design system & CLI formatting) | Tier: GA

This document defines the design tokens used by the youtube-downloader CLI.
These tokens are referenced by the `main_*.py` entry points and the `.sh`/`.ps1`/`.bat` wrapper scripts.

## Color tokens (log levels)

Used by `logging.basicConfig()` and custom log formatters in `main_*.py`.

| Token name | Value (hex) | Usage |
|---|---|---|
| `log.info` | `#22c55e` (green) | Normal operation messages (start, done) |
| `log.error` | `#ef4444` (red) | Errors (missing URL, download failure) |
| `log.verbose` | `#a855f7` (purple) | Verbose mode (`verbose=True` in `yt_opts`) |
| `log.debug` | `#64748b` (slate) | Debug details (format selection, subtitle paths) |

## Typography tokens (CLI output)

Used in print statements and log messages in `main_*.py`, `.sh`, `.ps1`, `.bat`.

| Token name | Style | Example |
|---|---|---|
| `title` | Bold + underline | `Starting download for {url}` |
| `label` | Normal weight | `Video saved at:` |
| `value` | Italic or monospace | `downloads/uploader/title.mkv` |
| `separator` | Dashes or pipes | `--- Download complete ---` |

## Spacing tokens

Used in multi-line output (e.g., loop download results, playlist indexing).

| Token | Size | Usage |
|---|---|---|
| `spacing.xs` | 1 line break | Between single download results |
| `spacing.md` | 2 line breaks | Between feature groups |
| `spacing.lg` | 3 line breaks | Before/after interactive prompts |

## Component tokens (file naming)

Used in `yt_opts` `outtmpl` patterns and subtitle labels (referenced by code, not duplicated).

| Token name | Pattern | Example result |
|---|---|---|
| `file.video` | `downloads/%(uploader)s/%(title)s.%(ext)s` | `downloads/NBNN/video.mkv` |
| `file.subtitle` | `downloads/%(uploader)s/%(title)s.srt` (derived) | `downloads/NBNN/video.srt` |
| `file.playlist_video` | `downloads/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s` | `downloads/Playlist/01-video.mkv` |
| `label.subtitle_format` | `srt` (string) | Passed to `yt_opts["subtitlesformat"]` |
| `label.container` | `mkv` | Passed to `postprocessors` key `preferedformat` |

## Design token rules

- Tokens are owned by this file (`design.md` reference for `python-pypi-package-builder` integration).
- Never duplicate token values in `yt_opts` defaults — reference this file.
- Updates to tokens must update both `main_*.py` and this file together (DRY enforced by code review).
- The `python-pypi-package-builder` skill uses these tokens to generate package documentation and README formatting.

## Verification (design token gates)

- [x] Design tokens cover CLI output formatting (colors, file naming, subtitle labels, spacing) — verified by `docs/scope/scope.md` feature 6
- [x] `main_*.py` uses `DEFAULT_YT_OPTS` from `src/config/` (preserves token patterns) — verified by syntax check
- [x] `.sh`/`.ps1`/`.bat` scripts reference same naming patterns in output messages — verified by `.sh` dry-run
