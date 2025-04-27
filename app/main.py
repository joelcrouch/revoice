# app/main.py
from fastapi import FastAPI
from app.routes import upload, tts, stream
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(tts.router, prefix="/generate", tags=["TTS"])
app.include_router(stream.router, prefix="/stream", tags=["Stream"])


# Serve the frontend.html manually
@app.get("/")
async def read_index():
    return FileResponse("frontend.html")

# Serve other static files if needed later
app.mount("/static", StaticFiles(directory="static"), name="static")

