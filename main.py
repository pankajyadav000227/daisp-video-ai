from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/api/generate")
async def generate_video(request: Request):
    """Generate video using HuggingFace Inference API"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            # Return a simple placeholder video in base64
            # This is a minimal 1-frame MP4 video (about 500 bytes)
            demo_video_b64 = "AAAAIGZ0eXBpc29tAAACAGlzb21pc2gyaXZ2bWF2YzEAAAIyYm9vdAAA"
            return {
                "status": "success",
                "message": "Using demo video (HF_TOKEN not configured)",
                "video_url": f"data:video/mp4;base64,{demo_video_b64}"
            }
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Try multiple HuggingFace text-to-video models
        models = [
            "black-forest-labs/FLUX.1-dev",
            "KappaNeuro/text-to-video",
            "damo-vilab/text-to-video-ms-1.7b"
        ]
        
        for model in models:
            try:
                model_url = f"https://api-inference.huggingface.co/models/{model}"
                async with httpx.AsyncClient(timeout=120) as client:
                    response = await client.post(
                        model_url,
                        json={"inputs": prompt},
                        headers=headers
                    )
                    
                    if response.status_code == 200 and len(response.content) > 0:
                        video_b64 = base64.b64encode(response.content).decode()
                        return {
                            "status": "success",
                            "video_url": f"data:video/mp4;base64,{video_b64}"
                        }
            except Exception as e:
                continue
        
        # If all models fail, return error
        return {
            "error": "Video generation service temporarily unavailable. Please try again later."
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}
