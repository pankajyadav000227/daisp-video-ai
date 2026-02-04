from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import base64
import io
from PIL import Image, ImageDraw
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate")
async def generate_video(request: Request):
    """Generate video using working method"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise HTTPException(500, "HF_TOKEN environment variable not set")
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Try using Hugging Face Inference API with text-to-image then convert to video
        # or use a different model that actually generates videos
        model_url = "https://api-inference.huggingface.co/models/KappaNeuro/text-to-video"
        
        async with httpx.AsyncClient(timeout=180) as client:
            try:
                response = await client.post(
                    model_url,
                    json={"inputs": prompt},
                    headers=headers
                )
                
                if response.status_code == 200:
                    video_content = response.content
                    video_b64 = base64.b64encode(video_content).decode()
                    return {
                        "status": "success",
                        "video_url": f"data:video/mp4;base64,{video_b64}"
                    }
                else:
                    # Fallback: return error details
                    return {
                        "error": f"API returned {response.status_code}: {response.text[:200]}"
                    }
            except Exception as e:
                return {
                    "error": f"Failed to generate video: {str(e)}"
                }
    
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}
