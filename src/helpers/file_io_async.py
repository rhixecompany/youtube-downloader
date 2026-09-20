"""File I/O helpers — async and sync pairs.
Example: result = await read_file("downloads/test.mkv")
Example sync: result = read_file_sync("downloads/test.mkv")
"""
import asyncio


async def read_file(path: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, read_file_sync, path)


def read_file_sync(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


async def write_file(path: str, content: str) -> bool:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, write_file_sync, path, content)


def write_file_sync(path: str, content: str) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False
