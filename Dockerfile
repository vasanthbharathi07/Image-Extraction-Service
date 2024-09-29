# Use a slim Python base image for smaller size and faster builds
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional, depending on your app's needs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY requirements_dev.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src
COPY run_mypy.sh /app/

EXPOSE 5000

# Use Uvicorn to serve the FastAPI app in production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4", "--log-level", "info"]
