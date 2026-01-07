# How to Deploy Changes

## Step-by-Step Deployment Guide

### 1. Copy Updated Files to Your Local Repository

You need to copy these updated files from your local workspace to the GitHub repo:

**Integration files** (copy to `integration/` folder):
- `integration/nest_listener.py` - Updated with API fetch and filesystem fallback
- `integration/services.py` - Added `fire_nest_event` service
- `integration/services.yaml` - Added service schema
- `integration/__init__.py` - Updated default port to 8080

**Add-on files** (copy to `face_recognition/face_recognition/` folder):
- `face_recognition/face_recognition/face_recognition_addon/__main__.py` - Added gunicorn support
- `face_recognition/face_recognition/face_recognition_addon/api.py` - Improved error handling
- `face_recognition/face_recognition/config.yaml` - Updated port mapping to 8080

### 2. Commit Changes to Git

**Using GitHub Desktop:**
1. Open GitHub Desktop
2. You should see all changed files listed
3. **Review the changes** (click on files to see diffs)
4. **Write commit message:**
   ```
   Chunk 3: Nest Event Ingestion - API fetch, filesystem fallback, video frame extraction
   ```
5. Click **Commit to main**
6. Click **Push origin** to upload to GitHub

**Using Command Line:**
```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition
git add .
git commit -m "Chunk 3: Nest Event Ingestion - API fetch, filesystem fallback, video frame extraction"
git push
```

### 3. Update Add-on in Home Assistant

**After pushing to GitHub:**

1. **Go to:** Settings → Add-ons → Face Recognition
2. **Click:** **Uninstall** (removes old container)
3. **Click:** **Install** (rebuilds with new code from GitHub)
4. **Wait** for installation to complete (1-2 minutes)
5. **Click:** **Start**
6. **Check Logs** - Should see:
   - "Checking for Gunicorn availability..."
   - Either "Gunicorn found!" or "Gunicorn not available"
   - "HTTP API server starting on port 8080"

### 4. Update Integration in Home Assistant

**After pushing to GitHub:**

1. **Copy integration files** to Home Assistant:
   - Use **File Editor** add-on or **SSH**
   - Copy files from `integration/` to `/config/custom_components/face_recognition/`
   
2. **Files to copy:**
   - `integration/nest_listener.py`
   - `integration/services.py`
   - `integration/services.yaml`
   - `integration/__init__.py`

3. **Restart Home Assistant:**
   - Settings → System → Restart
   - Or Developer Tools → YAML → Restart

### 5. Verify Configuration

**Make sure your `configuration.yaml` has:**
```yaml
face_recognition:
  api_host: localhost
  api_port: 8080
  ha_api_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjNTg3ZTVhYWQ1NTM0Y2U2YTAzZmUzNDk2NDQ5ZDczMiIsImlhdCI6MTc2Nzc4MjU5MSwiZXhwIjoyMDgzMTQyNTkxfQ.wd-28qDCW0cr-U7CGrM6cIIP-hB0C8eKfmGumybePlI"
```

### 6. Test

**After deployment:**

1. **Check add-on logs** - Should see server starting
2. **Test status endpoint:**
   - Browser: `http://homeassistant.local:8080/status`
   - Should return: `{"status": "ready", "version": "0.0.1", "chunk": "3"}`
   
3. **Trigger a Nest event** (or use the service):
   - Developer Tools → Services
   - Service: `face_recognition.fire_nest_event`
   - Or trigger a real Nest event
   
4. **Check logs** - Should see:
   - "NEST EVENT RECEIVED"
   - "Fetching Nest image from HA API"
   - "Successfully fetched Nest image via API"
   - "POST /event received" (in add-on logs)
   - "Successfully sent Nest event to add-on"

## Quick Checklist

- [ ] Files copied to local repo
- [ ] Changes committed to Git
- [ ] Pushed to GitHub
- [ ] Add-on uninstalled and reinstalled
- [ ] Integration files copied to `/config/custom_components/face_recognition/`
- [ ] Home Assistant restarted
- [ ] `configuration.yaml` updated with `ha_api_token`
- [ ] Add-on started and running
- [ ] Tested `/status` endpoint
- [ ] Tested Nest event trigger

## Troubleshooting

**If add-on doesn't rebuild:**
- Make sure you pushed to GitHub
- Try refreshing the repository in HA (Settings → Add-ons → Add-on Store → ⋮ → Repositories → Refresh)

**If integration doesn't load:**
- Check file permissions in `/config/custom_components/face_recognition/`
- Verify all files are copied (check file sizes match)
- Check Home Assistant logs for import errors

**If POST requests still fail:**
- Check add-on logs for "POST /event received"
- Verify add-on is running (Status should be "Running")
- Test with curl: `curl -X POST http://localhost:8080/event -H "Content-Type: application/json" -d '{"event_type":"nest_event","test":true}'`

