# Spec — YouTube CLI Architecture (Rebuild)

Created: 2026-09-20 | Spec ref: youtube-downloader-rebuild-2026-09-20
Repo: `youtube-downloader` | Profile: default | Tier: GA

## What this builds

This rebuild introduces a `src/` directory with async and synchronous helper pairs, rewrites the 4 existing `main_*.py` entry points to use those helpers, adds interactive/non-interactive CLI modes, and creates `.sh`/`.ps1`/`.bat` wrapper scripts at the repo root.

The design tokens (`design.md`) cover CLI formatting: log colors (info, error, verbose), file naming patterns (`downloads/%(uploader)s/%(title)s.%(ext)s`), subtitle format labels (`srt`), and spacing rules for multi-line output.

## Source layout (after rebuild)

```
.
├── .sh / .ps1 / .bat          # Cross-platform wrapper scripts (interactive by default)
├── myvenv/                     # New uv venv (created via uv venv myvenv)
├── src/
│   ├── helpers/
│   │   ├── download_async.py   # async download_url(url) + sync download_url_sync(url)
│   │   ├── file_io_async.py    # async file I/O pair (read / write)
│   │   └── cli_input_async.py  # async ask_url() + sync ask_url_sync()
│   └── config/
│       └── yt_opts_defaults.py # Shared yt_opts defaults (same format/subtitle logic as original)
├── main_noplaylist.py          # Rewritten: uses src/ helpers, interactive/non-interactive
├── main_playlist.py            # Rewritten: same
├── main_loop_noplaylist.py     # Rewritten: same
├── main_loop_playlist.py       # Rewritten: same
├── docs/
│   ├── scope/scope.md          # Scope (Tracer Bullet, GA, 8 features)
│   └── specs/                  # This file (architecture spec)
└── scripts/                    # Scripts directory (existing or new helper scripts)
```

## Helper pairs (all three pairs required)

Every public function has both an `async` and `sync` version. The sync version calls the async version with `asyncio.run()` internally, or delegates to a blocking wrapper. This allows users to call either style without duplicating the download/file logic.

### Pair 1: download_url

- `async download_url(url: str) -> DownloadResult`
- `sync download_url_sync(url: str) -> DownloadResult`

Both use the same `yt_opts` defaults (video format `136+ba,298+ba,232+ba,bv+ba`, merge `mkv`, subtitles `en` in `srt` format, thumbnail enabled, `outtmpl` following design token patterns). The result includes the saved file path and subtitle file paths.

### Pair 2: file I/O

- `async read_file(path: str) -> str`
- `sync read_file_sync(path: str) -> str`
- `async write_file(path: str, content: str) -> bool`
- `sync write_file_sync(path: str, content: str) -> bool`

Used by the entry points for any extra file creation (e.g., URL list storage, result logging).

### Pair 3: CLI input

- `async ask_url(prompt: str = "Enter URL: ") -> str`
- `sync ask_url_sync(prompt: str = "Enter URL: ") -> str`
- `async ask_url_list(prompt: str = "Enter URLs (comma-separated): ") -> list[str]`
- `sync ask_url_list_sync(prompt: str = "Enter URLs (comma-separated): ") -> list[str]`

Interactive by default (prints prompt, waits for input). Non-interactive mode skips the prompt and reads from command-line argument (`sys.argv` or passed list).

## Entry point behavior

All 4 `main_*.py` files are rewritten to:

1. Import from `src.helpers` (download, file I/O, CLI input) and `src.config` (default `yt_opts`).
2. Call `ask_url()` (interactive) or read from `sys.argv` (non-interactive when `--interactive` is not set, or when no stdin is available).
3. Call `download_url()` or `download_url_sync()` based on whether the entry point itself uses `async def main()` or `def main()`.
4. Log results using the design token formatting (verbose mode enabled by default, consistent with original `yt_opts`).

The `.sh` / `.ps1` / `.bat` scripts at root call `python main_*.py` with the URL(s) passed as arguments. If no arguments are given and `--interactive` is used (or by default when interactive mode is active), the script asks the user. The non-interactive default is triggered when arguments are provided or when `--interactive` is not used.

## Design token integration (`design.md`)

The `yt_opts` `outtmpl` and subtitle labels reference the design token patterns:

- File path: `downloads/%(uploader)s/%(title)s.%(ext)s` (matches `downloads/` root with uploader folder)
- Playlist index: `downloads/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s`
- Subtitle label: `srt`
- Container: `mkv`

The `design.md` file (to be created separately by `/design-md`) defines these tokens formally (colors for log levels, spacing for multi-line output, naming conventions). This spec references `design.md` but does not duplicate its content.

## Verification checklist

- [x] Scope exists (`docs/scope/scope.md`, 5768 B) — verified
- [x] Plan exists (`$HERMES_HOME/plans/youtube-downloader-rebuild-2026-09-20/PLAN.md`) — verified
- [x] Design tokens referenced (`/design-md` reference preserved) — verified
- [x] Source layout documented (this file) — verified
- [x] Async/sync pairs defined (3 pairs) — verified
- [x] `.env` protected: workspace `.env` (5274 B) and hermes `.env` (30501 B) unchanged — verified
- [ ] Implementation: `myvenv` created, `local.txt` installed
- [ ] Implementation: `src/` created with `helpers/` and `config/`
- [ ] Implementation: `main_*.py` rewritten
- [ ] Implementation: `.sh` + `.ps1` + `.bat` created
- [ ] Verification: `ruff check .` passes; `pyright .` passes; `pylint .` passes (or warnings preserved honestly)
- [ ] Verification: interactive/non-interactive modes verified by dry-run
- [ ] Integrity: 0 synthetic artifacts; all file sizes real; `.env` unchanged; 0 new `.bak`
