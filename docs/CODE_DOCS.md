# YouTube Downloader — Code Documentation

## Overview

A Python CLI tool for downloading YouTube videos and playlists using yt-dlp. Provides two standalone scripts optimized for different use cases: single video downloads and full playlist downloads. Both scripts merge streams to MKV format with subtitle support and metadata embedding.

**Stack:** Python 3.8+ | yt-dlp | ffmpeg (external dependency for merging)  
**Files:** `main_noplaylist.py`, `main_playlist.py`, `main_loop_noplaylist.py`, `main_loop_playlist.py`

---

## 1. Single Video Download Script

**File:** `main_noplaylist.py`

### Core Function

```python
import yt_dlp

def download_single_video(url: str, output_path: str = "downloads") -> dict:
    """Download a single YouTube video with optimal quality.

    Downloads the best available video+audio stream, merges to MKV,
    embeds subtitles and thumbnail metadata.

    Args:
        url: YouTube video URL to download.
        output_path: Directory to save the downloaded file
            (default: "downloads" in current directory).

    Returns:
        dict containing download results with keys:
            - filename: Path to the output file.
            - filesize: Approximate file size in bytes.
            - duration: Video duration in seconds.
            - format: Selected format code used.

    Raises:
        yt_dlp.utils.DownloadError: If the URL is invalid or download fails.
        yt_dlp.utils.ExtractorError: If extractor fails to parse the page.
    """
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mkv',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'embedsubs': True,
        'embedthumbnail': True,
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                'key': 'EmbedThumbnail',
            },
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return {
            'filename': ydl.prepare_filename(info),
            'filesize': info.get('filesize') or info.get('filesize_approx'),
            'duration': info.get('duration'),
            'format': info.get('format_id'),
        }
```

### CLI Entry Point

```python
def main():
    """Parse command-line arguments and initiate download.

    Usage:
        python main_noplaylist.py <URL> [--output OUTPUT_DIR]

    Arguments:
        URL: YouTube video URL (required positional).
        --output, -o: Output directory (default: "downloads").

    Example:
        python main_noplaylist.py "https://youtube.com/watch?v=..."
        python main_noplaylist.py "https://youtu.be/..." --output ./videos
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Download a single YouTube video in MKV format"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="Output directory (default: downloads)"
    )
    args = parser.parse_args()

    result = download_single_video(args.url, args.output)
    print(f"Downloaded: {result['filename']}")
```

### yt-dlp Options Reference

| Option                | Value                                                    | Purpose                               |
| --------------------- | -------------------------------------------------------- | ------------------------------------- |
| `format`              | `'bestvideo[height<=1080]+bestaudio/best[height<=1080]'` | Best 1080p video + best audio, merged |
| `merge_output_format` | `'mkv'`                                                  | Container format for merged streams   |
| `outtmpl`             | `'{output}/%(title)s.%(ext)s'`                           | Output filename template              |
| `writesubtitles`      | `True`                                                   | Download available subtitles          |
| `writeautomaticsub`   | `True`                                                   | Download auto-generated captions      |
| `subtitleslangs`      | `['en']`                                                 | English subtitles only                |
| `embedsubs`           | `True`                                                   | Embed subtitles in output file        |
| `embedthumbnail`      | `True`                                                   | Embed thumbnail as cover art          |
| `writethumbnail`      | `True`                                                   | Write thumbnail as separate file      |
| `postprocessors`      | `[FFmpegMetadata, EmbedThumbnail]`                       | Embed metadata and thumbnail          |

---

## 2. Playlist Download Script

**File:** `main_playlist.py`

### Core Function

```python
import yt_dlp

def download_playlist(url: str, output_path: str = "downloads") -> list[dict]:
    """Download all videos from a YouTube playlist.

    Downloads each video with the highest available quality using format selection
    optimized for 1080p. Videos are merged to MKV with subtitles and metadata.

    The format string '136+ba,298+ba,232+ba,bv+ba' selects formats in order:
        136:  mp4 1280x720   (H.264)
        298:  mp4 1280x720   (H.264, DASH)
        232:  mp4 1280x720   (H.264, DASH)
        bv+ba: Fallback to best video + best audio

    Args:
        url: YouTube playlist URL to download.
        output_path: Directory to save downloaded files
            (default: "downloads" in current directory).

    Returns:
        list of dict, each containing download results for a video:
            - filename: Path to the output file.
            - title: Video title.
            - duration: Video duration in seconds.
            - index: Position in the playlist.

    Raises:
        yt_dlp.utils.DownloadError: If the URL is invalid.
        yt_dlp.utils.ExtractorError: If extraction fails.
    """
    ydl_opts = {
        'format': '136+ba,298+ba,232+ba,bv+ba',
        'merge_output_format': 'mkv',
        'outtmpl': f'{output_path}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'embedsubs': True,
        'embedthumbnail': True,
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegMetadata', 'add_metadata': True},
            {'key': 'EmbedThumbnail'},
        ],
    }

    results = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if 'entries' in info:
            for entry in info['entries']:
                results.append({
                    'filename': ydl.prepare_filename(entry),
                    'title': entry.get('title'),
                    'duration': entry.get('duration'),
                    'index': entry.get('playlist_index'),
                })

    return results
```

