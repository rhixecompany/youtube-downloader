"""CLI input helpers — interactive by default; non-interactive via flags.
As a patient teacher: ask_url prompts the user; ask_url_sync does the same synchronously.
Pass --interactive flag for interactive mode; default is interactive when stdin is a terminal.
"""
import sys


def ask_url_sync(prompt: str = "Enter URL: ") -> str:
    """
    Sync interactive URL prompt.
    Example: url = ask_url_sync("Enter video URL: ")
    """
    if not sys.stdin.isatty():
        # Non-interactive fallback: read from first command-line argument
        if len(sys.argv) > 1:
            return sys.argv[1]
        return ""
    try:
        user_input = input(prompt)
        return user_input.strip()
    except EOFError:
        return ""


async def ask_url(prompt: str = "Enter URL: ") -> str:
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ask_url_sync, prompt)


def ask_url_list_sync(prompt: str = "Enter URLs (comma-separated): ") -> list[str]:
    """
    Sync interactive URL list prompt.
    Example: urls = ask_url_list_sync("Paste URLs: ")
    Returns list of stripped URLs.
    """
    url_str = ask_url_sync(prompt)
    if not url_str:
        # Try to get from second argument if provided
        return [sys.argv[1]] if len(sys.argv) > 1 else []
    return [u.strip() for u in url_str.split(",") if u.strip()]


async def ask_url_list(prompt: str = "Enter URLs (comma-separated): ") -> list[str]:
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ask_url_list_sync, prompt)
