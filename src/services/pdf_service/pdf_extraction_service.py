import fitz
from fastapi import File
import os

def extract_images_from_pdf(file:File):
    doc = fitz.open(file)

    # Iterate through each page
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        image_list = page.get_images(full=True)

    print(f"Image count is {len(image_list)}")