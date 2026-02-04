from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import base64
import json
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")  # xAI Grok API key

@app.post("/api/generate-image")
async def generate_image(request: Request):
    """Generate image using OpenAI DALL-E"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        if not OPENAI_API_KEY:
            return {"error": "OpenAI API key not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/images/generations",
                json={
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "standard",
                    "model": "dall-e-3"
                },
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                timeout=120.0
            )
            
            if response.status_code != 200:
                error_detail = response.text
                return {"error": f"OpenAI API error: {error_detail[:200]}"}
            
            result = response.json()
            image_url = result.get("data", [{}])[0].get("url")
            
            if image_url:
                # Download the image and convert to base64
                img_response = await client.get(image_url, timeout=30.0)
                if img_response.status_code == 200:
                    img_b64 = base64.b64encode(img_response.content).decode()
                    return {
                        "status": "success",
                        "image_url": f"data:image/png;base64,{img_b64}",
                        "prompt": prompt
                    }
            
            return {"error": "Failed to retrieve image from OpenAI"}
    
    except Exception as e:
        return {"error": f"Error generating image: {str(e)}"}

@app.post("/api/generate-script")
async def generate_script(request: Request):
    """Generate video script using Grok (xAI free API)"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        if not GROK_API_KEY:
            # Return a demo script if API key not set
            demo_script = f"""[Scene 1: Opening]
Voiceover: Creating video content: {prompt}
Visuals: Beautiful transitions and effects

[Scene 2: Main Content]
Voiceover: Exploring the concept in detail
Visuals: High-quality footage and graphics

[Scene 3: Conclusion]
Voiceover: Thank you for watching!
Visuals: Credits and call to action"""
            return {
                "status": "success",
                "script": demo_script,
                "message": "Using demo script (Grok API key not configured)"
            }
        
        async with httpx.AsyncClient() as client:
            # Grok API through xAI
            response = await client.post(
                "https://api.x.ai/chat/completions",
                json={
                    "model": "grok-3",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a creative video script writer. Write engaging, professional video scripts with scene descriptions, dialogue, and visual directions."
                        },
                        {
                            "role": "user",
                            "content": f"Write a professional video script for: {prompt}\n\nFormat the script with [Scene X] headers and include voiceover, dialogue, and visual directions."
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 1000
                },
                headers={"Authorization": f"Bearer {GROK_API_KEY}"},
                timeout=60.0
            )
            
            if response.status_code == 200:
                result = response.json()
                script = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                if script:
                    return {
                        "status": "success",
                        "script": script,
                        "prompt": prompt
                    }
            
            return {"error": "Failed to generate script from Grok API"}
    
    except Exception as e:
        return {"error": f"Error generating script: {str(e)}"}

@app.post("/api/generate-video")
async def generate_video(request: Request):
    """Generate video combining image and script"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        # Step 1: Generate image
        image_result = await generate_image(Request({"type": "http", "method": "POST", "body": json.dumps({"prompt": prompt}).encode()}))
        
        # Step 2: Generate script
        script_result = await generate_script(Request({"type": "http", "method": "POST", "body": json.dumps({"prompt": prompt}).encode()}))
        
        if "error" in image_result or "error" in script_result:
            return {
                "status": "partial",
                "image": image_result.get("image_url"),
                "script": script_result.get("script"),
                "warning": image_result.get("error") or script_result.get("error")
            }
        
        # Return combined result
        return {
            "status": "success",
            "image_url": image_result.get("image_url"),
            "script": script_result.get("script"),
            "prompt": prompt
        }
    
    except Exception as e:
        return {"error": f"Error generating video: {str(e)}"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "openai_configured": bool(OPENAI_API_KEY),
        "grok_configured": bool(GROK_API_KEY)
    }
