import yt_dlp  # type: ignore[import-untyped]
from yt_dlp.utils import download_range_func  # noqa: F401 # type: ignore

save_path = "Django REST Framework"
video_url = input("Enter your URL: ")
url = "https://youtube.com/playlist?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t&si=gF6wqVQf4vtWZ5d0"


def main(video_url, save_path=save_path):
    # start_time = 2  # accepts decimal value like 2.3
    # end_time = 7

    yt_opts = {
        # "verbose": True,
        # "download_ranges": download_range_func(None, [(start_time, end_time)]),
        # "force_keyframes_at_cuts": True,
        # "format": "bestvideo+bestaudio/best",
        "format": "best/bestvideo+bestaudio",
        "writeautomaticsub": True,
        "subtitlesformat": "srt",
        # "writesubtitles": True,
        # "allsubtitles": True,
        "skip_download": False,
        "outtmpl": save_path + "/%(title)s.%(ext)s",
        "subtitleslangs": ["en", "fr"],
        "postprocessors": [
            # {
            #     "key": "FFmpegMetadata",
            # },
            # {
            #     "key": "EmbedThumbnail",
            #     "already_have_thumbnail": True,  # overwrite any thumbnails already present
            # },
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
        ],
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:  # type: ignore[arg-type]
        ydl.download([video_url])


if __name__ == "__main__":
    main(url, save_path)
    print("Downloaded Successful!")
