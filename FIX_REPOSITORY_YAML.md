# Fix: "Not a valid add-on repository" Error

## Problem
Home Assistant says: `https://github.com/i049382/haFacialRecognition is not a valid add-on repository`

## Solution: Add repository.yaml

Home Assistant requires a `repository.yaml` file at the root of your repository to recognize it as an add-on repository.

## What I Just Did

✅ Created `repository.yaml` file at the root of your repository

## What You Need to Do

### Step 1: Commit the New File

1. **Open GitHub Desktop**
2. **You should see:** `repository.yaml` in the list of changed files
3. **Check the box** next to `repository.yaml`
4. **Summary:** `Add repository.yaml for HA add-on store`
5. **Click:** "Commit to main"
6. **Click:** "Push origin"

### Step 2: Verify on GitHub

1. **Go to:** `https://github.com/i049382/haFacialRecognition`
2. **Verify:** `repository.yaml` file exists at the root
3. **Check contents:** Should show:
   ```yaml
   name: Face Recognition Add-ons
   url: https://github.com/i049382/haFacialRecognition
   maintainer: i049382
   ```

### Step 3: Try Again in Home Assistant

1. **Remove repository** from HA (if already added):
   - Settings → Add-ons → Add-on Store
   - ⋮ → Repositories
   - Remove `https://github.com/i049382/haFacialRecognition`

2. **Re-add repository:**
   - Click **Add**
   - Enter: `https://github.com/i049382/haFacialRecognition`
   - Click **Add**
   - Wait for refresh

3. **Verify:**
   - Should now recognize as valid repository ✅
   - "Face Recognition" add-on should appear

---

## Repository Structure (Now Correct)

```
haFacialRecognition/
├── repository.yaml          # ✅ REQUIRED - tells HA this is an add-on repo
├── face_recognition/        # ✅ Add-on directory
│   └── face_recognition/
│       ├── config.yaml
│       ├── Dockerfile
│       └── ...
├── integration/
└── README.md
```

---

## Why This Was Needed

Home Assistant add-on repositories need:
1. ✅ `repository.yaml` at root (tells HA where add-ons are)
2. ✅ Add-on directories: `addon_slug/addon_slug/config.yaml`

We had #2 but were missing #1!

---

## After Fixing

Once `repository.yaml` is pushed to GitHub:
- ✅ HA will recognize the repository
- ✅ "Face Recognition" add-on will appear
- ✅ You can install it!

---

**Next Steps:**
1. Commit `repository.yaml` to GitHub
2. Re-add repository in HA
3. Install add-on!

