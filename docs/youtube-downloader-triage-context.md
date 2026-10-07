# youtube-downloader Triage Context

**Date:** 2026-05-20
**Priority:** MEDIUM
**Stack:** Python, yt-dlp / pytube (YouTube download library)
**Branch:** main
**Repo path:** `Rhixe-company/youtube-downloader`

## Summary

Python-based YouTube video/playlist downloader. Provides separate entry points for
single videos (`main_noplaylist.py`) and playlists (`main_playlist.py`), plus loop
variants for both. Has CONTRIBUTING, CODE_OF_CONDUCT, and `docs/SETUP.md`.

## Issues Found & Fixed

| #   | Issue                                                                               | Action                                                                           | Commit    |
| --- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------- |
| 1   | `.vscode/extensions.json` and `.vscode/settings.json` tracked and deleted from disk | Staged removals; `.gitignore` already has `.vscode/*` rule to prevent recurrence | `432305c` |

## Final State

- **Working tree:** Clean
- **Last commit:** `432305c` — chore: remove stale .vscode editor config files
- **Docs:** `docs/SETUP.md`, CONTRIBUTING.md, CODE_OF_CONDUCT.md
- **CI/CD:** `.github/` directory present

## Recommendations

- Pin dependency versions in `requirements/` directory
- Add a GitHub Actions workflow to lint Python files on push
- Verify yt-dlp version is current (YouTube API changes break older versions frequently)
