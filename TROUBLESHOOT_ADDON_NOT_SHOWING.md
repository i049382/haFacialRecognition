# Troubleshooting: Add-on Not Showing in Store

## Problem
Repository added successfully (no error), but "Face Recognition" add-on doesn't appear in the store.

## Common Causes & Solutions

### 1. Repository Not Refreshed

**Solution:**
1. **Remove repository:**
   - Settings → Add-ons → Add-on Store
   - ⋮ → Repositories
   - Remove `https://github.com/i049382/haFacialRecognition`

2. **Wait 30 seconds**

3. **Re-add repository:**
   - Click **Add**
   - Enter: `https://github.com/i049382/haFacialRecognition`
   - Click **Add**
   - **Wait 1-2 minutes** for full refresh

4. **Check again:**
   - Scroll through Add-on Store
   - Look for "Face Recognition" under your repository name

### 2. Check Repository Structure on GitHub

**Verify on GitHub:**
1. Go to: `https://github.com/i049382/haFacialRecognition`
2. **Check these files exist:**
   - ✅ `repository.yaml` (at root)
   - ✅ `face_recognition/face_recognition/config.yaml`
   - ✅ `face_recognition/face_recognition/Dockerfile`

**If files are missing:**
- They weren't pushed to GitHub
- Commit and push them

### 3. Check config.yaml Syntax

**Verify config.yaml is valid:**
1. Go to: `https://github.com/i049382/haFacialRecognition/blob/main/face_recognition/face_recognition/config.yaml`
2. **Check for:**
   - ✅ `slug: face_recognition` (must match directory name)
   - ✅ `name: Face Recognition`
   - ✅ Valid YAML syntax (no syntax errors)

**Common issues:**
- Missing quotes around version: `version: "0.0.1"` ✅
- Invalid YAML indentation
- Missing required fields

### 4. Force Refresh in HA

**Method 1: Restart HA Supervisor**
1. Settings → System → Hardware
2. Click **⋮** → **Restart Supervisor**
3. Wait for restart
4. Check Add-on Store again

**Method 2: Clear Browser Cache**
1. Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Or clear browser cache
3. Reload HA

### 5. Check HA Logs

**Check Supervisor logs:**
1. Settings → System → Logs
2. Look for errors related to:
   - Add-on repository
   - Repository refresh
   - Add-on discovery

**Common log errors:**
- "Failed to load repository"
- "Invalid add-on structure"
- "Config validation failed"

### 6. Verify Repository URL Format

**Correct format:**
```
https://github.com/i049382/haFacialRecognition
```

**Wrong formats:**
- ❌ `https://github.com/i049382/haFacialRecognition.git` (has .git)
- ❌ `git@github.com:i049382/haFacialRecognition.git` (SSH)
- ❌ `https://github.com/i049382/haFacialRecognition/tree/main` (has path)

### 7. Check Branch Name

**Verify default branch:**
1. Go to GitHub repository
2. Check if default branch is `main` or `master`
3. **If `master`:**
   - HA might be looking at `main` branch
   - Either rename branch or specify branch in repository.yaml

**Update repository.yaml if needed:**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
```

### 8. Manual Verification

**Check if files are actually on GitHub:**

1. **Repository.yaml:**
   ```
   https://github.com/i049382/haFacialRecognition/blob/main/repository.yaml
   ```
   Should show the file contents

2. **Config.yaml:**
   ```
   https://github.com/i049382/haFacialRecognition/blob/main/face_recognition/face_recognition/config.yaml
   ```
   Should show the config file

3. **Directory structure:**
   ```
   https://github.com/i049382/haFacialRecognition/tree/main/face_recognition/face_recognition
   ```
   Should show all add-on files

---

## Step-by-Step Fix

### Step 1: Verify Files on GitHub
1. Go to your repository on GitHub
2. Verify `repository.yaml` exists at root
3. Verify `face_recognition/face_recognition/config.yaml` exists
4. Click on `config.yaml` to verify it's valid YAML

### Step 2: Remove and Re-add Repository
1. HA → Settings → Add-ons → Add-on Store
2. ⋮ → Repositories
3. **Remove** your repository
4. **Wait 1 minute**
5. **Re-add** repository
6. **Wait 2-3 minutes** for full refresh

### Step 3: Check Add-on Store
1. Scroll through Add-on Store
2. Look for section with your repository name
3. Look for "Face Recognition" add-on
4. **Note:** It might be at the bottom of the list

### Step 4: Check Logs
1. Settings → System → Logs
2. Filter for: "repository" or "add-on"
3. Look for any errors

---

## Still Not Showing?

### Check These:

1. **Is repository public?**
   - Private repos need GitHub token (advanced setup)

2. **Are all files committed?**
   - Check GitHub - all files should be there

3. **Try different browser/device:**
   - Sometimes browser cache issues

4. **Check HA version:**
   - Older HA versions might have issues
   - Update HA if possible

---

## Expected Behavior

**After adding repository:**
- ✅ No error message
- ✅ Repository appears in Repositories list
- ✅ After 1-2 minutes, add-on appears in store
- ✅ Add-on shows under repository name section

**If add-on appears:**
- ✅ Click on it
- ✅ Click Install
- ✅ Configure and Start

---

## Quick Checklist

- [ ] `repository.yaml` exists at root on GitHub
- [ ] `face_recognition/face_recognition/config.yaml` exists on GitHub
- [ ] Repository removed and re-added in HA
- [ ] Waited 2-3 minutes after adding
- [ ] Scrolled through entire Add-on Store
- [ ] Checked HA logs for errors
- [ ] Verified repository is public (or has token)

---

**Most Common Fix:** Remove repository, wait 1 minute, re-add, wait 2-3 minutes, then check again!

