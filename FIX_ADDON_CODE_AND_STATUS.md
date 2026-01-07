# Fix Add-on Code and Status Endpoint

## Problem Summary
1. **Add-on running old code** - Missing "Checking for Gunicorn availability..." log
2. **Status endpoint not working** - Can't access `http://homeassistant.local:8080/status`

## Root Cause
The add-on is running code from an older commit, not the latest code from GitHub.

## Solution Steps

### Step 1: Commit and Push Latest Code

**I've added debug logging to help diagnose the status endpoint issue.**

```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition

# Check what needs to be committed
git status

# Add the changes
git add face_recognition/face_recognition/face_recognition_addon/api.py

# Commit with descriptive message
git commit -m "Add debug logging to status endpoint and route registration"

# Push to GitHub
git push
```

**Or using GitHub Desktop:**
1. Open GitHub Desktop
2. You should see `api.py` as modified
3. Commit message: `Add debug logging to status endpoint and route registration`
4. Click **Commit to main**
5. Click **Push origin**

### Step 2: Force Complete Rebuild

**IMPORTANT:** You need to completely remove the add-on and rebuild:

1. **Stop the add-on:**
   - Settings → Add-ons → Face Recognition → **Stop**

2. **Uninstall the add-on:**
   - Settings → Add-ons → Face Recognition → **Uninstall**
   - Wait for uninstall to complete

3. **Clear Docker cache (if possible):**
   - If you have SSH access, run: `docker system prune -f`
   - This ensures Docker pulls fresh code

4. **Refresh the repository:**
   - Settings → Add-ons → Add-on Store
   - Click **⋮** (three dots) → **Repositories**
   - Click your repository → **Refresh**
   - Wait for refresh to complete

5. **Reinstall the add-on:**
   - Settings → Add-ons → Face Recognition → **Install**
   - Wait 3-5 minutes for installation
   - **DO NOT START YET**

6. **Verify code was pulled:**
   - Check the add-on version/build date
   - Should match your latest commit

7. **Start the add-on:**
   - Settings → Add-ons → Face Recognition → **Start**

### Step 3: Verify New Code is Running

**Check logs - you should see:**

```
[INFO] __main__: Starting Face Recognition Add-on
[INFO] __main__: Configuration loaded successfully
[INFO] __main__: Add-on ready (Chunk 3 - Nest Event Ingestion)
[INFO] __main__: HTTP API server starting on port 8080
[INFO] __main__: Checking for Gunicorn availability...  <-- THIS LINE MUST APPEAR
```

**If you see "Checking for Gunicorn availability..." then new code is running!**

**Then either:**
- `[INFO] __main__: Gunicorn found! Attempting to start...`
- OR `[WARNING] __main__: Gunicorn not available: ...`
- Followed by `[INFO] face_recognition_addon.api: Registering API routes...`
- Followed by `[INFO] face_recognition_addon.api: API routes registered successfully`

### Step 4: Test Status Endpoint

**After add-on starts, test the status endpoint:**

1. **From browser:**
   - Go to: `http://homeassistant.local:8080/status`
   - Should return: `{"status": "ready", "version": "0.0.1", "chunk": "3"}`

2. **Check logs when accessing:**
   - You should see: `[INFO] face_recognition_addon.api: GET /status endpoint called`
   - Followed by: `[INFO] face_recognition_addon.api: Returning status response: {...}`

3. **If it still doesn't work:**
   - Check add-on logs for errors
   - Try accessing from inside HA: `http://localhost:8080/status`
   - Check if port 8080 is actually exposed

### Step 5: Troubleshooting

**If logs still don't show "Checking for Gunicorn availability...":**

1. **Verify code is on GitHub:**
   - Go to: `https://github.com/i049382/haFacialRecognition`
   - Check `face_recognition/face_recognition/face_recognition_addon/__main__.py`
   - Verify line 38 exists: `logger.info("Checking for Gunicorn availability...")`

2. **Check which commit is being used:**
   - In HA, check add-on logs for any version/build info
   - Compare with your latest commit hash

3. **Try removing and re-adding repository:**
   - Settings → Add-ons → Add-on Store → Repositories
   - Remove your repository
   - Re-add it: `https://github.com/i049382/haFacialRecognition`
   - Refresh and reinstall

**If status endpoint still doesn't work:**

1. **Check Flask is actually listening:**
   - Logs should show: `* Running on http://127.0.0.1:8080`
   - If not, Flask might not be starting correctly

2. **Check port mapping:**
   - Verify `config.yaml` has: `ports: 8080/tcp: 8080`
   - Check add-on network settings

3. **Test from different locations:**
   - From browser: `http://homeassistant.local:8080/status`
   - From HA container (if SSH): `curl http://localhost:8080/status`
   - From host (if SSH): `curl http://127.0.0.1:8080/status`

4. **Check for errors in logs:**
   - Look for any exceptions when accessing `/status`
   - Look for route registration errors
   - Look for Flask startup errors

## Expected Final State

**After successful deployment:**

1. **Logs show:**
   ```
   [INFO] __main__: Checking for Gunicorn availability...
   [INFO] face_recognition_addon.api: Registering API routes...
   [INFO] face_recognition_addon.api: API routes registered successfully
   ```

2. **Status endpoint works:**
   - `http://homeassistant.local:8080/status` returns JSON
   - Logs show "GET /status endpoint called" when accessed

3. **Add-on is stable:**
   - No connection reset errors
   - POST requests work reliably

## Quick Checklist

- [ ] Code committed and pushed to GitHub
- [ ] Repository refreshed in HA
- [ ] Add-on uninstalled completely
- [ ] Add-on reinstalled (waited 3-5 minutes)
- [ ] Add-on started
- [ ] Logs show "Checking for Gunicorn availability..."
- [ ] Logs show "Registering API routes..."
- [ ] Status endpoint accessible from browser
- [ ] Status endpoint logs show "GET /status endpoint called"

