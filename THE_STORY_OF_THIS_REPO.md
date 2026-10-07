# The Story of youtube-downloader

_The CLI that downloaded 10,000 videos so you didn't have to_

---

## Prologue: The Playlist Problem

You find a channel. 500 videos. You want them all. Locally. Organized.

Browser extensions: 50 at a time. Manual. Crash-prone.

`yt-dlp` exists. But the flags are a dissertation.

**Solution:** A wrapper. Sensible defaults. Loop modes. Done.

---

## Chapter 1: The Core

```python
# main_noplaylist.py — 47 lines
import yt_dlp

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
```

That's it. The rest is UX.

---

## Chapter 2: The Four Modes

| Script                    | Use Case                           |
| ------------------------- | ---------------------------------- |
| `main_noplaylist.py`      | One video, best quality            |
| `main_playlist.py`        | Entire channel/playlist            |
| `main_loop_noplaylist.py` | URLs from `urls.txt`               |
| `main_loop_playlist.py`   | Playlist URLs from `playlists.txt` |

**Loop mode** reads a file, downloads sequentially, logs progress, resumes on failure.

```python
# main_loop_playlist.py
with open('playlists.txt') as f:
    for line in f:
        url = line.strip()
        if url:
            download_playlist(url)  # with retry + logging
```

---

## Chapter 3: The curl_cffi Addition

Some sites block `yt-dlp`'s default HTTP client.

```python
# Added in 2024
import curl_cffi.requests

ydl_opts['http_client'] = curl_cffi.requests.Session()
```

Now works on: TikTok, Instagram Reels, Twitter/X videos, region-locked content.

---

## Chapter 4: The FFmpeg Dependency

```bash
# macOS
brew install ffmpeg

# Windows
winget install ffmpeg

# Linux
apt install ffmpeg
```

Without it: "Requested format not available" on merge. With it: seamless `mp4` output.

---

## Chapter 5: Zero Config, Zero Config Files

No `config.yaml`. No `.env`. No database.

```bash
# Just run it
python main_playlist.py "https://youtube.com/playlist?list=PL..."
```

Arguments via `sys.argv`. Output to `./downloads/`. Logs to stdout.

---

## Chapter 6: The Test That Isn't

```python
# test.py
import subprocess

result = subprocess.run([
    'python', 'main_noplaylist.py',
    'https://youtube.com/watch?v=jNQXAC9IVRw'
], capture_output=True, text=True)

assert result.returncode == 0
assert 'Downloaded' in result.stdout
```

Runs in CI. Downloads one video (first 10 seconds via `--playlist-items 1`). Verifies the pipeline works.

---

## Epilogue: The Tool That Stays Simple

No database. No server. No auth. No updates since 2024 except `pip install -U yt-dlp`.

It does one thing: **downloads videos**. It does it well.

The best tool is the one you forget exists — until you need it, and it works.

---

_Written by the workspace chronicler, July 25, 2025.  
Filed at `projects/youtube-downloader/THE_STORY_OF_THIS_REPO.md`._
