from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import StreamingResponse
from services.storage import storage_service

images_router = APIRouter(prefix="/images", tags=["Images"])


@images_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    filename = await storage_service.upload_image(file)

    return {
        "status": "success",
        "image_url": f"/images/{filename}"
    }


@images_router.get("/{filename}")
async def get_image(filename: str):
    body_stream, content_type = await storage_service.get_image(filename)

    
    return StreamingResponse(body_stream, media_type=content_type)