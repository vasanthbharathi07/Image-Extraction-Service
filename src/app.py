from typing import Union

from fastapi import FastAPI
from src.routes.extract_image_routes import router as extract_image_route

app = FastAPI()

app.include_router(extract_image_route)