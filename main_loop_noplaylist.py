"""Loop mode single video — rewritten with src/ helpers.
As a patient teacher: loops over a list of URLs (hardcoded or from args), uses download_url_sync().
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
            urls_text = ask_url_list_sync("Enter URLs (comma-separated) for loop download: ")
            urls = [urls_text] if isinstance(urls_text, str) else urls_text
        else:
            args = [a for a in sys.argv[1:] if not a.startswith("--")]
            urls = args if args else []
        # For loop mode, process all URLs in the list
        for single_url in urls if isinstance(urls, list) else [urls]:
            if not single_url:
                continue
            msg = f"Starting loop download for {single_url}"
            logger.info(msg)
            print(msg)
            opts = DEFAULT_YT_OPTS.copy()
            opts["noplaylist"] = True
            result = download_url_sync(str(single_url), opts)
            print(f"Loop download complete for {single_url}: {result.video_path}")
    else:
        # Single URL loop mode
        msg = f"Starting loop download for {url}"
        logger.info(msg)
        print(msg)
        opts = DEFAULT_YT_OPTS.copy()
        opts["noplaylist"] = True
        result = download_url_sync(url, opts)
        print(f"Loop download complete: {result.video_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    interactive_flag = "--interactive" in sys.argv
    non_interactive_flag = "--non-interactive" in sys.argv
    if args:
        # Loop over provided URLs (each argument is a URL)
        for arg in args:
            main(input_url=arg)
    elif interactive_flag or not non_interactive_flag:
        main()
    else:
        main()
