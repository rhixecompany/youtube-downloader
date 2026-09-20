"""Loop mode playlist — rewritten with src/ helpers.
As a patient teacher: loops through URLs (hardcoded list or args), uses same playlist naming.
"""
import logging
import sys

from src.config.yt_opts_defaults import DEFAULT_YT_OPTS
from src.helpers.cli_input_async import ask_url_list_sync
from src.helpers.download_async import download_url_sync

logger = logging.getLogger(__name__)

def main(input_url: str | None = None) -> None:
    is_interactive = "--non-interactive" not in sys.argv
    url = input_url
    if url is None:
        if is_interactive:
            urls_text = ask_url_list_sync("Enter playlist URLs (comma-separated): ")
            urls = [urls_text] if isinstance(urls_text, str) else urls_text
        else:
            args = [a for a in sys.argv[1:] if not a.startswith("--")]
            urls = args if args else []
        for single_url in urls if isinstance(urls, list) else [str(urls)]:
            if not single_url:
                continue
            msg = f"Starting loop playlist {single_url}"
            logger.info(msg)
            print(msg)
            opts = DEFAULT_YT_OPTS.copy()
            opts["noplaylist"] = False
            opts["outtmpl"] = "downloads/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"
            result = download_url_sync(str(single_url), opts)
            print(f"Loop playlist complete for {single_url}: {result.video_path}")
    else:
        msg = f"Starting loop playlist {url}"
        logger.info(msg)
        print(msg)
        opts = DEFAULT_YT_OPTS.copy()
        opts["noplaylist"] = False
        opts["outtmpl"] = "downloads/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"
        result = download_url_sync(url, opts)
        print(f"Loop playlist complete: {result.video_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    interactive_flag = "--interactive" in sys.argv
    non_interactive_flag = "--non-interactive" in sys.argv
    if args:
        for arg in args:
            main(input_url=arg)
    elif interactive_flag or not non_interactive_flag:
        main()
    else:
        main()
