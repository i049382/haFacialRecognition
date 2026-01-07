# Diagnose POST Request Failure

## Current Status
- ✅ GET requests work (`/status` endpoint)
- ❌ POST requests fail ("Connection reset by peer")
- ❌ Request not reaching Flask (no "Incoming request" log)

## Critical: Check Add-on Logs

**Please check the add-on logs when you trigger a Nest event.** Look for:

1. **"Incoming request: POST /event"** - If this appears, request reached Flask ✅
2. **"POST /event received"** - If this appears, route handler executed ✅
3. **Any gunicorn errors** - Worker crashes, timeouts, etc.
4. **Access logs** - Should show the POST request attempt

## Possible Causes

### 1. Gunicorn Rejecting POST Requests
- Gunicorn might be configured to reject POST requests
- Check gunicorn worker logs for errors
- Check if there's a size limit being exceeded

### 2. Network/Firewall Issue
- POST requests might be blocked
- Check if `localhost:8080` resolves correctly
- Try using `127.0.0.1:8080` instead

### 3. Request Format Issue
- Gunicorn might not like how aiohttp sends POST requests
- Check request headers and format

## Next Steps

### Step 1: Check Add-on Logs
When you trigger a Nest event, immediately check add-on logs for:
- Any errors or warnings
- "Incoming request" messages
- Gunicorn worker status

### Step 2: Test with curl (if you have SSH access)
```bash
# Test POST request directly
curl -X POST http://localhost:8080/event \
  -H "Content-Type: application/json" \
  -d '{"event_type":"nest_event","test":true}'
```

### Step 3: Try Different URL
In `configuration.yaml`, try:
```yaml
face_recognition:
  api_host: 127.0.0.1  # Instead of localhost
  api_port: 8080
```

### Step 4: Check Gunicorn Configuration
The issue might be in how gunicorn handles POST requests. We may need to:
- Use a different worker class
- Adjust timeout settings
- Check for request size limits

## What We Need

**Please provide:**
1. Add-on logs when triggering a Nest event
2. Any gunicorn errors or warnings
3. Whether "Incoming request" appears in logs

This will help us determine if:
- Request reaches Flask (good - issue is in Flask)
- Request doesn't reach Flask (bad - issue is gunicorn/network)

