from pathlib import Path
import json
from typing import List, Dict


MAX_CHARS = 1000
OVERLAP_CHARS = 150


def load_transcript(transcript_path: str) -> Dict:
    transcript_path = Path(transcript_path)

    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_transcript(
    transcript_path: str,
    source: str = "youtube"
) -> List[Dict]:
    """
    Convert Whisper transcript into context-preserving chunks.
    """

    data = load_transcript(transcript_path)
    segments = data.get("segments", [])

    chunks = []
    current_text = ""
    current_start = None
    chunk_id = 0

    for segment in segments:
        seg_text = segment["text"].strip()
        seg_start = segment["start"]
        seg_end = segment["end"]

        if not current_text:
            current_start = seg_start

        # If adding this segment exceeds limit → flush chunk
        if len(current_text) + len(seg_text) > MAX_CHARS:
            chunks.append({
                "chunk_id": chunk_id,
                "text": current_text.strip(),
                "start_time": current_start,
                "end_time": prev_end,
                "source": source,
            })

            # overlap
            current_text = current_text[-OVERLAP_CHARS:]
            current_start = seg_start
            chunk_id += 1

        current_text += " " + seg_text
        prev_end = seg_end

    # Final chunk
    if current_text.strip():
        chunks.append({
            "chunk_id": chunk_id,
            "text": current_text.strip(),
            "start_time": current_start,
            "end_time": prev_end,
            "source": source,
        })

    return chunks


def save_chunks(
    chunks: list,
    transcript_path: str,
    output_dir: str = "storage/chunks"
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    transcript_name = Path(transcript_path).stem
    output_path = output_dir / f"{transcript_name}_chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return str(output_path)

