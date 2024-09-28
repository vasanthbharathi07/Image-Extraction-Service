import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from fastapi import UploadFile
import io
import os

# Assuming the following structure:
from app import app  # Adjust the import based on your structure
from services.extract_image_services import extract_image_service
from constants.constants import VALID_EXTENSION_LIST

client = TestClient(app)

class TestExtractImageRoute(unittest.TestCase):

    @patch("services.extract_image_services.extract_image_service")
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

        response = client.post(
            "/extract_image",
            files={"file": (upload_file.filename, upload_file.file, "text/plain")},
            data={"width": 300, "height": 200},
        )

        # Check response for invalid file type
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": f"Only {VALID_EXTENSION_LIST} are supported"})

    @patch("services.extract_image_services.extract_image_service")
    def test_extract_image_route_service_failure(self, mock_extract_image_service):
        # Mock the service to return None
        mock_extract_image_service.return_value = None
        
        file_content = b"dummy content"
        upload_file = UploadFile(filename="test.pdf", file=io.BytesIO(file_content))

        response = client.post(
            "/extract_image",
            files={"file": (upload_file.filename, upload_file.file, "application/pdf")},
            data={"width": 300, "height": 200},
        )

        # Check response for service failure
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Error Occurred During Image Extraction"})


if __name__ == "__main__":
    unittest.main()
