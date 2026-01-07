# Testing the API Fetch Approach

## What We've Changed

1. **Modified `nest_listener.py`** to try API fetch first, then fallback to filesystem
2. **Added debug logging** to `__init__.py` to see if configuration is being read
3. **Improved error handling** for 401 (authentication) errors

## Expected Behavior

When a Nest event fires:

1. **Try API fetch first** (with HA API token)
   - If token is configured and URL hasn't expired: ✅ Success (fastest)
   - If 401 error: Log warning, fallback to filesystem
   - If 404 error: URL expired, fallback to filesystem
   - If timeout: Fallback to filesystem

2. **Fallback to filesystem** (if API fails)
   - Extract frame from MP4 video
   - Always works (files don't expire)
   - Slower but reliable

## Steps to Test

### 1. Update Your Configuration

Edit `/config/configuration.yaml` (main HA config file):
```yaml
face_recognition:
  api_host: "localhost"
  api_port: 8080
  api_token: ""  # Optional
  ha_api_token: "YOUR_LONG_LIVED_ACCESS_TOKEN_HERE"  # REQUIRED
```

### 2. Update the Integration Files

Copy these files to your HA `custom_components/face_recognition/`:
- `integration/__init__.py` (with debug logging)
- `integration/nest_listener.py` (with API-first approach)

### 3. Restart Home Assistant

Full restart (not just reload):
```bash
# In HA Supervisor
Configuration → System → Restart
```

### 4. Check Logs

Look for these log messages:

**On startup:**
```
=== DEBUG: Full config received ===
Config keys: ['face_recognition', ...]
Face recognition config in config: True

=== DEBUG: Integration config from YAML ===
Config keys: ['api_host', 'api_port', 'api_token', 'ha_api_token']
HA API token present: True
HA API token length: 123  # Should be > 0
HA API token configured for internal API calls
```

**When Nest event fires:**
```
Trying API thumbnail fetch: /api/nest/event_media/.../thumbnail
Fetching Nest image from HA API: http://127.0.0.1:8123/api/nest/event_media/.../thumbnail
Using HA API token for authentication
Successfully fetched Nest image via API (12345 bytes)  # If successful
```

**If API fails:**
```
Authentication failed (401) - check HA API token configuration  # If token wrong
Nest media expired or not found (404)  # If URL expired
API fetch failed or no image URL, trying filesystem extraction  # Fallback
Successfully extracted frame using ffmpeg (12345 bytes)  # Filesystem success
```

## Common Issues

### 1. "No HA API token configured"
- Token not in configuration.yaml
- Wrong YAML indentation
- Configuration not reloaded

### 2. "Authentication failed (401)"
- Token is incorrect/expired
- Token doesn't have required permissions
- Token format wrong

### 3. "Nest media expired or not found (404)"
- Normal! URLs expire quickly
- System will fallback to filesystem
- This is expected behavior

### 4. No API attempt at all
- Old code still running
- Integration not updated
- Need full HA restart

## Success Criteria

The system is working correctly if:

1. ✅ API fetch is attempted (with token)
2. ✅ Either API succeeds OR falls back to filesystem
3. ✅ Image is successfully obtained (one way or another)
4. ✅ Image is sent to add-on for processing

## Performance Comparison

### API Fetch (When it works):
- **Speed**: < 1 second
- **CPU**: Very low (HTTP request only)
- **Success rate**: Depends on how fast you fetch

### Filesystem Fallback:
- **Speed**: 1-3 seconds (frame extraction)
- **CPU**: Moderate (ffmpeg/OpenCV)
- **Success rate**: 100% (files don't expire)

## Recommendation

Even with the API fetch, **keep the filesystem fallback**. It ensures 100% reliability. The API fetch gives you a speed boost when it works, but the filesystem ensures it always works.