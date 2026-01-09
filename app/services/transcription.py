import whisper
import json
from pathlib import Path

MODEL_NAME = "base"

model = whisper.load_model(MODEL_NAME)

def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    elif hasattr(obj, "item"):  # numpy scalars
        return obj.item()
    else:
        return obj


def transcribe_audio(audio_path: str, output_dir: str = "storage/transcripts"):
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = model.transcribe(str(audio_path))

    # 🔒 FIX: make result JSON-safe
    safe_result = make_json_serializable(result)

    transcript_path = output_dir / f"{audio_path.stem}.json"

    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(safe_result, f, ensure_ascii=False, indent=2)

    return {
        "transcript_path": str(transcript_path),
        "language": safe_result.get("language"),
        "text_preview": safe_result.get("text", "")[:300]
    }


