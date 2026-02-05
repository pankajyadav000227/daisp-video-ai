import requests
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import json

load_dotenv()

HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY')
HEYGEN_API_BASE = 'https://api.heygen.com/v2'


class HeyGenService:
    """Service for interacting with HeyGen API"""
    
    def __init__(self):
        if not HEYGEN_API_KEY:
            raise ValueError("HEYGEN_API_KEY environment variable not set")
        self.api_key = HEYGEN_API_KEY
        self.base_url = HEYGEN_API_BASE
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        return {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def create_video(self, 
                    text: str,
                    avatar_id: Optional[str] = None,
                    voice_id: Optional[str] = None,
                    title: Optional[str] = None) -> Dict[str, Any]:
        """Create a video using HeyGen API"""
        try:
            payload = {
                "text": text,
                "avatar_id": avatar_id or "wayne-public",
                "voice": {
                    "voice_id": voice_id or "en_us_001"
                }
            }
            
            if title:
                payload["title"] = title
            
            response = requests.post(
                f'{self.base_url}/videos',
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video status and details"""
        try:
            response = requests.get(
                f'{self.base_url}/videos/{video_id}',
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "error"}
    
    def list_videos(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """List all videos"""
        try:
            params = {"limit": limit, "offset": offset}
            response = requests.get(
                f'{self.base_url}/videos',
                headers=self._get_headers(),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def list_avatars(self) -> Dict[str, Any]:
        """Get available avatars"""
        try:
            response = requests.get(
                f'{self.base_url}/avatars',
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def list_voices(self) -> Dict[str, Any]:
        """Get available voices"""
        try:
            response = requests.get(
                f'{self.base_url}/voices',
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def delete_video(self, video_id: str) -> Dict[str, Any]:
        """Delete a video"""
        try:
            response = requests.delete(
                f'{self.base_url}/videos/{video_id}',
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return {"status": "deleted", "video_id": video_id}
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}


# Initialize service
heygen_service = None

def get_heygen_service() -> HeyGenService:
    """Get or create HeyGen service instance"""
    global heygen_service
    if heygen_service is None:
        heygen_service = HeyGenService()
    return heygen_service
