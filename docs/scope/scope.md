# Scope: YouTube CLI downloader

A Python CLI that downloads YouTube videos, playlists, and loops, using `yt-dlp`. It serves anyone who wants to save YouTube content locally with subtitles, thumbnails, and custom formats.

**Build approach:** Tracer Bullet (each feature works end to end: code runs through download, verify, test, review, document).
**Workflow:** GA (after `/develop`: `/check verify` → `/test` → `/check review` → `/document`).

_Recommendations, not orders. Skip what doesn't fit. Design tokens live in `/design-md`; the design-md spec covers CLI output formatting (log colors, file naming patterns, subtitle format labels)._

## At a glance

|| # | Feature | Phase | Status |
||---|---------|-------|--------|
|| 1 | Stack & architecture | Foundation | existing |
|| 2 | Single video download | Foundation | existing |
|| 3 | Playlist download | Slice 1 | existing |
|| 4 | Loop mode (repeat download) | Slice 2 | existing |
|| 5 | Subtitles + thumbnail | Cross cut | existing |
|| 6 | Design system & CLI formatting | Foundation | planned |
|| 7 | Output format customization | Slice 1 | planned |
|| 8 | Coding standards & tooling | Foundation | planned |

## Existing features (brownfield enrollment)

### 1. Stack & architecture · existing
Python 3.x CLI using `yt-dlp` and `curl_cffi`. Code lives at root: `main_noplaylist.py`, `main_playlist.py`, `main_loop_noplaylist.py`, `main_loop_playlist.py`. Project manifest: `package.json`, `PLAN.md`, `SPEC.md`.

### 2. Single video download · existing
Download one video with subtitles, thumbnail, and MKV output format. `noplaylist: True`. Code in `main_noplaylist.py`.

### 3. Playlist download · existing
Download an entire playlist with index-based file naming (`playlist_title/index-title`). `noplaylist: False`. Code in `main_playlist.py`.

### 4. Loop mode · existing
Repeat download in a loop. Supports both single (`main_loop_noplaylist.py`) and playlist (`main_loop_playlist.py`) loop variants.

### 5. Subtitles + thumbnail · existing
Write subtitles (`srt` format) and thumbnail for each download. Configured in `yt_opts` across all main scripts (`writesubtitles: True`, `writethumbnail: True`, `subtitleslangs: ["en"]`).

## Planned features (next slice, Tracer Bullet)

### 6. Design system & CLI formatting · planned · needs a decision · GA
Design tokens (`design.md`) covering CLI output formatting: log color patterns (info, error, verbose), file naming conventions (folder structure `downloads/%(uploader)s/` or `downloads/%(playlist_title)s/%(playlist_index)s`), subtitle format labels (`srt` vs others), and spacing/indent rules for multi-line output. This supports the GA tier's `/document` step.

**Done when:** `design.md` covers CLI formatting tokens, and the scope references it in `docs/scope/scope.md`.
- [ ] Design it (spec): `/architect design system & CLI formatting`
- [ ] Build tokens into format modules: `/develop design system & CLI formatting`
- [ ] Verify it: `/check verify design system & CLI formatting`
- [ ] Test it: `/test design system & CLI formatting`
- [ ] Fresh model review: `/check review design system & CLI formatting`
- [ ] Document it: `/document design system & CLI formatting`
Spec: `/design-md` · code in `docs/design.md`

### 7. Output format customization · planned · needs a decision
Expose format customization (video format selection, subtitle language, output container) as configurable CLI options instead of hardcoded `yt_opts`. Builds on the design tokens for consistent naming.

**Done when:** user can specify format, subtitle language, and container from the CLI; output follows `design.md` naming patterns.
- [ ] Design it (spec): `/architect output format customization`
- [ ] Build CLI flags + validation: `/develop output format customization`
  - [ ] Add `--format`, `--subtitles-lang`, `--container` flags
  - [ ] Apply design token naming to output paths
  - [ ] Wire flags into `yt_opts`
- [ ] Verify it: `/check verify output format customization`
- [ ] Test it: `/test output format customization`
- [ ] Fresh model review: `/check review output format customization`
- [ ] Document it: `/document output format customization`
Spec: future spec · code in `main_*.py`

### 8. Coding standards & tooling · planned · needs a decision
Capture conventions from the existing repo (`AGENTS.md`, `.ruff.toml`, `pyrightconfig.json`) and install/enforce lint (`ruff`), type check (`pyright`), and pre-commit (`.pre-commit-config.yaml`). This is the foundation that every feature in this GA-tier scope relies on.

**Done when:** root `AGENTS.md` reflects the real Python CLI stack, and `ruff` + `pyright` + `pre-commit` run clean.
- [ ] Capture conventions + tooling choices: `/audit`
- [ ] Install/update the tooling: `/develop tooling`
  - [ ] Confirm `.ruff.toml` rules match codebase
  - [ ] Confirm `pyrightconfig.json` covers all entrypoints
  - [ ] Confirm `.pre-commit-config.yaml` hooks are active
- [ ] Verify it: `/check verify tool`
- [ ] Test it: `/test tool`
- [ ] Fresh model review: `/check review tool`
- [ ] Document it: `/document tool`
Spec: `/audit` · code in root config files

## Deferred

- **Billing & analytics**: not part of this CLI's scope.
- **Web dashboard**: out of scope; this is a headless CLI.

## Legend

- **Decision box** = the box whose label ends with `(spec)`. Only `/architect` ticks it.
- **Next step** = the first unticked box (always a command or milestone).
- **Status**: `existing` = pre-workflow, complete; `planned` = this scope will build it.
- **GA tier closing stages**: after `/test`: `/check review` (fresh model), then `/document`.
- **Design tokens**: `/design-md` covers CLI formatting (colors, naming, spacing); this scope references it in feature 6.
