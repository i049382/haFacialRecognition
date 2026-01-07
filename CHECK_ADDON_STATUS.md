# Quick Add-on Status Check

Since it's -1°C outside, here's what to do QUICKLY:

## 1. Check Add-on is Running
- Go to HA Supervisor → Add-ons
- Find "Face Recognition" add-on
- Is it **STARTED**? If not, start it!
- Check logs for errors

## 2. Test Add-on Connection
From HA container (use Terminal add-on or SSH):
```bash
# Test if add-on is responding
curl http://localhost:8080/status

# Expected response:
# {"status": "ready", "version": "0.0.1", "chunk": "3"}
```

## 3. Check Add-on Logs
Look for:
- "Starting Flask dev server on 0.0.0.0:8080" (should appear)
- Any errors about port 8080 already in use
- Gunicorn errors (should be disabled now)

## 4. Quick Fixes if Add-on Won't Start

### A. Port Conflict
If port 8080 is already used:
1. Edit add-on configuration in HA UI
2. Change `api_port` to something else (e.g., 8081)
3. Update integration config to match
4. Restart add-on

### B. Update Add-on Files
Make sure you have the **latest files**:
1. Copy updated `__main__.py` (with Gunicorn disabled)
2. Copy updated `api.py`
3. Restart add-on

## 5. What We've Fixed So Far

✅ **API fetch works** - You're getting Nest images!
✅ **HA token works** - No more 401 errors!
✅ **Local save fallback** - Images saved if add-on fails
❌ **Add-on connection** - Needs fixing

## 6. Immediate Workflow

Even with add-down down, you'll now get:
1. Nest event → API fetch (works!)
2. If add-on fails → Save image locally
3. Images saved to: `/config/face_recognition/saved_images/`

## 7. Next Test

Go outside once more (quickly!):
1. Trigger camera
2. Check logs for:
   - "Successfully fetched Nest image via API"
   - "Saved image locally due to connection_error"
   - Check `/config/face_recognition/saved_images/` for your image

## 8. If Still Stuck

Temporarily simplify - modify `_send_to_addon` to **always save locally**:
```python
# In nest_listener.py, comment out the POST request and just save:
await self._save_image_locally(event_data, image_data, "debug")
```

This way you at least capture images while we fix the add-on!