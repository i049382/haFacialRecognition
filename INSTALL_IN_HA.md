# Install Face Recognition Add-on in Home Assistant

## Step-by-Step Installation Guide

### Step 1: Get Your GitHub Repository URL

Your repository URL should be:
```
https://github.com/YOUR_USERNAME/haFacialRecognition
```
(Replace `YOUR_USERNAME` with your actual GitHub username)

**To find it:**
- Go to your GitHub repository page
- Click the green **"Code"** button
- Copy the HTTPS URL (should look like above)

---

### Step 2: Add Repository to Home Assistant

1. **Open Home Assistant**
2. **Go to:** Settings → Add-ons → Add-on Store
3. **Click:** ⋮ (three dots) in the top right corner
4. **Select:** **Repositories**
5. **Click:** **Add** button
6. **Paste your repository URL:**
   ```
   https://github.com/YOUR_USERNAME/haFacialRecognition
   ```
7. **Click:** **Add**
8. **Wait:** A few seconds for repository to refresh

---

### Step 3: Find and Install the Add-on

1. **Scroll down** in the Add-on Store
2. **Look for:** "Face Recognition" add-on
   - Should appear under your repository name
   - May show a default add-on icon
   - Description: "Personal face recognition system for Home Assistant"
3. **Click** on "Face Recognition" add-on
4. **Click:** **Install** button
5. **Wait:** Installation may take 1-2 minutes
   - You'll see progress: "Downloading...", "Building...", "Installing..."

---

### Step 4: Configure the Add-on

1. **Click:** **Configuration** tab
2. **Set these values:**

```yaml
confidence_threshold: 0.80
review_threshold: 0.65
camera_paths: []
enable_daily_poll: false
daily_poll_time: "02:00"
drive_folder_id: ""
api_port: 8080
api_token: "your_secret_token_here"
```

**Important Notes:**
- `review_threshold` (0.65) **must be less than** `confidence_threshold` (0.80)
- `daily_poll_time` must be in **HH:MM** format (e.g., "02:00")
- `api_token` can be any string (e.g., "my_secret_token_123")
- `camera_paths` leave as empty array `[]` for now
- `drive_folder_id` leave empty `""` for now

3. **Click:** **Save** button

---

### Step 5: Start the Add-on

1. **Click:** **Start** button (top right)
2. **Wait:** A few seconds for add-on to start
3. **Status** should change to: **"Running"** (green)

---

### Step 6: Verify Installation ✅

1. **Click:** **Logs** tab
2. **You should see:**

```
Starting Face Recognition Add-on
Configuration loaded successfully
Add-on ready (Chunk 0 - Configuration only)
Waiting for future functionality... (Chunk 2+)
```

**Success Indicators:**
- ✅ Status shows **"Running"** (green)
- ✅ Logs show "Configuration loaded successfully"
- ✅ No error messages
- ✅ Add-on stays running

**If you see errors:**
- Check the error message in logs
- Common issues:
  - Configuration validation error (check threshold values)
  - Missing files (verify GitHub repository structure)

---

## Troubleshooting

### Add-on Not Appearing in Store

**Problem:** Can't find "Face Recognition" add-on

**Solutions:**
1. **Refresh repository:**
   - Remove repository from Repositories list
   - Re-add it
   - Wait a few minutes

2. **Check repository URL:**
   - Must be: `https://github.com/USERNAME/REPO`
   - NOT: `git@github.com:USERNAME/REPO.git` (SSH)

3. **Check repository structure:**
   - Go to GitHub
   - Verify `face_recognition/face_recognition/config.yaml` exists
   - Verify `face_recognition/face_recognition/Dockerfile` exists

4. **Check repository visibility:**
   - Repository must be **Public** OR
   - Use GitHub token for private repos (advanced)

### Add-on Fails to Install

**Problem:** Installation fails or errors

**Solutions:**
1. **Check logs:**
   - Look for error messages
   - Common: Docker build errors, missing files

2. **Verify GitHub files:**
   - All files should be on GitHub
   - Check `face_recognition/face_recognition/` structure

3. **Try again:**
   - Uninstall (if partially installed)
   - Reinstall

### Add-on Fails to Start

**Problem:** Status shows "Stopped" or "Error"

**Solutions:**
1. **Check Configuration:**
   - Verify `review_threshold < confidence_threshold`
   - Verify time format is HH:MM

2. **Check Logs:**
   - Look for configuration errors
   - Look for missing file errors

3. **Common Errors:**
   - **"Configuration validation error"** → Fix threshold values
   - **"File not found"** → Verify GitHub repository structure
   - **"Permission denied"** → Check HA add-on permissions

### Configuration Not Loading

**Problem:** Logs show configuration errors

**Solutions:**
1. **Check values:**
   - `confidence_threshold`: Must be 0.0-1.0
   - `review_threshold`: Must be < confidence_threshold
   - `daily_poll_time`: Must be HH:MM format

2. **Reset to defaults:**
   - Use default values from config.yaml
   - Save and restart

---

## What to Expect (Chunk 0)

**Current Functionality:**
- ✅ Add-on installs successfully
- ✅ Configuration loads from HA UI
- ✅ Validation works (thresholds, time format)
- ✅ Add-on stays running
- ⚠️ **No functionality yet** (waiting for Chunk 2)

**This is Expected!**
- Chunk 0 only handles configuration
- Chunk 2 will add HTTP API
- Chunk 3+ will add face recognition

---

## Next Steps After Installation

1. ✅ **Verify** add-on is running
2. ✅ **Test** configuration changes:
   - Change threshold values
   - Verify validation works
   - Test invalid values (should fail gracefully)
3. 🚀 **Proceed** to Chunk 2: IPC & Event Plumbing

---

## Quick Reference

**Repository URL Format:**
```
https://github.com/USERNAME/haFacialRecognition
```

**Required Configuration:**
- `review_threshold < confidence_threshold`
- `daily_poll_time` in HH:MM format

**Success Logs:**
```
Configuration loaded successfully
Add-on ready (Chunk 0 - Configuration only)
```

---

**Need Help?** Check logs first - they usually tell you what's wrong!

