from typing import Optional
from fastapi import APIRouter,File,UploadFile,Form,Query,HTTPException, status
from services.extract_image_services import extract_image_service
from fastapi.responses import JSONResponse, StreamingResponse
from constants.constants import VALID_EXTENSION_LIST
import os

router = APIRouter()

@router.post("/extract_image")
def extract_image_route(
  file: UploadFile = File(...),
  width: Optional[int] = Form(None),
  height: Optional[int] = Form(None)
):  
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in VALID_EXTENSION_LIST:
      raise HTTPException(
         status_code = status.HTTP_400_BAD_REQUEST,
         detail = f"Only {VALID_EXTENSION_LIST} are supported"
      )
    
    payload = extract_image_service(file_extension,file,width,height)
    if payload is None:
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Error Occurred During Image Extraction'
    )
    else:
       response = StreamingResponse(
        payload,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=download.zip"}
    )
    return response