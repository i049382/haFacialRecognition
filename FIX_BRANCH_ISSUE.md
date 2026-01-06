# Fix: Branch Name Issue (master vs main)

## Problem Found

Your local branch is `master`, but Home Assistant might be looking for `main` branch by default.

## Solution Options

### Option 1: Rename Branch to `main` (Recommended)

**On GitHub:**
1. Go to: `https://github.com/i049382/haFacialRecognition`
2. Click **Settings** tab
3. Scroll to **"Default branch"** section
4. Click **"Switch to another branch"**
5. If `main` doesn't exist, create it:
   - Go to **"Branches"** tab
   - Click **"New branch"**
   - Name: `main`
   - Based on: `master`
   - Click **"Create branch"**
6. Go back to **Settings → Default branch**
7. Select `main` as default
8. Click **"Update"**

**Then push your code to `main`:**
```bash
git checkout -b main
git push origin main
```

**Or in GitHub Desktop:**
1. Branch → New Branch
2. Name: `main`
3. Based on: `master`
4. Create branch
5. Push origin

### Option 2: Update repository.yaml to Specify Branch

**Update repository.yaml:**
```yaml
name: Face Recognition Add-ons
url: https://github.com/i049382/haFacialRecognition
maintainer: i049382
```

**Actually, HA doesn't support branch specification in repository.yaml**, so Option 1 is better.

### Option 3: Verify Files Are on `master` Branch

**Check on GitHub:**
1. Go to: `https://github.com/i049382/haFacialRecognition/tree/master`
2. Verify files exist:
   - `repository.yaml`
   - `face_recognition/face_recognition/config.yaml`

**If files exist on `master`:**
- HA should find them
- But `main` is more standard

---

## Quick Fix: Create `main` Branch

**In GitHub Desktop:**

1. **Branch → New Branch**
2. **Name:** `main`
3. **Based on:** `master` (or current branch)
4. **Create branch**
5. **Push origin** (publish the branch)

**Then on GitHub:**
1. Go to repository Settings
2. Change default branch to `main`
3. Delete `master` branch (optional)

**Then in HA:**
1. Remove repository
2. Re-add repository
3. Wait 2 minutes
4. Check for add-on

---

## Verify Current State

**Check these URLs:**

**Master branch:**
```
https://github.com/i049382/haFacialRecognition/tree/master
```

**Repository.yaml on master:**
```
https://raw.githubusercontent.com/i049382/haFacialRecognition/master/repository.yaml
```

**Config.yaml on master:**
```
https://raw.githubusercontent.com/i049382/haFacialRecognition/master/face_recognition/face_recognition/config.yaml
```

**If these URLs work:**
- Files are on GitHub
- But HA might be looking for `main` branch

---

## Most Likely Solution

**Create `main` branch and set as default:**

1. **GitHub Desktop:**
   - Branch → New Branch → `main`
   - Push origin

2. **GitHub.com:**
   - Settings → Default branch → `main`

3. **HA:**
   - Remove repository
   - Re-add repository
   - Wait 2 minutes

---

**Try this first - it's the most common issue!**

