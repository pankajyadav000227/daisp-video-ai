from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    prompt: str

@app.post("/api/generate")
async def generate_video(req: VideoRequest):
    """Generate video using HuggingFace free API"""
    try:
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise HTTPException(500, "HF_TOKEN environment variable not set")
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        model_url = "https://api-inference.huggingface.co/models/ali-vilab/text-to-video-ms-1.7b"
        
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                model_url,
                json={"inputs": req.prompt},
                headers=headers
            )
        
        if r.status_code != 200:
            return {"error": f"Video generation failed: {r.text}"}
        
        video_b64 = base64.b64encode(r.content).decode()
        return {
            "status": "success",
            "video_url": f"data:video/mp4;base64,{video_b64}"
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}
