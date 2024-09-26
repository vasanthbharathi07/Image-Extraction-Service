from typing import Optional
from fastapi import APIRouter,File,UploadFile,Form,Query,HTTPException, status
from services.extract_image_from_pdf_services import extract_image_from_pdf_service
from fastapi.responses import JSONResponse, StreamingResponse

router = APIRouter()

@router.post("/extract_image/pdf")
def extract_image_from_pdf_route(
  file: UploadFile = File(...),
  width: Optional[int] = Form(None),
  height: Optional[int] = Form(None),
  color: Optional[str] = Query("black_and_white", enum=["color", "black_and_white"])
):  
    if not file.filename.endswith('.pdf'):
      raise HTTPException(
         status_code = status.HTTP_400_BAD_REQUEST,
         detail = 'Only PDF documents are supported'
      )
    
    payload = extract_image_from_pdf_service(file,width,height,color)
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