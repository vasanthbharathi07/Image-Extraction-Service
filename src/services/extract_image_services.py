from fastapi import File, UploadFile
from src.services.pdf_service.pdf_extraction_service import extract_images_from_pdf


def extract_image_service(file_extension,file:UploadFile = File(...),width=None,height=None):
    if file_extension == ".pdf":
        return extract_images_from_pdf(file,width,height)