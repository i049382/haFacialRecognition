# Fix Connection Reset Error

## Problem
POST requests to add-on are failing with "Connection reset by peer":
```
aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer
```

## Root Cause Analysis
The connection is being reset before the request completes. Possible causes:
1. Gunicorn closing connection prematurely
2. Request timeout too short
3. Missing Content-Type header
4. Network connectivity issue between HA and add-on

## Fixes Applied

### 1. Added Explicit Content-Type Header
- Set `Content-Type: application/json` explicitly in request headers
- Ensures Flask/gunicorn recognizes the request as JSON

### 2. Increased Request Timeout
- Changed from `timeout=30` to `timeout=aiohttp.ClientTimeout(total=60, connect=10)`
- Gives more time for request to complete

### 3. Added More Logging
- Log request URL, headers, and payload size
- Log request headers on add-on side
- Helps diagnose what's happening

### 4. Updated Gunicorn Configuration
- Added request size limits (defaults)
- Ensures gunicorn can handle the request

## Next Steps

### 1. Commit and Push Changes
```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition
git add integration/nest_listener.py
git add face_recognition/face_recognition/face_recognition_addon/api.py
git add face_recognition/face_recognition/face_recognition_addon/__main__.py
git commit -m "Fix: Add explicit Content-Type header and increase timeout for POST requests"
git push
```

### 2. Update Integration in HA
Copy the updated `nest_listener.py` to:
- `/config/custom_components/face_recognition/nest_listener.py`

### 3. Restart Add-on
- Settings → Add-ons → Face Recognition → Restart
- Wait for restart

### 4. Restart Home Assistant
- Settings → System → Restart
- Or Developer Tools → YAML → Restart

### 5. Test Again
1. Trigger your doorbell camera
2. Check HA logs for:
   - "Making POST request to http://localhost:8080/event"
   - Request headers and payload size
3. Check add-on logs for:
   - "POST /event received"
   - Request headers
   - "Received event data"

## Expected Behavior

**After fix:**
- Request includes explicit Content-Type header
- Longer timeout allows request to complete
- More logging helps diagnose issues
- Connection should not reset

**If still failing:**
- Check add-on logs to see if request reaches Flask
- Verify network connectivity (status endpoint works, so this should be fine)
- Check if payload size is causing issues
- Consider if gunicorn needs different worker configuration

## Debugging Tips

**If connection still resets:**
1. Check add-on logs - does "POST /event received" appear?
2. If yes: Request reaches Flask, issue is in processing
3. If no: Request doesn't reach Flask, issue is network/gunicorn

**Check network:**
- Status endpoint works, so network should be fine
- But verify `localhost:8080` resolves correctly from HA

**Check payload:**
- Current payload is small (just metadata, no image)
- Should not cause size issues

