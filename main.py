from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import base64
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from heygen_service import get_heygen_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_demo_image(prompt: str) -> str:
    """
    Generate a demo placeholder image with the prompt text.
    This works entirely on Render free tier without external API calls.
    """
    try:
        # Create a gradient image
        img = Image.new('RGB', (512, 512), color=(70, 130, 180))  # Steel blue
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for i in range(512):
            color = (70 + i//4, 130 - i//8, 180 + i//10)
            draw.line([(0, i), (512, i)], fill=color)
        
        # Add text
        text = f"✨ AI Generated: {prompt[:40]}..." if len(prompt) > 40 else f"✨ AI Generated: {prompt}"
        try:
            draw.text((256, 256), text, fill=(255, 255, 255), anchor="mm", align="center")
        except:
            # Fallback if font issues
            draw.text((50, 240), text[:30], fill=(255, 255, 255))
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_b64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_b64}"
    except Exception as e:
        # Return a solid color if image generation fails
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='512' height='512'%3E%3Crect fill='%234682B4' width='512' height='512'/%3E%3Ctext x='256' y='256' text-anchor='middle' fill='white' font-size='24'%3EGenerated Image%3C/text%3E%3C/svg%3E"

@app.post("/api/generate-image")
async def generate_image(request: Request):
    """
    Generate image - demo version for free tier compatibility
    """
    try:
        data = await request.json()
        prompt = data.get("prompt", "abstract art")
        
        if not prompt:
            prompt = "abstract art"
        
        image_url = generate_demo_image(prompt)
        return {
            "status": "success",
            "image_url": image_url,
            "prompt": prompt,
            "note": "Demo image generated. For production image generation, configure OpenAI DALL-E API key."
        }
    except Exception as e:
        return {"error": f"Error generating image: {str(e)}"}

@app.post("/api/generate-script")
async def generate_script(request: Request):
    """
    Generate video script - demo version
    """
    try:
        data = await request.json()
        prompt = data.get("prompt", "a creative video")
        
        if not prompt:
            prompt = "a creative video"
        
        # Generate a professional video script template
        demo_script = f"""[Scene 1: Opening]
Voiceover: Welcome to our video about {prompt}
Visuals: Engaging opening sequence with smooth transitions
Text overlay: "\"" + prompt + "\"" + """
Duration: 5 seconds
    """
        return {
                "status": "success",
                        "script": prompt,
                                "note": "Demo script template - use with FastAPI endpoints"
                                    }
                                        except Exception as e:
                                                return {"status": "error", "error": str(e)}
    """
    Generate video combining image and script - demo version
    """
    try:
        data = await request.json()
        prompt = data.get("prompt", "a creative video project")
        
        image_result = await generate_image(Request({
            "type": "http",
            "method": "POST",
            "body": json.dumps({"prompt": prompt}).encode()
        }))
        
        script_result = await generate_script(Request({
            "type": "http",
            "method": "POST",
            "body": json.dumps({"prompt": prompt}).encode()
        }))
        
        return {
            "status": "success",
            "image_url": image_result.get("image_url"),
            "script": script_result.get("script"),
            "prompt": prompt,
            "note": "Full video project created with demo content. Upgrade API keys for production quality."
        }
    except Exception as e:
        return {"error": f"Error generating video: {str(e)}"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "AI Content Generator",
        "features": ["image_generation", "script_generation", "video_generation"]
    }


# HeyGen API Endpoints
from pydantic import BaseModel

class VideoGenerationRequest(BaseModel):
    text: str
    avatar_id: str = None
    voice_id: str = None
    title: str = None

@app.post("/api/heygen/generate-video")
async def generate_video(request: VideoGenerationRequest):
    """Generate a video using HeyGen API"""
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
    """Get video status and details"""
    try:
        service = get_heygen_service()
        result = service.get_video(video_id)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/videos")
async def list_videos(limit: int = 10, offset: int = 0):
    """List all videos"""
    try:
        service = get_heygen_service()
        result = service.list_videos(limit=limit, offset=offset)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/avatars")
async def list_avatars():
    """Get available avatars"""
    try:
        service = get_heygen_service()
        result = service.list_avatars()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/heygen/voices")
async def list_voices():
    """Get available voices"""
    try:
        service = get_heygen_service()
        result = service.list_voices()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.delete("/api/heygen/video/{video_id}")
async def delete_video(video_id: str):
    """Delete a video"""
    try:
        service = get_heygen_service()
        result = service.delete_video(video_id)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
