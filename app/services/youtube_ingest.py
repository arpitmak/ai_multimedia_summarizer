# app/services/youtube_ingest.py

from pathlib import Path
import subprocess
import sys
import re
import imageio_ffmpeg


class YouTubeIngestError(RuntimeError):
    pass


def _safe_filename(name: str) -> str:
    """Make filename Windows-safe."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '_', name).strip('_')
    return name[:150]  # keep it reasonable


def download_youtube_audio(url: str, output_dir="storage", cookies_file="cookies.txt") -> str:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    cookies_path = Path(cookies_file).resolve()
    if not cookies_path.exists():
        raise YouTubeIngestError("cookies.txt not found")

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # 🔹 Step 1: Get video info (title + id)
    info_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--cookies", str(cookies_path),
        "--js-runtime", "node",
        "--remote-components", "ejs:github",
        "--print", "%(title)s|%(id)s",
        url,
    ]

    info_proc = subprocess.run(info_cmd, capture_output=True, text=True)
    if info_proc.returncode != 0:
        raise YouTubeIngestError(info_proc.stderr)

    title, video_id = info_proc.stdout.strip().split("|", 1)
    safe_title = _safe_filename(title)

    # 🔹 Step 2: Download audio using readable filename
    outtmpl = str(output_path / f"{safe_title}_{video_id}.%(ext)s")

    dl_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--cookies", str(cookies_path),
        "--js-runtime", "node",
        "--remote-components", "ejs:github",
        "--no-playlist",
        "-f", "140/bestaudio/best",
        "--extract-audio",
        "--audio-format", "m4a",
        "--ffmpeg-location", ffmpeg_path,
        "-o", outtmpl,
        url,
    ]

    proc = subprocess.run(dl_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise YouTubeIngestError(proc.stderr)

    final_audio = output_path / f"{safe_title}_{video_id}.m4a"
    if not final_audio.exists() or final_audio.stat().st_size == 0:
        raise YouTubeIngestError("Audio file missing or empty")

    return str(final_audio)
