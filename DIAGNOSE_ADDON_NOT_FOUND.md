# Diagnose: Add-on Not Found After All Steps

## What You've Tried
✅ Removed repository  
✅ Restarted HA  
✅ Added repository  
✅ Restarted HA  
✅ Waited  
❌ Add-on still not found  

## Critical Checks

### 1. Verify Files Are Actually on GitHub

**Go to these URLs and verify files exist:**

**A. Repository.yaml:**
```
https://github.com/i049382/haFacialRecognition/blob/main/repository.yaml
```
**OR if branch is `master`:**
```
https://github.com/i049382/haFacialRecognition/blob/master/repository.yaml
```

**B. Config.yaml:**
```
https://github.com/i049382/haFacialRecognition/blob/main/face_recognition/face_recognition/config.yaml
```
**OR:**
```
https://github.com/i049382/haFacialRecognition/blob/master/face_recognition/face_recognition/config.yaml
```

**If files don't exist:**
- They weren't pushed to GitHub
- Commit and push them now

### 2. Check Branch Name

**Home Assistant might be looking at wrong branch:**

1. **Go to GitHub:** `https://github.com/i049382/haFacialRecognition`
2. **Check default branch:**
   - Look at top of page: "main" or "master"?
   - Click "branches" to see all branches

**If default is `master` but HA expects `main`:**
- Either rename branch to `main` on GitHub
- Or update repository.yaml (see below)

### 3. Check Supervisor Logs

**This is critical - logs will tell us what's wrong:**

1. **HA → Settings → System → Logs**
2. **Top right:** Select **"Supervisor"** (not Core)
3. **Look for errors about:**
   - Repository refresh
   - Add-on discovery
   - Config validation
   - File not found errors

**Common log errors:**
- `Failed to load repository`
- `Invalid add-on structure`
- `Config validation failed`
- `File not found: config.yaml`

**Copy any errors you see** - they'll tell us exactly what's wrong!

### 4. Verify Repository Structure on GitHub

**Go to:** `https://github.com/i049382/haFacialRecognition/tree/main`

**Should see:**
```
repository.yaml                    ← At root
face_recognition/                  ← Directory
  └── face_recognition/            ← Nested directory
      ├── config.yaml              ← Must exist!
      ├── Dockerfile
      ├── run.sh
      └── ...
```

**If structure is wrong:**
- Files are in wrong location
- Need to reorganize

### 5. Check Repository.yaml Format

**Current format:**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
```

**Try adding version (sometimes helps):**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
version: "1.0.0"
```

### 6. Test with Raw GitHub URLs

**Sometimes HA needs raw file access:**

1. **Test repository.yaml:**
   ```
   https://raw.githubusercontent.com/i049382/haFacialRecognition/main/repository.yaml
   ```
   Should show file contents

2. **Test config.yaml:**
   ```
   https://raw.githubusercontent.com/i049382/haFacialRecognition/main/face_recognition/face_recognition/config.yaml
   ```
   Should show file contents

**If these don't work:**
- Files aren't on GitHub
- Or branch name is wrong

---

## Most Likely Issues

### Issue 1: Files Not Pushed to GitHub
**Check:** Go to GitHub, verify files exist
**Fix:** Commit and push in GitHub Desktop

### Issue 2: Wrong Branch
**Check:** Default branch on GitHub
**Fix:** Either rename branch or update repository.yaml

### Issue 3: Config.yaml Syntax Error
**Check:** Supervisor logs for validation errors
**Fix:** Fix syntax errors in config.yaml

### Issue 4: Repository Structure Wrong
**Check:** Files in correct location on GitHub
**Fix:** Reorganize files to match structure

---

## Step-by-Step Diagnostic

### Step 1: Verify GitHub Files
1. Go to: `https://github.com/i049382/haFacialRecognition`
2. **Check:**
   - [ ] `repository.yaml` exists at root
   - [ ] `face_recognition/face_recognition/config.yaml` exists
   - [ ] Default branch is `main` (or `master`)

### Step 2: Check Supervisor Logs
1. HA → Settings → System → Logs
2. Select **"Supervisor"** (top right)
3. **Look for:**
   - Repository refresh errors
   - Add-on discovery errors
   - File not found errors
4. **Copy any errors** you see

### Step 3: Test Raw URLs
1. Try: `https://raw.githubusercontent.com/i049382/haFacialRecognition/main/repository.yaml`
2. Should show file contents
3. If 404: Files not on GitHub or wrong branch

### Step 4: Check Repository in HA
1. HA → Settings → Add-ons → Add-on Store
2. ⋮ → Repositories
3. **Click on your repository** (if listed)
4. **Check:** Does it show any add-ons listed?
5. **Check:** Any error messages?

---

## What to Report Back

Please check and tell me:

1. **Do files exist on GitHub?**
   - Can you see `repository.yaml`?
   - Can you see `face_recognition/face_recognition/config.yaml`?

2. **What's the default branch?**
   - `main` or `master`?

3. **What do Supervisor logs say?**
   - Any errors about repository or add-on?

4. **Do raw URLs work?**
   - Can you access files via raw.githubusercontent.com?

5. **What happens when you click repository in HA?**
   - Does it show any add-ons?
   - Any error messages?

---

## Quick Fix to Try

**Update repository.yaml with version:**

```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
version: "1.0.0"
```

Then:
1. Commit and push
2. Remove repository in HA
3. Re-add repository
4. Wait 2 minutes
5. Check again

---

**Most Important:** Check Supervisor logs - they will tell us exactly what's wrong!

