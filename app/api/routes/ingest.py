from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from pydantic import BaseModel
from app.core.logger import logger

from app.services.transcription import transcribe_audio
from app.services.youtube_ingest import download_youtube_audio
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
        text = transcribe_audio(audio_path)
        return {"status": "success", "audio_path": audio_path, "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))