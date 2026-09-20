# Shared yt_opts defaults — same logic as original main_*.py files
# Design tokens (design.md) cover file naming, subtitle labels, container format

DEFAULT_YT_OPTS = {
    "verbose": True,
    "format": "136+ba,298+ba,232+ba,bv+ba",
    "merge_output_format": "mkv",
    "writeautomaticsub": True,
    "subtitlesformat": "srt",
    "subtitleslangs": ["en"],
    "writesubtitles": True,
    "writethumbnail": True,
    "noplaylist": True,
    "skip_download": False,
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mkv",
        },
    ],
    "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",
}

# Design token references (not duplicated — see design.md):
# - File naming: downloads/<uploader>/<title>.<ext>
# - Playlist index: downloads/<playlist_title>/<index>-<title>.<ext>
# - Subtitle label: srt
# - Container: mkv
