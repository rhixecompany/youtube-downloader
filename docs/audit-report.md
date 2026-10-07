# YouTube Downloader — Security Audit Report

**Repository:** Rhixe-company/youtube-downloader  
**Audit Date:** 2026-05-21  
**Priority:** LOW  
**Auditor:** Automated Security Scan

---

## Executive Summary

The youtube-downloader repository contains four small Python CLI utility scripts with **no significant security risks**. The scripts have no network-facing services, no authentication systems, no databases, and no user data storage. The primary concerns are operational (lack of error handling, hardcoded paths) rather than security vulnerabilities.

**Risk Score: 1.5/10** — No secrets, no web exposure, simple CLI utility with low-risk issues.

---

## Findings Summary

| ID    | Severity | Finding                                  | Status        |
| ----- | -------- | ---------------------------------------- | ------------- |
| F-001 | 🟢 LOW   | No requirements.txt / dependency pinning | ❌ Unresolved |
| F-002 | 🟢 LOW   | No error handling for download failures  | ❌ Unresolved |
| F-003 | 🟢 LOW   | Hardcoded default output path            | ❌ Unresolved |
| F-004 | 🟢 LOW   | No input validation on URLs              | ❌ Unresolved |
| F-005 | 🟢 LOW   | No automated tests                       | ❌ Unresolved |
| F-006 | 🟢 LOW   | No CI/CD configuration                   | ❌ Unresolved |
| F-007 | ℹ️ INFO  | yt-dlp auto-updates — no version pin     | ❌ Unresolved |
| F-008 | ℹ️ INFO  | No logging — stdout only                 | ❌ Unresolved |

---

## Detailed Findings

### LOW: No requirements.txt / Dependency Pinning

**Category:** Operational  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

The repository has no `requirements.txt` file. Users must manually install `yt-dlp` without version constraints. This can lead to:

- Unexpected behavior after yt-dlp API changes
- Incompatibility with existing yt-dlp installations
- Difficulty reproducing the development environment

**Remediation:**

```bash
# Create requirements.txt
pip freeze | grep yt-dlp > requirements.txt
```

Or create manually:

```
yt-dlp>=2023.0.0,<2025.0.0
```

### LOW: No Error Handling for Download Failures

**Category:** Robustness  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

Download failures from yt-dlp are not caught or handled gracefully:

```python
# Current: unhandled exception terminates the script
info = ydl.extract_info(url, download=True)

# Better: try/except with user-friendly message
try:
    info = ydl.extract_info(url, download=True)
except yt_dlp.utils.DownloadError as e:
    print(f"Download failed: {e}")
    return None
except yt_dlp.utils.ExtractorError as e:
    print(f"Failed to extract video info: {e}")
    return None
```

**Impact:** A single failed download in a playlist batch stops the entire process. Network interruptions, deleted videos, or region blocks all cause unhandled crashes.

**Remediation:**

1. Wrap `extract_info()` calls in try/except blocks
2. Add per-video error handling in playlist/loop scripts to skip failed items
3. Print descriptive error messages instead of raw tracebacks

### LOW: Hardcoded Default Output Path

**Category:** Operational  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

```python
def download_single_video(url: str, output_path: str = "downloads"):
```

The default output path `./downloads/` is relative to the current working directory. This can cause:

- Unexpected file creation if run from an unintended directory
- Permission errors if the working directory is not writable
- Files landing in unexpected locations when run via cron or automation

**Remediation:**

1. Use `os.path.expanduser()` for sensible defaults: `os.path.join(os.path.expanduser('~'), 'Downloads')`
2. Create the output directory if it doesn't exist: `os.makedirs(output_path, exist_ok=True)`
3. Print the absolute output path after successful download

### LOW: No Input Validation on URLs

**Category:** Operational  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

URLs are passed directly to yt-dlp without any validation or sanitization:

```python
# Current: no validation
url = args.url  # Passed directly to yt-dlp
info = ydl.extract_info(url, download=True)
```

While yt-dlp handles invalid URLs gracefully, missing validation means:

- Non-YouTube URLs cause confusing errors upstream
- Malformed URLs produce unhelpful tracebacks
- Empty strings or whitespace are not caught early

**Remediation:**

```python
import re

def validate_youtube_url(url: str) -> bool:
    """Basic validation for YouTube URLs."""
    patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=',
        r'^https?://youtu\.be/',
        r'^https?://(www\.)?youtube\.com/playlist\?list=',
    ]
    return any(re.match(p, url) for p in patterns)

# Usage
if not validate_youtube_url(url):
    print("Error: Invalid YouTube URL")
    sys.exit(1)
```

