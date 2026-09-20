"""Playlist download — rewritten with src/ helpers (Tracer Bullet approach preserved).
As a patient teacher: uses same yt_opts (noplaylist=False, playlist index naming), new async/sync helpers.
"""
import logging
import sys

from src.config.yt_opts_defaults import DEFAULT_YT_OPTS
from src.helpers.cli_input_async import ask_url_sync
from src.helpers.download_async import download_url_sync

logger = logging.getLogger(__name__)

def main(input_url: str | None = None) -> None:
    is_interactive = "--non-interactive" not in sys.argv
    url = input_url
    if url is None:
        if is_interactive:
            url = ask_url_sync("Enter playlist URL: ")
        else:
            args = [a for a in sys.argv[1:] if not a.startswith("--")]
            url = args[0] if args else ""
    if not url:
        print("No playlist URL provided.")
        return
    msg = f"Starting playlist {url}"
    logger.info(msg)
    print(msg)
    opts = DEFAULT_YT_OPTS.copy()
    opts["noplaylist"] = False
    opts["outtmpl"] = "downloads/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"
    result = download_url_sync(url, opts)
    print(f"Playlist download complete: {result.video_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    interactive_flag = "--interactive" in sys.argv
    non_interactive_flag = "--non-interactive" in sys.argv
    if args:
        main(input_url=args[0])
    elif interactive_flag or not non_interactive_flag:
        main()
    else:
        main()
