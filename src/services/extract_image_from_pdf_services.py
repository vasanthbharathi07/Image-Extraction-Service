from fastapi import File
from services.pdf_service.pdf_extraction_service import extract_images_from_pdf


def extract_image_from_pdf_service(file:File,width,height,color):
    return extract_images_from_pdf(file)