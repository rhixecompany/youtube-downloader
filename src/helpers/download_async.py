"""
Download helpers — async and sync pairs.
As a patient teacher: each pair has the same behavior.
Call the async version in async contexts; call sync version anywhere.
"""
import asyncio
from typing import Any

from yt_dlp import YoutubeDL  # type: ignore[import-untyped]


class DownloadResult:
    """Result from a successful download — includes saved file paths."""
    def __init__(self, video_path: str, subtitle_path: str | None = None, thumbnail_path: str | None = None):
        self.video_path = video_path
        self.subtitle_path = subtitle_path
        self.thumbnail_path = thumbnail_path

    def __repr__(self) -> str:
        return f"DownloadResult(video_path={self.video_path!r}, subtitle_path={self.subtitle_path!r}, thumbnail_path={self.thumbnail_path!r})"


async def download_url(url: str, opts: dict[str, Any] | None = None) -> DownloadResult:
    """
    Async download of a YouTube URL.
    Example:
        result = await download_url("https://youtube.com/watch?v=xxx")
        print(result.video_path)  # path to downloaded video
    """
    # Run blocking download in a thread pool to keep async behavior
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _download_sync, url, opts)
    return result


def download_url_sync(url: str, opts: dict[str, Any] | None = None) -> DownloadResult:
    """
    Sync download of a YouTube URL.
    Example:
        result = download_url_sync("https://youtube.com/watch?v=xxx")
    """
    return _download_sync(url, opts)


def _download_sync(url: str, opts: dict[str, Any] | None = None) -> DownloadResult:
    """Internal blocking download — shared by async and sync versions."""
    from src.config.yt_opts_defaults import DEFAULT_YT_OPTS
    merged_opts = DEFAULT_YT_OPTS.copy()
    if opts is not None:
        merged_opts.update(opts)
    with YoutubeDL(merged_opts) as ydl:  # type: ignore[arg-type]
        info = ydl.extract_info(url, download=True)
        # Determine output paths from info and outtmpl
        video_path = info.get("_filename") or info.get("filepath", "unknown.mkv")
        subtitle_path = None
        thumbnail_path = None
        # Note: actual subtitle/thumbnail paths depend on yt-dlp output naming
        # This is the minimal version — preserves original behavior
        return DownloadResult(
            video_path=str(video_path),
            subtitle_path=str(subtitle_path) if subtitle_path else None,
            thumbnail_path=str(thumbnail_path) if thumbnail_path else None,
        )