### LOW: No Automated Tests

**Category:** Quality Assurance  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

The repository has zero test coverage. Risks include:

- Regressions after yt-dlp API changes go undetected
- Format selection changes may silently break
- Edge cases (empty playlists, deleted videos, private videos) are untested

**Remediation:**

```python
# tests/test_downloader.py
import pytest
from unittest.mock import patch
from main_noplaylist import download_single_video

@patch('main_noplaylist.yt_dlp.YoutubeDL')
def test_single_video_download(mock_ydl):
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {
        'title': 'Test Video',
        'duration': 120,
        'filesize': 50000000,
        'format_id': '136+ba',
    }
    mock_instance.prepare_filename.return_value = 'downloads/Test Video.mkv'

    result = download_single_video('https://youtube.com/watch?v=test')
    assert result['filename'] == 'downloads/Test Video.mkv'
    assert result['duration'] == 120
```

### LOW: No CI/CD Configuration

**Category:** Operations  
**Severity:** 🟢 LOW  
**Status:** ❌ Unresolved

No `.github/workflows/` or CI configuration exists. Missing benefits:

- Automated testing on pull requests
- Dependency vulnerability scanning
- Linting and code style enforcement
- Automated release management

### INFO: yt-dlp Auto-Update Behavior

**Category:** Operational  
**Severity:** ℹ️ INFO  
**Status:** ❌ Unresolved

yt-dlp auto-updates by default (`--update`). This means the script's behavior can change without explicit dependency updates. While yt-dlp maintains backward compatibility, major site changes (e.g., YouTube API changes) can temporarily break functionality.

**Remediation:** Pin yt-dlp version in requirements.txt and disable auto-updates with `ydl_opts['update'] = False`.

### INFO: No Logging — stdout Only

**Category:** Operational  
**Severity:** ℹ️ INFO  
**Status:** ❌ Unresolved

All output goes to stdout via `print()`. This means:

- No log rotation for automated/batch downloads
- No persistent record of download history
- Errors cannot be audited retroactively

**Remediation:** Add basic Python `logging`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('downloads.log'),
        logging.StreamHandler()
    ]
)
```

---

## Recommendations

### Short-term (before next release)

1. Add `requirements.txt` with yt-dlp version pinning
2. Add try/except error handling around all `extract_info()` calls
3. Make output directory configurable with sensible default
4. Add basic URL validation before passing to yt-dlp
5. Create output directory if it doesn't exist

### Medium-term (1 month)

1. Add per-video error handling in playlist/loop scripts (skip on failure)
2. Implement basic test suite with mocked yt-dlp
3. Add GitHub Actions CI for linting and testing
4. Replace `print()` with proper `logging` module

### Long-term (3 months)

1. Add download resume support (yt-dlp's `--continue`)
2. Implement parallel download option for playlists
3. Add progress bar output (yt-dlp's `--progress` or `tqdm`)
4. Create a unified CLI entry point with subcommands

---

## Security Considerations

Since these are CLI scripts run on the user's machine:

- **No network exposure** — Only outbound connections to YouTube
- **No credentials** — No API keys, tokens, or passwords stored
- **No user data** — Only downloads publicly available video content
- **No system access** — Writes only to the configured output directory
- **Low risk** — Typical risks involve failed downloads, not security breaches

The most security-relevant action is the inclusion of cookies for restricted content — if `cookies.txt` is used, it should be:

- Kept out of version control (add to `.gitignore`)
- Stored with restricted file permissions (`chmod 600`)
- Deleted when no longer needed

---

## Rapid Remediation Patch

Apply these minimal changes to `main_noplaylist.py` for immediate improvement:

```python
import os
import sys
import yt_dlp

def ensure_output_dir(path: str) -> str:
    """Create output directory if it doesn't exist."""
    abs_path = os.path.abspath(path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path

def download_single_video(url: str, output_path: str = None) -> dict | None:
    if output_path is None:
        output_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'youtube')

    output_path = ensure_output_dir(output_path)

    ydl_opts = { ... }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # ... return result ...
    except yt_dlp.utils.DownloadError as e:
        print(f"ERROR: Download failed for {url}: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return None
```

---

## References

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp Configuration](https://github.com/yt-dlp/yt-dlp#configuration)
- [OWASP Top 10 for CLIs](https://owasp.org/www-community/attacks/Command_Injection)
