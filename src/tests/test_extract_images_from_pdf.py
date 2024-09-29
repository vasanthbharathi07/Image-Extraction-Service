import unittest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile, HTTPException
import io
from PIL import Image

from src.services.extract_image_services import extract_images_from_pdf

class TestExtractImagesFromPdf(unittest.TestCase):

    @patch("fitz.open")
    @patch("PIL.Image.open")
    def test_extract_images_valid_pdf(self, mock_image_open, mock_fitz_open):
        # Create a mock PDF file with images
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = MagicMock()  # Mock the file attribute
        mock_file.file.read.return_value = b"pdf file bytes"

        # Mock the return of the fitz document
        mock_fitz_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_images.return_value = [(0, 'image')]
        mock_fitz_doc.load_page.return_value = mock_page
        mock_fitz_doc.__len__.return_value = 1  # 1 page PDF
        mock_fitz_open.return_value = mock_fitz_doc

        # Mock the image extracted from the PDF
        mock_fitz_doc.extract_image.return_value = {
            "image": b"image bytes",
            "ext": "jpg"
        }

        # Mock PIL Image open
        mock_pil_image = MagicMock()
        mock_image_open.return_value = mock_pil_image

        # Call the service function
        zip_buffer = extract_images_from_pdf(mock_file)

        # Verify that the result is a valid ZIP file in memory
        self.assertIsInstance(zip_buffer, io.BytesIO)

        # Check that the correct functions were called
        mock_fitz_open.assert_called_once()
        mock_fitz_doc.load_page.assert_called_once_with(0)
        mock_fitz_doc.extract_image.assert_called_once()

    @patch("fitz.open")
    @patch("PIL.Image.open")
    def test_extract_images_with_resize(self, mock_image_open, mock_fitz_open):
        # Create a mock PDF file with images
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = MagicMock()  # Mock the file attribute
        mock_file.file.read.return_value = b"pdf file bytes"

        # Mock the return of the fitz document
        mock_fitz_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_images.return_value = [(0, 'image')]
        mock_fitz_doc.load_page.return_value = mock_page
        mock_fitz_doc.__len__.return_value = 1  # 1 page PDF
        mock_fitz_open.return_value = mock_fitz_doc

        # Mock the image extracted from the PDF
        mock_fitz_doc.extract_image.return_value = {
            "image": b"image bytes",
            "ext": "jpg"
        }

        # Mock PIL Image open and resize
        mock_pil_image = MagicMock()
        mock_resized_image = MagicMock()
        mock_image_open.return_value = mock_pil_image
        mock_pil_image.resize.return_value = mock_resized_image

        # Call the service function with resizing
        zip_buffer = extract_images_from_pdf(mock_file, width=300, height=200)

        # Verify that the image was resized
        mock_pil_image.resize.assert_called_once_with((300, 200))

        # Verify that the result is a valid ZIP file in memory
        self.assertIsInstance(zip_buffer, io.BytesIO)

    @patch("fitz.open")
    def test_extract_images_invalid_pdf(self, mock_fitz_open):
        # Mock an invalid PDF (raising an exception)
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = MagicMock()  # Mock the file attribute
        mock_file.file.read.return_value = b"invalid pdf file bytes"

        mock_fitz_open.side_effect = Exception("Invalid PDF")

        # Call the service function and check for the HTTPException
        with self.assertRaises(HTTPException) as context:
            extract_images_from_pdf(mock_file)

        # Check if the raised exception is correct
        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "An error occurred during PDF image extraction: Invalid PDF")

    @patch("fitz.open")
    def test_no_images_in_pdf(self, mock_fitz_open):
        # Create a mock PDF file with no images
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = MagicMock()  # Mock the file attribute
        mock_file.file.read.return_value = b"pdf file bytes"

        mock_fitz_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_images.return_value = []  # No images
        mock_fitz_doc.load_page.return_value = mock_page
        mock_fitz_doc.__len__.return_value = 1  # 1 page PDF
        mock_fitz_open.return_value = mock_fitz_doc

        # Call the service function
        zip_buffer = extract_images_from_pdf(mock_file)

        # Verify that the result is an empty ZIP file in memory
        self.assertIsInstance(zip_buffer, io.BytesIO)

if __name__ == "__main__":
    unittest.main()
