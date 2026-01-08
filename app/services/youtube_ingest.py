import os
import re
import yt_dlp
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """
    Remove or replace characters that are invalid in Windows filenames.
    """
    # Replace invalid characters with underscore
    return re.sub(r'[<>:"/\\|?*#…]', '_', name)

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

def download_youtube_audio(url: str) -> str:
    """
    Download audio from YouTube and return path to saved audio file
    """
    output_template = str(STORAGE_DIR / "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "128",
        }],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = sanitize_filename(info_dict.get("title", "audio"))
        filename = STORAGE_DIR / f"{title}.m4a"
        return str(filename)
