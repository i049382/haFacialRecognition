# Fix Gunicorn Worker Timeout

## Problem
Gunicorn starts successfully and the status endpoint works, but there's a worker timeout:
```
[2026-01-07 14:34:35 +0000] [79] [CRITICAL] WORKER TIMEOUT (pid:80)
[2026-01-07 14:34:35 +0000] [80] [INFO] Worker exiting (pid: 80)
```

## Root Cause
The gunicorn timeout is set to 30 seconds, which is too short. The worker times out even when idle or during request processing.

## Solution
I've updated the gunicorn configuration to:
- Increase timeout from 30 to 120 seconds
- Increase keepalive from 5 to 30 seconds
- Set `preload_app: False` to avoid initialization issues
- Add `graceful_timeout: 30` for graceful shutdowns

## Next Steps

### 1. Commit and Push Changes
```bash
cd C:\Users\ismet\Documents\Github\haFacialRecognition
git add face_recognition/face_recognition/face_recognition_addon/__main__.py
git commit -m "Fix: Increase gunicorn timeout to prevent worker timeouts"
git push
```

### 2. Restart Add-on
1. Settings → Add-ons → Face Recognition → **Restart**
2. Wait for restart to complete
3. Check logs - should see gunicorn starting without timeout errors

### 3. Verify Fix
After restart, monitor logs for:
- ✅ Gunicorn starts successfully
- ✅ Status endpoint works
- ✅ No worker timeout errors
- ✅ Worker stays alive during requests

## Expected Behavior

**Before fix:**
- Worker times out after 30 seconds
- Worker exits and restarts
- Potential request failures during timeout

**After fix:**
- Worker stays alive
- No timeout errors
- Stable request handling

## Additional Notes

The timeout was increased to 120 seconds to handle:
- Long-running requests (like image processing)
- Network delays
- System load spikes

If you still see timeouts after this fix, we may need to:
1. Investigate blocking operations in the Flask app
2. Consider async workers instead of sync
3. Add request timeout handling

