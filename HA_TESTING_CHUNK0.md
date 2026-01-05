# Testing Chunk 0 in Home Assistant

## Is It Worth Testing Now?

### ✅ **YES, but with caveats:**

**Benefits:**
- ✅ Validates add-on structure is correct
- ✅ Ensures HA can install and start the add-on
- ✅ Catches HA-specific integration issues early
- ✅ Validates `config.yaml` schema works in HA UI
- ✅ Tests configuration loading from HA's options.json

**Limitations:**
- ⚠️ Limited functionality (just config loading)
- ⚠️ Add-on will run but do nothing (waiting for Chunk 2)
- ⚠️ Requires HA setup

**Recommendation:** 
- **Optional but beneficial** - catches HA-specific issues early
- **Minimum viable test:** Verify add-on installs, starts, and loads config without errors
- **Full testing:** Better after Chunk 2 when we have HTTP API to test

## What You Can Test Now

### ✅ Basic Installation Test
1. Add-on installs without errors
2. Add-on starts successfully
3. Configuration loads from HA UI
4. Logs show "Configuration loaded successfully"
5. Add-on stays running (doesn't crash)

### ❌ What You Can't Test Yet
- HTTP API (Chunk 2)
- Event firing (Chunk 2)
- Face detection (Chunk 5+)
- Any actual functionality

## Setup Instructions

### 1. Prepare Add-on for HA

The add-on is already set up, but you need to:

1. **Copy add-on to HA:**
   ```bash
   # On your HA system (or via Samba/SSH)
   cp -r addon /config/addons/face_recognition
   ```

2. **Or use local add-on repository:**
   - Create a repository structure:
   ```
   haFacialRecognition/
   ├── face_recognition/
   │   └── face_recognition/
   │       ├── config.yaml
   │       ├── Dockerfile
   │       ├── run.sh
   │       ├── requirements.txt
   │       └── face_recognition_addon/
   ```

### 2. Install in Home Assistant

1. **If using local add-on:**
   - Go to **Settings → Add-ons → Add-on Store**
   - Click **⋮ (three dots)** → **Repositories**
   - Add your local path or GitHub repo URL
   - Refresh

2. **Install add-on:**
   - Find "Face Recognition" in add-on store
   - Click **Install**
   - Wait for installation to complete

3. **Configure add-on:**
   - Click **Configuration** tab
   - Set values:
     ```yaml
     confidence_threshold: 0.80
     review_threshold: 0.65
     camera_paths: []
     enable_daily_poll: false
     daily_poll_time: "02:00"
     drive_folder_id: ""
     api_port: 8080
     api_token: "test_token_123"
     ```

4. **Start add-on:**
   - Click **Start**
   - Check logs

### 3. Verify Success

**✅ Success indicators:**
- Add-on status: **Running**
- Logs show:
  ```
  Starting Face Recognition Add-on
  Configuration loaded successfully
  Add-on ready (Chunk 0 - Configuration only)
  Waiting for future functionality... (Chunk 2+)
  ```
- No error messages

**❌ Failure indicators:**
- Add-on status: **Stopped** or **Error**
- Logs show configuration errors
- Add-on crashes immediately

### 4. Test Configuration Changes

1. **Change threshold values:**
   - Edit configuration in HA UI
   - Set `review_threshold` >= `confidence_threshold`
   - Click **Save**
   - Try to start add-on
   - **Expected:** Add-on fails to start with validation error

2. **Test missing config:**
   - Clear all configuration
   - **Expected:** Uses defaults, starts successfully

3. **Test invalid time:**
   - Set `daily_poll_time: "25:00"`
   - **Expected:** Validation error

## Expected Behavior

### Current State (Chunk 0)
- ✅ Add-on installs
- ✅ Add-on starts
- ✅ Configuration loads
- ✅ Add-on stays running (sleeps, waiting for Chunk 2)
- ⚠️ No HTTP API yet
- ⚠️ No functionality yet

### After Chunk 2
- ✅ HTTP API available
- ✅ Can test `GET /status` endpoint
- ✅ Can test `POST /event` endpoint
- ✅ Integration can communicate with add-on

## Troubleshooting

### Add-on Won't Install
- Check `config.yaml` syntax
- Verify Dockerfile is correct
- Check HA logs for errors

### Add-on Crashes Immediately
- Check configuration values
- Verify `options.json` format
- Check logs for validation errors

### Configuration Not Loading
- Verify `options.json` exists in `/data/`
- Check file permissions
- Verify JSON format is valid

## Recommendation

**For Chunk 0:**
- ✅ **Quick test:** Install and verify it starts (5 minutes)
- ⚠️ **Full test:** Wait until Chunk 2 for meaningful testing

**For Chunk 2:**
- ✅ **Full test:** Test HTTP API, event firing, integration communication

## Next Steps

1. **If testing now:** Follow setup instructions above
2. **If waiting:** Proceed to Chunk 2, then test everything together

---

**Bottom line:** Testing in HA now is **optional but safe** - it validates the add-on structure works. Full functionality testing should wait until Chunk 2.
