# Fix Status Page Issue

## Problem
1. Add-on is running old code (missing "Checking for Gunicorn availability..." log)
2. Status page doesn't work
3. Code changes not reflected in running add-on

## Solution

### Step 1: Verify Code is Updated Locally

Check that these files have the latest code:

**`face_recognition/face_recognition/face_recognition_addon/__main__.py`**
- Should have line 38: `logger.info("Checking for Gunicorn availability...")`
- Should have gunicorn import and fallback logic

**`face_recognition/face_recognition/face_recognition_addon/api.py`**
- Should have `run()` method with `threaded` and `use_reloader` parameters

### Step 2: Commit and Push to GitHub

**Using GitHub Desktop:**
1. Open GitHub Desktop
2. Review all changed files
3. Commit message:
   ```
   Fix: Update API run() signature and ensure gunicorn check runs
   ```
4. Click **Commit to main**
5. Click **Push origin**

**Using Command Line:**
```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition
git add .
git commit -m "Fix: Update API run() signature and ensure gunicorn check runs"
git push
```

### Step 3: Force Rebuild Add-on

**IMPORTANT:** You must completely remove and reinstall to force rebuild:

1. **Go to:** Settings → Add-ons → Face Recognition
2. **Click:** **Stop** (if running)
3. **Click:** **Uninstall** (removes container and image)
4. **Wait** for uninstall to complete
5. **Go to:** Settings → Add-ons → Add-on Store
6. **Click:** **⋮** (three dots) → **Repositories**
7. **Click:** Your repository → **Refresh** (forces HA to pull latest code)
8. **Go back to:** Settings → Add-ons → Face Recognition
9. **Click:** **Install** (rebuilds from GitHub)
10. **Wait** for installation (2-3 minutes)
11. **Click:** **Start**

### Step 4: Verify Logs Show New Code

After starting, check logs. You should see:

```
[INFO] __main__: Starting Face Recognition Add-on
[INFO] __main__: Configuration loaded successfully
[INFO] __main__: Add-on ready (Chunk 3 - Nest Event Ingestion)
[INFO] __main__: HTTP API server starting on port 8080
[INFO] __main__: Checking for Gunicorn availability...
```

**Then either:**
- `[INFO] __main__: Gunicorn found! Attempting to start...`
- OR `[WARNING] __main__: Gunicorn not available: ...`

### Step 5: Test Status Endpoint

**From Home Assistant:**
- Browser: `http://homeassistant.local:8080/status`
- Should return: `{"status": "ready", "version": "0.0.1", "chunk": "3"}`

**From command line (if you have SSH access):**
```bash
curl http://localhost:8080/status
```

**Expected response:**
```json
{
  "status": "ready",
  "version": "0.0.1",
  "chunk": "3"
}
```

## Troubleshooting

**If logs still don't show "Checking for Gunicorn availability...":**
- The add-on is still running old code
- Make sure you **refreshed the repository** before installing
- Try removing the repository and re-adding it
- Check GitHub to verify your latest commit is there

**If status page still doesn't work:**
- Check add-on logs for errors
- Verify port 8080 is exposed in `config.yaml`
- Try accessing from inside the container (if possible)
- Check if Flask is actually listening: Look for `Running on http://127.0.0.1:8080` in logs

**If you see "Connection refused" or "Site can't be reached":**
- Add-on might not be running
- Port might not be exposed
- Check `config.yaml` has: `ports: 8080/tcp: 8080`

## Quick Verification Commands

**Check if add-on is running:**
- Settings → Add-ons → Face Recognition → Check status is "Running"

**Check logs:**
- Settings → Add-ons → Face Recognition → Logs
- Look for the startup sequence

**Test from HA container (if you have SSH):**
```bash
curl http://localhost:8080/status
```

