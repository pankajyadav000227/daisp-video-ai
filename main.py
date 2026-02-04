from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import asyncio
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

# API Keys from environment variables (optional for free tier)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

@app.post("/api/generate-image")
async def generate_image(request: Request):
    """Generate image using AI Horde (FREE - no API key required)"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        # Using AI Horde - completely free, no authentication needed
        async with httpx.AsyncClient() as client:
            # Create generation request
            generation_payload = {
                "prompt": prompt,
                "params": {
                    "width": 512,
                    "height": 512,
                    "steps": 20,
                    "n": 1
                },
                "models": ["stable_diffusion_xl"],
                "nsfw": False
            }
            
            response = await client.post(
                "https://api.aihorde.net/v2/generate/async",
                json=generation_payload,
                timeout=30.0
            )
            
            if response.status_code != 202:
                return {"error": f"Failed to start image generation: {response.text[:200]}"}
            
            result = response.json()
            request_id = result.get("id")
            
            if not request_id:
                return {"error": "No request ID received from AI Horde"}
            
            # Poll for completion (max 2 minutes)
            max_attempts = 120
            for attempt in range(max_attempts):
                check_response = await client.get(
                    f"https://api.aihorde.net/v2/generate/check/{request_id}",
                    timeout=10.0
                )
                
                if check_response.status_code == 200:
                    check_result = check_response.json()
                    if check_result.get("done"):
                        result_response = await client.get(
                            f"https://api.aihorde.net/v2/generate/status/{request_id}",
                            timeout=10.0
                        )
                        if result_response.status_code == 200:
                            result_data = result_response.json()
                            images = result_data.get("generations", [])
                            if images and len(images) > 0:
                                image_b64 = images[0].get("img")
                                if image_b64:
                                    return {
                                        "status": "success",
                                        "image_url": f"data:image/webp;base64,{image_b64}",
                                        "prompt": prompt
                                    }
                        break
                
                await asyncio.sleep(1)
            
            return {"error": "Image generation timed out"}
        
    except Exception as e:
        return {"error": f"Error generating image: {str(e)}"}

@app.post("/api/generate-script")
async def generate_script(request: Request):
    """Generate video script using Groq (FREE API)"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        if not prompt:
            raise HTTPException(400, "prompt field is required")
        
        if GROQ_API_KEY:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json={
                        "model": "mixtral-8x7b-32768",
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
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
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
        
        # Fallback demo script
        demo_script = f"""[Scene 1: Opening]
Voiceover: Welcome to our video about {prompt}
Visuals: Beautiful transitions and modern effects
Text overlay: Main title with elegant typography

[Scene 2: Main Content]
Voiceover: Let's explore the key aspects
Visuals: High-quality footage, animations, and graphics

[Scene 3: Conclusion]
Voiceover: Thank you for watching!
Visuals: Recap with smooth transitions

[Scene 4: Credits]
Visuals: Rolling credits with background music"""
        
        return {
            "status": "success",
            "script": demo_script,
            "message": "Using demo script",
            "prompt": prompt
        }
        
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
        
        image_result = await generate_image(Request(
            {
                "type": "http",
                "method": "POST",
                "body": json.dumps({"prompt": prompt}).encode()
            }
        ))
        
        script_result = await generate_script(Request(
            {
                "type": "http",
                "method": "POST",
                "body": json.dumps({"prompt": prompt}).encode()
            }
        ))
        
        return {
            "status": "success",
            "image_url": image_result.get("image_url"),
            "script": script_result.get("script"),
            "image_error": image_result.get("error"),
            "script_error": script_result.get("error"),
            "prompt": prompt
        }
        
    except Exception as e:
        return {"error": f"Error generating video: {str(e)}"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "ai_horde_available": True,
        "groq_configured": bool(GROQ_API_KEY)
    }
