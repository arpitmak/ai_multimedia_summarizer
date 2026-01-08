from pathlib import Path
import whisper


model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file using Whisper and return the text.
    """
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"{audio_path} does not exist")

    result = model.transcribe(str(audio_file))
    return result["text"]
