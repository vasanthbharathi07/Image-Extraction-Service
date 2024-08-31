from typing import Union

from fastapi import FastAPI
from routes.extract_image_from_pdf_routes import router as extract_image_from_pdf_router

app = FastAPI()

app.include_router(extract_image_from_pdf_router)
# app.include_router(extract_image_from_docx, prefix="/api/v1")
# app.include_router(extract_image_from_pptx, prefix="/api/v1")
# app.include_router(extract_image_from_dicom, prefix="/api/v1")
# app.include_router(extract_image_from_web_page, prefix="/api/v1")
# app.include_router(extract_image_from_epub, prefix="/api/v1")
# app.include_router(extract_image_from_mobi, prefix="/api/v1")
# app.include_router(extract_image_from_dwg, prefix="/api/v1")
# app.include_router(extract_image_from_dxf, prefix="/api/v1")
# app.include_router(extract_image_from_psd, prefix="/api/v1")
# app.include_router(extract_image_from_ai, prefix="/api/v1")