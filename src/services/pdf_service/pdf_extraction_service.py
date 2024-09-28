import fitz
from fastapi import File, HTTPException
from PIL import Image
import os
import io
import zipfile
from fastapi.responses import JSONResponse
import shutil

def extract_images_from_pdf(uploaded_file_artifact:File,width=None,height=None):
    zip_buffer = None
    try:
        file_bytes = uploaded_file_artifact.file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")  # use stream instead of filename
        total_images_count = 0
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer,'w',zipfile.ZIP_DEFLATED) as zip_file:
            # Iterate through each page
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                images = page.get_images(full=True)
                total_images_count = total_images_count + len(images)
                for image_inx,img in enumerate(images):
                    base_image = doc.extract_image(img[0])
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    # Convert image bytes to a PIL Image object
                    image = Image.open(io.BytesIO(image_bytes))

                    if width is not None or height is not None:
                        #Resize the image to the desired width and height
                        resized_image = image.resize((width, height))
                        image = resized_image

                    # Save the image as JPEG
                    image_io = io.BytesIO()
                    image.save(image_io, 'JPEG')
                    image_io.seek(0)
                    image_name = f'page_{page_number + 1}_image_{image_inx + 1}.jpg'
                    zip_file.writestr(image_name,image_io.read())

        
        zip_buffer.seek(0)
    except Exception as e:
        # Handle any exception and raise HTTP 500 error
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during PDF image extraction: {str(e)}"
        )
    
    finally:
        # Clean up the document
        if 'doc' in locals() and doc is not None:
            doc.close()
    
    return zip_buffer