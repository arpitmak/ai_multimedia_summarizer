from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.core.logger import logger

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
