import fitz
from fastapi import File
from PIL import Image
import os
import io

def extract_images_from_pdf(uploaded_file_artifact:File):

    file_bytes = uploaded_file_artifact.file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")  # use stream instead of filename
    
    total_images_count = 0
    current_file_dir = os.path.dirname(__file__)
    print('CWD = {curr_file_dir}')
    output_dir = os.path.join(current_file_dir, "../../../resource/extracted_image")
    if not os.path.exists(output_dir):
        return False

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

            # Define the output path
            output_path = os.path.join(output_dir, f'page_{page_number + 1}_image_{image_inx + 1}.jpg')

            # Save the image as JPEG
            image.save(output_path, 'JPEG')

    print(f"Image count is {total_images_count}")
    doc.close()
    return True