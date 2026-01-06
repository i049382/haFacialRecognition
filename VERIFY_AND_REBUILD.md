# Verify and Rebuild Add-on

## Current Situation

✅ `__main__.py` file exists locally  
❌ Add-on container still has old code (needs rebuild)

## Verification Steps

### Step 1: Verify File Exists Locally

The file should be at:
```
face_recognition/face_recognition/face_recognition_addon/__main__.py
```

**Check in GitHub Desktop:**
- You should see `__main__.py` in changed files
- If you don't see it, the file might not be tracked by git

### Step 2: Commit and Push

**In GitHub Desktop:**

1. **Check if `__main__.py` appears in changed files:**
   - If YES: Check the box and commit
   - If NO: The file might not be tracked. Try:
     - Right-click on `__main__.py` → "Add to Git"
     - Or use "Select all" to stage everything

2. **Commit message:**
   ```
   Fix: Add __main__.py for module execution
   ```

3. **Push to GitHub**

### Step 3: Verify on GitHub

**Go to GitHub and check:**
```
https://github.com/i049382/haFacialRecognition/tree/main/face_recognition/face_recognition/face_recognition_addon
```

**Should see:**
- `__init__.py`
- `__main__.py` ✅ (this is the new file)
- `config.py`

**If `__main__.py` is NOT on GitHub:**
- File wasn't committed/pushed
- Commit and push it

### Step 4: Rebuild Add-on in HA

**Important:** You MUST rebuild the add-on to get the new code!

1. **Stop** the add-on (if running)
2. **Uninstall** the add-on
   - This removes the old container
3. **Wait** 30 seconds
4. **Reinstall** the add-on
   - This builds a NEW container with the new code
5. **Start** the add-on

### Step 5: Verify Success

**After rebuild and start, logs should show:**
```
Starting Face Recognition Add-on
Configuration loaded successfully
Add-on ready (Chunk 0 - Configuration only)
```

**NOT:**
```
No module named face_recognition_addon.__main__
```

---

## Why Rebuild is Critical

Docker containers are **immutable snapshots** of your code at build time. The old container was built with `main.py`, so it will ALWAYS fail until you rebuild with `__main__.py`.

**Simply restarting won't work** - you MUST rebuild!

---

## Quick Checklist

- [ ] `__main__.py` exists locally ✅
- [ ] `__main__.py` appears in GitHub Desktop changed files
- [ ] Changes committed to git
- [ ] Changes pushed to GitHub
- [ ] `__main__.py` visible on GitHub website
- [ ] Add-on **uninstalled** in HA (not just stopped!)
- [ ] Add-on **reinstalled** in HA (rebuilds container)
- [ ] Add-on started
- [ ] Logs show success (no module error)

---

**The key is: UNINSTALL then REINSTALL - not just restart!**

