"""Single video download — rewritten with src/ helpers.
Interactive by default; non-interactive when URL passed as argument.
As a patient teacher: this preserves the same download behavior (same yt_opts format,
subtitle settings, thumbnail, MKV output) but uses the new async/sync helper pairs.
"""
import logging
import sys

from src.config.yt_opts_defaults import DEFAULT_YT_OPTS
from src.helpers.cli_input_async import ask_url_sync
from src.helpers.download_async import download_url_sync

logger = logging.getLogger(__name__)


def main(input_url: str | None = None) -> None:
    """
    Main entry point for single video download.
    Interactive by default (asks for URL); non-interactive when input_url provided or --non-interactive flag used.
    Example interactive: ./myvenv/Scripts/python main_noplaylist.py
    Example non-interactive: ./myvenv/Scripts/python main_noplaylist.py "https://youtube.com/watch?v=xxx"
    """
    # Check for non-interactive flag
    is_interactive = "--non-interactive" not in sys.argv

    url = input_url
    if url is None:
        if is_interactive:
            url = ask_url_sync("Enter video URL: ")
        else:
            # Non-interactive fallback: read from command line
            args = [a for a in sys.argv[1:] if not a.startswith("--")]
            url = args[0] if args else ""

    if not url:
        print("No URL provided. Use --interactive (default) to enter interactively, or pass URL as argument.")
        logger.error("No URL provided for single video download.")
        return

    msg = f"Starting {url}"
    logger.info(msg)
    print(msg)

    # Use shared design token settings from config
    opts = DEFAULT_YT_OPTS.copy()
    opts["noplaylist"] = True

    result = download_url_sync(url, opts)
    msg1 = f"Done Downloading {url}"
    logger.info(msg1)
    print(msg1)
    print(f"Video saved at: {result.video_path}")
    if result.subtitle_path:
        print(f"Subtitle saved at: {result.subtitle_path}")
    if result.thumbnail_path:
        print(f"Thumbnail saved at: {result.thumbnail_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Detect interactive mode: interactive by default unless --non-interactive is passed
    # If first argument is a URL (doesn't start with --), treat as non-interactive
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    interactive_flag = "--interactive" in sys.argv
    non_interactive_flag = "--non-interactive" in sys.argv

    if args:
        # Non-interactive: URL passed as argument
        main(input_url=args[0])
    elif interactive_flag or not non_interactive_flag:
        # Interactive by default (as user selected)
        main()
    else:
        # Explicit non-interactive with no URL
        main()
