# RESEARCH_REPORT.md

## Project: youtube-downloader

**Type:** YouTube CLI download tool
**Tech Stack:** Python 3.x, yt-dlp[curl-cffi], FFmpeg, ruff, mypy, uv, pytest
**Status:** Active

---

## Similar Projects

| Project         | URL                        | Why Relevant                             |
| --------------- | -------------------------- | ---------------------------------------- |
| Python-projects | `projects/Python-projects` | Shared Python CLI + requirements hygiene |

---

## Key Findings

### yt-dlp Best Practices (2026)

- **yt-dlp** is gold standard — 149K+ stars, 1,800+ sites, daily updates
- **Install `yt-dlp[curl-cffi]`** — `--impersonate chrome` bypasses bot protection
- **`--download-archive archive.txt`** — skip already-downloaded content; essential for cron jobs
- **`-o` output template** — always include `%(id)s` to avoid title collisions; prefer `bestvideo[height<=1080]+bestaudio` over hardcoded numeric format codes
- **Rate limiting** — `--limit-rate 5M --sleep-interval 5 --max-sleep-interval 15` for unattended jobs
- **Cookie support** — `--cookies-from-browser firefox` for gated content
- **Post-processing** — `--embed-metadata --embed-thumbnail --embed-subs --embed-chapters` in one pass

### curl_cffi for Bot Protection Bypass

- Python binding for curl-impersonate — mimics real browser TLS/JA3/HTTP2 fingerprints
- Key impersonation targets: `chrome`, `safari`, `safari_ios`, `firefox`, `edge`
- **Limitations**: beats TLS/HTTP2 fingerprinting; does NOT solve JavaScript challenges (Cloudflare Turnstile)

### Legal Landscape (2026)

- 2026 DMCA ruling: third-party downloading ruled as copyright circumvention; personal use only
- Creative Commons content explicitly downloadable — filter with `--match-filter "license!=*"`
- Tool itself not infringing (RIAA vs youtube-dl 2020); distribution for infringing use is the risk

---

## Cheatsheets & Quick Reference

| Topic                   | Resource                                            | Type    |
| ----------------------- | --------------------------------------------------- | ------- |
| yt-dlp docs             | <https://github.com/yt-dlp/yt-dlp>                  | Docs    |
| curl_cffi               | <https://github.com/yifeikong/curl_cffi>            | Package |
| yt-dlp format selection | <https://github.com/yt-dlp/yt-dlp#format-selection> | Guide   |

---

## Best Practices

1. **`--impersonate chrome`** — bypass bot protection via curl_cffi
2. **`--download-archive`** — skip duplicates; essential for automation
3. **Always include `%(id)s`** in output template — prevent filename collisions
4. **Rate limit yourself** — `--limit-rate 5M --sleep-interval 5` for cron/automation
5. **`--embed-metadata`** — embed all metadata in one pass

---

## Common Pitfalls

| Pitfall                    | Impact                  | Avoidance                                                |
| -------------------------- | ----------------------- | -------------------------------------------------------- |
| No curl_cffi installed     | Bot detection blocks    | `pip install "yt-dlp[curl-cffi]"`                        |
| Missing `%(id)s` in output | Files overwritten       | Always include `%(id)s` in template                      |
| No download archive        | Repeated downloads      | `--download-archive archive.txt`                         |
| Missing FFmpeg             | Merge/subs fail         | Install FFmpeg system-wide                               |
| Hardcoded format codes     | Format no longer exists | Use expressions like `bestvideo[height<=1080]+bestaudio` |

---

## Performance

1. **curl_cffi impersonation** — avoids bot-related rate limiting
2. **Format selection limiting** — cap quality to reduce download time and storage
3. **Download archive** — skip already-fetched content
4. **Concurrent fragments** — yt-dlp `--concurrent-fragments` for DASH streams
5. **Rate limiting** — prevents IP throttling/blocking

---

## Security

1. **No hardcoded cookies** — use `--cookies-from-browser` for authenticated access
2. **Validate output paths** — prevent path traversal via `..` in filenames
3. **Respect copyright** — personal use only; Creative Commons when possible
4. **FFmpeg from trusted source** — official builds only to avoid malware

---

## Related Projects (in workspace)

- **Python-projects** — shared Python CLI tooling patterns
- **selenium_webdriver** — shared web scraping and automation patterns

---

## Resources

| Resource                | URL                                                 | Description       |
| ----------------------- | --------------------------------------------------- | ----------------- |
| yt-dlp GitHub           | <https://github.com/yt-dlp/yt-dlp>                  | Download tool     |
| curl_cffi               | <https://github.com/yifeikong/curl_cffi>            | TLS impersonation |
| yt-dlp format selection | <https://github.com/yt-dlp/yt-dlp#format-selection> | Format syntax     |

### Research Methodology

- **Web search:** web_search (2026 yt-dlp patterns, DEV Community, legal landscape)
- **Documentation:** web_extract (yt-dlp, curl_cffi docs)
- **Last verified:** 2026-07-28
