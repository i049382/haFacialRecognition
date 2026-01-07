# Debug Status Endpoint Issue

## Current Problem
- Add-on starts but status endpoint doesn't work
- Logs show Flask is running on `0.0.0.0:8080`
- But accessing `http://homeassistant.local:8080/status` fails

## Possible Causes

### 1. Port Not Exposed Correctly
Check `config.yaml` has:
```yaml
ports:
  8080/tcp: 8080
```

### 2. Flask Not Actually Listening
The logs show Flask starting, but it might be crashing or not binding correctly.

### 3. Network Access Issue
- Try accessing from inside HA container: `http://localhost:8080/status`
- Try accessing from host: `http://127.0.0.1:8080/status`
- Try accessing from network: `http://homeassistant.local:8080/status`

### 4. Code Issue - Routes Not Registered
The routes might not be registered correctly.

## Debug Steps

### Step 1: Check Add-on Logs for Errors
Look for:
- Any exceptions after Flask starts
- Any errors about routes
- Any connection errors

### Step 2: Test from Inside Container (if possible)
If you have SSH access to HA:
```bash
# Get into add-on container
docker exec -it <addon_container_id> sh

# Test status endpoint
curl http://localhost:8080/status
```

### Step 3: Check if Flask is Actually Listening
Look for this in logs:
```
* Running on http://127.0.0.1:8080
* Running on http://172.30.33.3:8080
```

### Step 4: Test with curl from Host
If you can SSH into HA host:
```bash
curl http://localhost:8080/status
```

### Step 5: Check Network Configuration
- Verify add-on network mode
- Check if port mapping is correct
- Verify firewall rules

## Quick Fix to Try

Add more logging to see what's happening:

1. Add logging to status endpoint
2. Add logging when Flask starts
3. Add error handling for route registration

## Expected Behavior

When accessing `http://homeassistant.local:8080/status`:
- Should return: `{"status": "ready", "version": "0.0.1", "chunk": "3"}`
- Status code: 200
- Content-Type: application/json

