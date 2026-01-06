# Rebuild Add-on After Fix

## Current Status

✅ `__main__.py` file created locally  
❌ Add-on still using old code (needs rebuild)

## Why It's Still Failing

The add-on container was built with the old code (before `__main__.py` existed). You need to rebuild it.

## Steps to Fix

### Step 1: Commit and Push Changes

**In GitHub Desktop:**
1. You should see `__main__.py` in changed files
2. **Check the box** next to it
3. **Summary:** `Fix: Rename main.py to __main__.py for module execution`
4. **Click:** "Commit to main"
5. **Click:** "Push origin"

### Step 2: Rebuild Add-on in HA

**Option A: Uninstall and Reinstall (Recommended)**
1. **Stop** the add-on (if running)
2. **Uninstall** the add-on
3. **Wait** 30 seconds
4. **Reinstall** the add-on
5. **Start** the add-on

**Option B: Force Rebuild (If Available)**
1. **Stop** the add-on
2. Look for **"Rebuild"** button (if available)
3. Click **Rebuild**
4. **Start** the add-on

### Step 3: Verify

**After rebuild and start, check logs:**
- Should see: `Starting Face Recognition Add-on`
- Should see: `Configuration loaded successfully`
- Should NOT see: `No module named face_recognition_addon.__main__`

## Why Rebuild is Needed

Docker containers are built from the code at build time. The old container still has `main.py` instead of `__main__.py`. Rebuilding creates a new container with the correct file.

## Quick Checklist

- [ ] `__main__.py` exists locally ✅
- [ ] Changes committed to git
- [ ] Changes pushed to GitHub
- [ ] Add-on uninstalled in HA
- [ ] Add-on reinstalled in HA
- [ ] Add-on started
- [ ] Logs show success

---

**After pushing and rebuilding, the add-on should start successfully!**

