import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.routes.extract_image_routes import router, extract_image_route
from src.constants.constants import VALID_EXTENSION_LIST
from fastapi import UploadFile, HTTPException
import io

# Assuming the following structure:

client = TestClient(router)

class TestExtractImageRoute(unittest.TestCase):

    @patch("src.routes.extract_image_routes.extract_image_service")
    def test_extract_image_route_valid_file(self, mock_extract_image_service):
        # Mock the service to return a BytesIO object
        mock_extract_image_service.return_value = io.BytesIO(b"mocked zip content")
        
        file_content = b"dummy content"
        upload_file = UploadFile(filename="test.pdf", file=io.BytesIO(file_content))

        response = client.post(
            "/extract_image",
            files={"file": (upload_file.filename, upload_file.file, "application/pdf")},
            data={"width": 300, "height": 200},
        )

        # Check response status and headers
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=download.zip")
        self.assertEqual(response.content, b"mocked zip content")

    def test_extract_image_route_invalid_extension(self):
        file_content = b"dummy content"
        upload_file = UploadFile(filename="test.txt", file=io.BytesIO(file_content))

        with self.assertRaises(HTTPException) as context:
            extract_image_route(upload_file)

        # Check response for invalid file type
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail ,f"Only {VALID_EXTENSION_LIST} are supported")

    @patch("src.routes.extract_image_routes.extract_image_service")
    def test_extract_image_route_service_failure(self, mock_extract_image_service):
        # Mock the service to return None
        mock_extract_image_service.return_value = None
        
        file_content = b"dummy content"
        upload_file = UploadFile(filename="test.pdf", file=io.BytesIO(file_content))

        with self.assertRaises(HTTPException) as context:
            extract_image_route(upload_file)

        # Check response for service failure
        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "Error Occurred During Image Extraction")
