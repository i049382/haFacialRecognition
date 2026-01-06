# Final Troubleshooting: Add-on Still Not Showing

## Current Status
✅ Files on GitHub  
✅ Default branch set to `main`  
✅ No errors in Supervisor logs  
❌ Add-on still not visible  

## Additional Checks

### 1. Check Supervisor API Directly

**Try accessing Supervisor API:**

1. **In HA, go to:** Developer Tools → Services
2. **Service:** `supervisor.reload`
3. **Click:** "Call Service"
4. **Wait:** 30 seconds
5. **Check:** Add-on Store again

**Or via URL (if you have access):**
```
http://your-ha-ip:4357/store
```
Should show all repositories and add-ons

### 2. Try "Check for Updates"

**In HA:**
1. Settings → Add-ons → Add-on Store
2. Click **⋮** (three dots)
3. Click **"Check for updates"**
4. Wait for refresh
5. Check for add-on

### 3. Verify Repository Structure Exactly

**Go to GitHub and verify:**

```
https://github.com/i049382/haFacialRecognition/tree/main
```

**Should see:**
```
repository.yaml                    ← Root
face_recognition/                 ← Directory
  └── face_recognition/           ← Nested directory
      ├── config.yaml            ← Must be here!
      ├── Dockerfile
      ├── run.sh
      └── requirements.txt
```

**If structure is different:** That's the problem!

### 4. Check if Repository Shows Add-ons Count

**In HA:**
1. Settings → Add-ons → Add-on Store
2. ⋮ → Repositories
3. **Click on your repository** (if it's listed)
4. **Does it show:** "X add-ons" or "0 add-ons"?
5. **If 0:** Repository found but add-on not discovered

### 5. Try Minimal Config.yaml

**Sometimes HA is picky about config format. Let's try a minimal version:**

Create a test config.yaml with only required fields:

```yaml
name: Face Recognition
version: "0.0.1"
slug: face_recognition
description: Personal face recognition system for Home Assistant
arch:
  - aarch64
  - amd64
  - armhf
  - armv7
  - i386
init: false
image: ghcr.io/home-assistant/{arch}-base-python:latest
```

**Note:** Removed quotes from `image` field - sometimes that matters!

### 6. Check Supervisor Version

**Some HA versions have bugs with add-on discovery:**

1. Settings → System → About
2. Check **Supervisor** version
3. If very old, might need update

### 7. Try Different Browser/Device

**Sometimes browser cache issues:**

1. Try different browser
2. Try incognito/private mode
3. Try mobile app
4. Clear browser cache completely

### 8. Check Repository.yaml Format

**Current:**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
version: "1.0.0"
```

**Try without version:**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
```

### 9. Verify Raw URLs Work

**Test these URLs in browser:**

1. **Repository.yaml:**
   ```
   https://raw.githubusercontent.com/i049382/haFacialRecognition/main/repository.yaml
   ```

2. **Config.yaml:**
   ```
   https://raw.githubusercontent.com/i049382/haFacialRecognition/main/face_recognition/face_recognition/config.yaml
   ```

**If these don't work:** Files aren't accessible (permissions issue?)

### 10. Check if Repository is Actually Added

**In HA:**
1. Settings → Add-ons → Add-on Store
2. ⋮ → Repositories
3. **Is your repository listed?**
4. **If yes:** Click on it - what does it show?
5. **If no:** Repository wasn't added successfully

---

## Most Likely Issues

### Issue 1: Image Field Format
**Try removing quotes from image:**
```yaml
image: ghcr.io/home-assistant/{arch}-base-python:latest
```
Instead of:
```yaml
image: "ghcr.io/home-assistant/{arch}-base-python:latest"
```

### Issue 2: Repository Not Actually Refreshed
**Try:** "Check for updates" button explicitly

### Issue 3: Browser Cache
**Try:** Different browser or incognito mode

### Issue 4: Supervisor Needs Restart
**Try:** Restart Supervisor explicitly

---

## Diagnostic Questions

Please check and tell me:

1. **When you click your repository in Repositories list, what does it show?**
   - Number of add-ons?
   - Any error message?
   - Empty list?

2. **Do the raw GitHub URLs work?**
   - Can you access files via raw.githubusercontent.com?

3. **What happens when you click "Check for updates"?**
   - Any error?
   - Does it refresh?

4. **Have you tried a different browser?**
   - Same result?

5. **What's your Supervisor version?**
   - Settings → System → About → Supervisor

---

## Quick Test: Minimal Config

Let's try updating config.yaml to be absolutely minimal and see if that helps discovery:

```yaml
name: Face Recognition
version: "0.0.1"
slug: face_recognition
description: Test
arch:
  - amd64
image: ghcr.io/home-assistant/amd64-base-python:latest
```

**Commit this minimal version, push, remove/re-add repository, and see if it appears.**

---

**Most Important:** Check what happens when you click on your repository in the Repositories list - that will tell us if it's a discovery issue or a display issue!

