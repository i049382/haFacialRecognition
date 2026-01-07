# Fix POST Request Issue with Gunicorn

## Problem
- ✅ GET requests work (`/status` endpoint)
- ❌ POST requests fail ("Connection reset by peer")
- ❌ No "Incoming request: POST /event" in add-on logs
- **Conclusion**: Gunicorn is resetting POST connections before Flask sees them

## Root Cause
Gunicorn is accepting GET requests but rejecting/resetting POST requests. This could be:
1. Request body size limits
2. Content-Length header handling
3. HTTP/1.1 keepalive issues
4. How aiohttp sends POST vs how gunicorn expects it

## Fixes Applied

### 1. Added Request Body Limit
```python
'limit_request_body': 10485760,  # 10MB limit for POST requests
```
- Ensures gunicorn can handle POST request bodies
- Default might be too small or undefined

### 2. Changed Request Encoding
```python
# Before: json=payload (aiohttp auto-encodes)
# After: data=json.dumps(payload) (explicit encoding)
```
- Some servers prefer explicit JSON encoding
- Better compatibility with gunicorn

### 3. Added Forwarded Headers Support
```python
'forwarded_allow_ips': '*',  # Allow forwarded headers
```
- Allows HA proxy headers if present

### 4. Increased Logging
```python
'loglevel': 'debug',  # See more details
```
- Will show POST requests in access logs
- Helps diagnose connection issues

## Next Steps

1. **Deploy changes**
   - Commit and push updated code
   - Restart add-on
   - Restart HA integration

2. **Test POST request**
   - Trigger Nest event
   - Check add-on logs for:
     - "Incoming request: POST /event" ← Should appear now
     - Access log entries showing POST requests
     - Any gunicorn errors

3. **If still failing**
   - Check gunicorn access logs for POST attempts
   - Try curl test: `curl -X POST http://localhost:8080/event -H "Content-Type: application/json" -d '{"test":true}'`
   - Consider switching to Flask dev server temporarily to test

## Expected Behavior After Fix

**Add-on logs should show:**
```
[INFO] face_recognition_addon.api: Incoming request: POST /event
[INFO] face_recognition_addon.api: POST /event received
[INFO] face_recognition_addon.api: Received event data: [...]
```

**HA logs should show:**
```
[INFO] Response received: status=200
[INFO] Successfully sent Nest event to add-on
```

## Alternative: Test with Flask Dev Server

If gunicorn still fails, we can temporarily use Flask dev server to verify:
- Change `use_gunicorn = False` in `__main__.py`
- Test if POST works with Flask
- If yes, issue is gunicorn-specific
- If no, issue is elsewhere

