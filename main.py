from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
from heygen_service import get_heygen_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoGenerationRequest(BaseModel):
    text: str
    avatar_id: str = None
    voice_id: str = None
    title: str = None

class VideoStatusRequest(BaseModel):
    video_id: str

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "HeyGen Video AI",
        "features": ["video_generation", "video_listing", "video_deletion"]
    }

@app.post("/api/heygen/generate-video")
async def generate_video(request: VideoGenerationRequest):
    try:
        service = get_heygen_service()
        result = service.create_video(
            text=request.text,
            avatar_id=request.avatar_id,
            voice_id=request.voice_id,
            title=request.title
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/video/{video_id}")
async def get_video(video_id: str):
    try:
        service = get_heygen_service()
        result = service.get_video(video_id)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/videos")
async def list_videos(limit: int = 10, offset: int = 0):
    try:
        service = get_heygen_service()
        result = service.list_videos(limit=limit, offset=offset)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/avatars")
async def list_avatars():
    try:
        service = get_heygen_service()
        result = service.list_avatars()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/voices")
async def list_voices():
    try:
        service = get_heygen_service()
        result = service.list_voices()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.delete("/api/heygen/video/{video_id}")
async def delete_video(video_id: str):
    try:
        service = get_heygen_service()
        result = service.delete_video(video_id)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
