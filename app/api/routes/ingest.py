from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from pydantic import BaseModel
from app.core.logger import logger

from app.services.transcription import transcribe_audio
from app.services.youtube_ingest import download_youtube_audio
from app.services.transcription import transcribe_audio

from app.services.chunking import chunk_transcript
from app.services.embeddings import embed_chunks
from app.services.vector_store import store_chunks
from app.services.chunking import save_chunks

router = APIRouter()


STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)


ALLOWED_EXTENSIONS = {".mp3", ".wav", ".mp4",".m4a"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    save_path = STORAGE_DIR / file.filename
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    logger.info(f"Uploaded file saved to {save_path}")

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "path": str(save_path)
    }

class YouTubeURL(BaseModel):
    url: str

@router.post("/youtube")
def ingest_youtube(data: YouTubeURL):
    try:
        audio_path = download_youtube_audio(data.url)
        return {"status": "success", "audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/youtube-transcribe")
def ingest_youtube_transcribe(data: YouTubeURL):
    try:
        audio_path = download_youtube_audio(data.url)

        transcription_info = transcribe_audio(audio_path)

        return {
            "status": "success",
            "audio_path": audio_path,
            "transcription": transcription_info
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


class QnAIngestRequest(BaseModel):
    source_type: str  # "youtube" | "local"
    source: str       # url or filename


@router.post("/qna")
def ingest_for_qna(data: QnAIngestRequest):
    try:
        # 1️⃣ Resolve audio
        if data.source_type == "youtube":
            audio_path = download_youtube_audio(data.source)

        elif data.source_type == "local":
            audio_path = STORAGE_DIR / data.source
            if not audio_path.exists():
                raise HTTPException(status_code=404, detail="File not found")

        else:
            raise HTTPException(status_code=400, detail="Invalid source_type")

        # 2️⃣ Transcribe
        transcription = transcribe_audio(str(audio_path))
        transcript_path = transcription["transcript_path"]

        # 3️⃣ Chunk
        chunks = chunk_transcript(
            transcript_path=transcript_path,
            source=data.source_type
        )
        

        chunk_file = save_chunks(
        chunks=chunks,
        transcript_path=transcript_path
        )


        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks generated")

        

        # 5️⃣ Store
        store_chunks(chunks)

        return {
            "status": "success",
            "chunks_added": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))