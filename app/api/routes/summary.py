from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.youtube_ingest import download_youtube_audio
from app.services.transcription import transcribe_audio
from app.services.chunking import chunk_transcript,save_chunks
from app.services.summarizer import stream_summary

router = APIRouter(prefix="/summary", tags=["Summary"])


class SummaryRequest(BaseModel):
    source_type: str  # "youtube" or "local"
    source: str       # youtube url OR local file path


@router.post("")
def generate_summary(data: SummaryRequest):
    """
    Full pipeline summary:
    - ingest
    - transcribe
    - chunk
    - stream summary
    """

    # 1️⃣ INGEST
    if data.source_type == "youtube":
        audio_path = download_youtube_audio(data.source)

    elif data.source_type == "local":
        audio_path = data.source

    else:
        raise HTTPException(400, "Invalid source_type")

    # 2️⃣ TRANSCRIBE
    transcription = transcribe_audio(audio_path)
    transcript_path = transcription["transcript_path"]

    # 3️⃣ CHUNK
    chunks = chunk_transcript(transcript_path)

    chunk_file = save_chunks(
        chunks=chunks,
        transcript_path=transcript_path,
        )

    # 4️⃣ STREAM SUMMARY
    return StreamingResponse(
        stream_summary(chunks),
        media_type="text/plain"
    )
