# Steps to Rebuild Add-on with Chunk 2 Code

## Problem
The add-on is still running Chunk 0 code (old code). Logs show:
```
Add-on ready (Chunk 0 - Configuration only)
Waiting for future functionality... (Chunk 2+)
```

But it should show:
```
Add-on ready (Chunk 2 - IPC & Event Plumbing)
HTTP API server starting on port 8080
```

## Solution: Force HA to Rebuild

### Step 1: Push Latest Code to GitHub ✅
```bash
git push
```
(Make sure all Chunk 2 files are pushed)

### Step 2: Force HA to Refresh Repository

**Option A: Refresh Repository**
1. Go to **Settings → Add-ons → Add-on Store**
2. Click **⋮** (three dots) → **Repositories**
3. Find your repository
4. Click **⋮** next to it → **Reload** (or **Remove** then **Add** again)

**Option B: Update Add-on**
1. Go to **Settings → Add-ons → Face Recognition**
2. If you see an **Update** button, click it
3. If not, proceed to Step 3

### Step 3: Rebuild Add-on (Required!)

**Important:** Simply restarting won't work - you must rebuild!

1. Go to **Settings → Add-ons → Face Recognition**
2. Click **Uninstall** (this removes the old container)
3. Wait for uninstall to complete
4. Click **Install** (this rebuilds with new code from GitHub)
5. Wait for installation (may take 1-2 minutes)
6. Click **Start**

### Step 4: Verify New Code is Running

Check the **Logs** tab. You should see:
```
Starting Face Recognition Add-on
Configuration loaded successfully
Add-on ready (Chunk 2 - IPC & Event Plumbing)
HTTP API server starting on port 8080
```

If you still see "Chunk 0" messages, the rebuild didn't work. Try:
- Check GitHub - are the files actually there?
- Remove repository and re-add it
- Check HA Supervisor logs for errors

### Step 5: Test API

Once logs show "HTTP API server starting on port 8080":
- Try: `http://homeassistant.local:8080/status`
- Or: `http://YOUR_HA_IP:8080/status`

Should return:
```json
{
  "status": "ready",
  "version": "0.0.1",
  "chunk": "2"
}
```

## Why Rebuild is Needed

Docker containers are immutable - once built, they don't change. To get new code:
- ❌ **Restart** = Uses same container (old code)
- ✅ **Uninstall + Install** = Builds new container (new code)

---

**After rebuilding, the API should be accessible!**
