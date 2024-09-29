# Image-Extraction-Service

## Why This Service ? 
In the current AI/ML ecosystem, a significant amount of time is spent preparing data for training models. Therefore, having a robust data preprocessor is essential. This service accelerates that process

## How Does It Help Me ?
The preprocessing step is critical, as various factors depend on it. This service assists teams in bootstrapping one specific scenario: extracting images from formats such as PDF, HTML, PPT, ODT, DOCX, DOC, DWG, and DXF (with plans for future extensions).

The extracted images can be saved in desired formats (e.g., JPEG, PNG) and resolutions.

Even if your use case doesn’t directly involve image extraction, this project provides containerized FastAPI boilerplate code for preprocessing tasks.

If you need to extract images from certain files, there's no need to start from scratch—this service can be leveraged to meet your needs.

## What Does This Service Do?

The service includes built-in Swagger documentation and currently supports image extraction only from PDFs. Future versions will expand its capabilities.

It features one endpoint, /extract_image, which accepts a file. The service detects the file extension to determine which extraction method to apply. It extracts images from all pages, and if a resolution is specified, the extracted images are saved at that resolution, zipped, and sent as a downloadable response.

## Steps To Run This Service

1. Install Git, VS Code, Docker, and the necessary VS Code extensions (DevContainer, Remote SSH, and Docker).
2. Clone this repository using Git.
3. Click the DevContainer button in the lower left corner of VS Code.
4. Once the container is up and running, the post-create command will start the FastAPI app, exposing it on port 5000 (you   can change this if needed).
5. Access the Swagger documentation at http://localhost:5000/docs.

## Contributing to This Project

1. Fork the repo 
2. Make the changes
3. Create a PR and make sure pipeline passes



