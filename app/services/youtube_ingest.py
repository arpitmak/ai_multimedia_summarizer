
from yt_dlp import YoutubeDL
from pathlib import Path

def download_youtube_audio(url: str, output_dir="storage") -> str:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # 🔒 THIS IS THE KEY LINE
        filename = ydl.prepare_filename(info)
        audio_path = Path(filename).with_suffix(".m4a")

    return str(audio_path)
 