### CLI Entry Point

```python
def main():
    """Parse command-line arguments and initiate playlist download.

    Usage:
        python main_playlist.py <URL> [--output OUTPUT_DIR] [--limit N]

    Arguments:
        URL: YouTube playlist URL (required positional).
        --output, -o: Output directory (default: "downloads").
        --limit, -l: Maximum number of videos to download (optional).

    Example:
        python main_playlist.py "https://youtube.com/playlist?list=..."
        python main_playlist.py "https://youtube.com/playlist?list=..." --limit 5
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Download all videos from a YouTube playlist in MKV format"
    )
    parser.add_argument("url", help="YouTube playlist URL")
    parser.add_argument("-o", "--output", default="downloads",
                        help="Output directory (default: downloads)")
    parser.add_argument("-l", "--limit", type=int,
                        help="Maximum number of videos to download")
    args = parser.parse_args()

    results = download_playlist(args.url, args.output)
    print(f"Downloaded {len(results)} videos from playlist")
```

### Format Selection Strategy

The playlist script uses a specific format priority:

```
'136+ba,298+ba,232+ba,bv+ba'
```

| Format Code | Resolution      | Codec        | Container |
| ----------- | --------------- | ------------ | --------- |
| `136`       | 1280x720 (720p) | H.264        | mp4       |
| `298`       | 1280x720 (720p) | H.264 (DASH) | mp4       |
| `232`       | 1280x720 (720p) | H.264 (DASH) | mp4       |
| `bv+ba`     | Best available  | Any          | Any       |

**Note:** `+ba` appends the best audio stream to the selected video. yt-dlp will try each format in order until one succeeds.

---

## 3. Loop Variants

### main_loop_noplaylist.py

```python
def download_videos_from_file(urls_file: str, output_path: str = "downloads") -> list[dict]:
    """Download multiple videos from a file containing URLs.

    Reads URLs line-by-line from a text file and downloads each video.
    Skips empty lines and comments (lines starting with #).

    Args:
        urls_file: Path to text file containing YouTube URLs (one per line).
        output_path: Directory to save downloaded files.

    Returns:
        list of dict, download results for each video.
    """
```

### main_loop_playlist.py

```python
def download_playlists_from_file(urls_file: str, output_path: str = "downloads") -> list[list[dict]]:
    """Download multiple playlists from a file containing playlist URLs.

    Reads URLs line-by-line and processes each playlist sequentially.
    Each playlist's videos are saved in a subdirectory named after the playlist.

    Args:
        urls_file: Path to text file containing playlist URLs.
        output_path: Base directory for all downloads.

    Returns:
        list of lists, each containing download results for one playlist.
    """
```

---

## 4. Common Utilities (Shared Pattern)

### Output Directory Structure

```
downloads/
├── (single_video_title).mkv         # From main_noplaylist.py
├── (single_video_title).mkv
└── (Playlist Name)/
    ├── 01 - (Video Title).mkv       # From main_playlist.py
    ├── 02 - (Video Title).mkv
    └── ...
```

### Error Handling Pattern

All scripts use minimal error handling:

- `yt_dlp` exceptions propagate to the caller
- No retry logic for failed downloads
- No logging beyond stdout print statements
- Network errors result in script termination

---

## 5. Dependencies

### Required

| Package  | Version | Purpose                                             |
| -------- | ------- | --------------------------------------------------- |
| `yt-dlp` | Latest  | YouTube downloading and extraction                  |
| `ffmpeg` | System  | Stream merging, metadata embedding, subtitle muxing |

### Installation

```bash
# Python package
pip install yt-dlp

# System: ffmpeg
# Windows: choco install ffmpeg  or  winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

---

## 6. File Comparison

| Feature | main_noplaylist.py    | main_playlist.py       | main_loop_noplaylist.py | main_loop_playlist.py |
| ------- | --------------------- | ---------------------- | ----------------------- | --------------------- |
| Input   | Single URL            | Playlist URL           | URLs file               | Playlist URLs file    |
| Output  | Single file           | Directory per playlist | Multiple files          | Multiple directories  |
| Format  | `bestvideo+bestaudio` | `136+ba,298+ba,...`    | Same as single          | Same as playlist      |
| Subdirs | No                    | Yes (per playlist)     | No                      | Yes (per playlist)    |
| Limit   | N/A                   | Optional --limit       | N/A                     | Optional --limit      |
