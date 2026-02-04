# AI Video Generator - Complete Installation Guide for daisp.live

## Status: ✅ READY FOR DEPLOYMENT

Your AI Video Generator is now fully built and deployed! Follow these steps to complete the setup.

---

## QUICK SUMMARY

| Component | Status | URL |
|-----------|--------|-----|
| Backend API | ✅ Live | https://daisp-video-ai.onrender.com |
| Health Check | ✅ Working | https://daisp-video-ai.onrender.com/health |
| Frontend HTML | ✅ Ready | Ready to upload to daisp.live |
| GitHub Repo | ✅ Complete | https://github.com/pankajyadav000227/daisp-video-ai |

---

## STEP 1: Get HuggingFace API Token (5 minutes)

The backend needs a HuggingFace token to generate videos.

### Method 1: Free HuggingFace Token (Recommended)

1. **Visit**: https://huggingface.co/settings/tokens
2. **Login** with your HuggingFace account (create one if you don't have)
3. **Click** "New token"
4. **Name**: "daisp-video-ai"
5. **Type**: Select "Read"
6. **Click** "Generate token"
7. **Copy** the token (you'll need it in next step)

**Token looks like**: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## STEP 2: Configure Backend Token in Render (3 minutes)

1. **Visit**: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0/env

2. **Find** the "HF_TOKEN" environment variable

3. **Update** it with your HuggingFace token:
   - Click the value field
   - Clear the current value
   - Paste your HuggingFace token
   - Click "Save"

4. **Redeploy**:
   - Go to: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0
   - Click "Manual Deploy" button
   - Select "Deploy latest commit"
   - Wait for deployment to complete (status will show green "Live")

**Note**: First deploy after token update takes 2-3 minutes.

---

## STEP 3: Upload Frontend to daisp.live (5 minutes)

### Option A: Using FileZilla (Easiest)

1. **Download FileZilla**: https://filezilla-project.org/

2. **Get FTP Credentials**:
   - Log in to InfinityFree/hosting panel
   - Find FTP details:
     - FTP Host
     - FTP Username
     - FTP Password

3. **Connect in FileZilla**:
   - Host: Your FTP host
   - Username: Your FTP username  
   - Password: Your FTP password
   - Port: 21 (usually)
   - Click "Quickconnect"

4. **Navigate** to `public_html` folder (right panel)

5. **Download** `index.html`:
   - Go to: https://github.com/pankajyadav000227/daisp-video-ai/raw/main/index.html
   - Save to your computer

6. **Upload** `index.html`:
   - Drag and drop from left to right panel
   - Or right-click → Upload

7. **Verify**:
   - Visit https://daisp.live
   - You should see the AI Video Generator UI!

### Option B: Using cPanel File Manager

1. **Log in** to your hosting cPanel

2. **Click** "File Manager"

3. **Navigate** to public_html

4. **Click** "Upload" button

5. **Select** index.html file (download first from GitHub)

6. **Wait** for upload to complete

---

## STEP 4: Test the Complete System (2 minutes)

### Test 1: Check Backend

```
Visit: https://daisp-video-ai.onrender.com/health
Expected Response: {"status": "ok"}
```

### Test 2: Visit Frontend

```
Visit: https://daisp.live
You should see: Beautiful purple gradient UI with input field
```

### Test 3: Generate a Test Video

1. **Visit**: https://daisp.live
2. **Type**: "A beautiful sunset"
3. **Click**: "Generate Video"
4. **Wait**: 1-2 minutes (first time is slower)
5. **See**: Generated video plays in browser
6. **Download**: Click "Download Video" button

---

## TROUBLESHOOTING

### Problem: "HF_TOKEN environment variable not set"

**Solution**:
1. Check Render dashboard at: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0/env
2. Verify HF_TOKEN is set to your HuggingFace token
3. Redeploy the service
4. Wait 3 minutes
5. Try again

### Problem: Frontend won't load

**Solution**:
1. Check if index.html is uploaded to public_html
2. Visit https://daisp.live/index.html (with filename)
3. Check permissions (should be 644)
4. Clear browser cache (Ctrl+Shift+Delete)
5. Try different browser

### Problem: Video generation times out

**Solution**:
- First-time generation takes 2-3 minutes (normal)
- Try again after waiting
- Check browser console (F12) for errors
- Check Render logs at: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0/logs

### Problem: CORS error in browser console

**Solution**:
- Already configured in backend
- Clear browser cache
- Try in incognito mode
- Check Network tab for actual error

---

## API USAGE (For Integration)

### Generate Video

```javascript
const response = await fetch('https://daisp-video-ai.onrender.com/api/generate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prompt: 'Your video description here'
  })
});

const data = await response.json();
if (data.status === 'success') {
  console.log('Video URL:', data.video_url);
}
```

---

## MAINTENANCE

### Keep Backend Updated

- Backend auto-updates when code is pushed to GitHub
- No manual deployment needed
- Monitor at: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0

### Update Frontend

- Re-upload index.html via FileZilla
- Old browsers may cache old version
- Instruct users to hard refresh (Ctrl+F5)

### Monitor Costs

- Backend: Free tier (limits: 750 hours/month)
- Frontend: Depends on hosting
- API calls: Free (HuggingFace free tier)

---

## NEXT STEPS (Optional)

### Add Custom Domain

- Point your domain to daisp.live
- Configure SSL certificate
- Update API URL in index.html if needed

### Add Analytics

- Google Analytics
- Mixpanel
- Custom logging

### Scale Up

- Upgrade Render to paid tier for faster generation
- Use commercial video model (Runwayml, Synthesia)
- Cache generated videos

---

## SUPPORT

- **Backend Logs**: https://dashboard.render.com/web/srv-d61su4qli9vc739chds0/logs
- **GitHub Issues**: https://github.com/pankajyadav000227/daisp-video-ai/issues
- **Render Support**: https://render.com/support
- **HuggingFace Support**: https://huggingface.co/support

---

## Deployment Complete! 🎉

Your AI Video Generator is ready. Share the link and start creating videos!

**Website**: https://daisp.live
**API**: https://daisp-video-ai.onrender.com
**Repository**: https://github.com/pankajyadav000227/daisp-video-ai

---

**Last Updated**: February 5, 2026
**Version**: 1.0
**Status**: Production Ready
