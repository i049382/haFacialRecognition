# Fix Server Disconnected Error

## Problem
POST requests are failing with "Server disconnected":
```
aiohttp.client_exceptions.ServerDisconnectedError: Server disconnected
```

The request is not reaching Flask (no "POST /event received" in add-on logs).

## Root Cause Analysis
Gunicorn is closing the connection before Flask can process the request. Possible causes:
1. Gunicorn worker timing out or crashing
2. HTTP/1.1 keepalive issue
3. Request not being properly handled by gunicorn
4. Connection pool issue

## Fixes Applied

### 1. Added Flask before_request Hook
- Logs all incoming requests before they're processed
- Helps diagnose if requests reach Flask
- Logs request method, path, headers, content-type, content-length

### 2. Updated Gunicorn Configuration
- Added `max_requests: 0` - No limit on requests per worker
- Added `worker_connections: 1000` - Allow more concurrent connections
- Ensures gunicorn doesn't close connections prematurely

### 3. Updated aiohttp Request Configuration
- Added `allow_redirects=False` - Prevents redirect issues
- Added explicit timeout configuration
- Ensures proper connection handling

## Next Steps

### 1. Commit and Push Changes
```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition
git add integration/nest_listener.py
git add face_recognition/face_recognition/face_recognition_addon/api.py
git add face_recognition/face_recognition/face_recognition_addon/__main__.py
git commit -m "Fix: Add before_request hook and improve gunicorn/aiohttp configuration"
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

### 5. Test and Check Logs
1. Trigger your doorbell camera
2. Check add-on logs for:
   - "Incoming request: POST /event" (from before_request hook)
   - "POST /event received" (from route handler)
   - Request headers and content info
3. Check HA logs for:
   - "Response status: 200" (if successful)
   - Any error messages

## Expected Behavior

**After fix:**
- before_request hook should log all incoming requests
- Request should reach Flask and be processed
- Response should be returned successfully
- No server disconnect errors

**If still failing:**
- Check if "Incoming request" appears in add-on logs
- If yes: Request reaches Flask, issue is in processing
- If no: Request doesn't reach Flask, issue is gunicorn/network

## Debugging Tips

**Check add-on logs for:**
1. "Incoming request: POST /event" - Request reached Flask
2. "POST /event received" - Route handler executed
3. Request headers - Verify Content-Type is correct
4. Any exceptions or errors

**If "Incoming request" appears but "POST /event received" doesn't:**
- Issue is in route registration or request processing
- Check for exceptions in Flask

**If neither appears:**
- Request isn't reaching Flask
- Issue is in gunicorn or network
- Check gunicorn worker logs for errors

## Alternative Solutions

If the issue persists, we may need to:
1. Try gevent workers instead of sync
2. Use Flask's built-in server instead of gunicorn (for testing)
3. Check if there's a compatibility issue between aiohttp and gunicorn
4. Consider using a different HTTP client library

