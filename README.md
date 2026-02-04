# AI Video Generator for daisp.live

🎬 Transform text prompts into stunning videos using AI-powered technology.

## Project Overview

This is a complete AI Video Generator application that converts text descriptions into videos. It includes:

- **Backend**: FastAPI server deployed on Render.com
- **Frontend**: Beautiful web interface for video generation
- **AI Model**: HuggingFace text-to-video model

## Live Deployment

- **Backend API**: https://daisp-video-ai.onrender.com
- **Frontend**: Will be deployed on daisp.live

## Features

✨ **Easy to Use**: Simple text input to generate videos
🚀 **Fast Processing**: Powered by AI models
💾 **Download Videos**: Save generated videos to your device
🎨 **Modern UI**: Beautiful and responsive design
🔄 **Real-time Status**: See generation progress

## Quick Start Guide

### For End Users

1. Visit the AI Video Generator at `https://daisp.live` (or your deployment URL)
2. Enter your video description in the text area
3. Click "Generate Video"
4. Wait for the AI to generate your video
5. Download or watch directly in the browser

### For Developers

#### Prerequisites

- Python 3.8+
- HuggingFace API Token (free)
- Render.com account (free tier)

#### Installation

```bash
# Clone the repository
git clone https://github.com/pankajyadav000227/daisp-video-ai.git
cd daisp-video-ai

# Install dependencies
pip install -r requirements.txt
```

#### Configuration

1. **Get HuggingFace API Token**:
   - Visit https://huggingface.co/settings/tokens
   - Create a new token (read access is sufficient)
   - Copy the token

2. **Set Environment Variable** (for local testing):
   ```bash
   export HF_TOKEN="your_huggingface_token_here"
   ```

3. **Deploy to Render**:
   - The backend is already deployed
   - To update: Push to GitHub, Render auto-deploys
   - To configure HF token:
     1. Go to https://dashboard.render.com/web/srv-d61su4qli9vc739chds0/env
     2. Set `HF_TOKEN` environment variable
     3. Redeploy the service

#### Local Development

```bash
# Run the backend locally
uvicorn main:app --reload

# The API will be available at http://localhost:8000
```

#### Deploy Frontend

1. **Copy `index.html`** to your web server
2. **Update API URL** in `index.html` if needed
3. **Upload to daisp.live** using FTP/FileZilla

## API Documentation

### Generate Video

**Endpoint**: `POST /api/generate`

**Request**:
```json
{
  "prompt": "A beautiful sunset over the ocean with waves crashing on the beach"
}
```

**Response (Success)**:
```json
{
  "status": "success",
  "video_url": "data:video/mp4;base64,..."
}
```

**Response (Error)**:
```json
{
  "error": "Error message describing what went wrong"
}
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

## Troubleshooting

### "HF_TOKEN environment variable not set"

Solution: Configure the HuggingFace token in Render:
1. Go to Render dashboard
2. Select the daisp-video-ai service
3. Go to Environment tab
4. Add `HF_TOKEN` variable with your HuggingFace API token
5. Redeploy the service

### Video Generation Times Out

The free HuggingFace API can be slow. First-time requests may take 2-3 minutes.

### CORS Errors

The API supports CORS for cross-origin requests. If issues persist, check browser console for specific errors.

## File Structure

```
daisp-video-ai/
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── index.html          # Frontend UI
├── Procfile            # Render deployment config
├── README.md           # This file
└── .gitignore
```

## Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI Model**: HuggingFace transformers (text-to-video)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Hosting**: Render.com (backend), daisp.live or similar (frontend)

## Installation Steps for daisp.live

### Step 1: Prepare Frontend

1. Download or copy `index.html` from this repo
2. No modifications needed if backend is at https://daisp-video-ai.onrender.com

### Step 2: Upload to daisp.live

**Using FileZilla**:
1. Open FileZilla
2. Enter FTP credentials for daisp.live
3. Drag and drop `index.html` to the public_html folder
4. Set permissions to 644 for index.html

**Using cPanel File Manager**:
1. Log in to cPanel
2. Open File Manager
3. Navigate to public_html
4. Upload index.html

### Step 3: Configure Backend Token

1. Visit https://dashboard.render.com
2. Select daisp-video-ai service
3. Go to Environment variables
4. Add/Update `HF_TOKEN` with your HuggingFace token
5. Redeploy

### Step 4: Test

1. Visit https://daisp.live
2. Enter a test prompt
3. Click "Generate Video"
4. Check browser console (F12) for any errors

## Support

For issues or questions:
- Check the Troubleshooting section
- Review browser console for error messages
- Check Render service logs at https://dashboard.render.com

## License

This project is open source and available for educational and commercial use.

## Author

Created for daisp.live by pankajyadav000227

---

**Last Updated**: February 2026
**Status**: Production Ready
