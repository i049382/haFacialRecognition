# GitHub Desktop Installation Guide

Step-by-step instructions for setting up and installing the add-on using GitHub Desktop.

## Prerequisites

- ✅ GitHub Desktop installed ([Download here](https://desktop.github.com/))
- ✅ GitHub account created
- ✅ Repository files ready (already done ✅)

---

## Step 1: Create GitHub Repository

### Option A: Create Repository on GitHub First

1. **Go to GitHub.com**
   - Log in to your account
   - Click the **+** icon (top right) → **New repository**

2. **Repository Settings:**
   - **Repository name:** `haFacialRecognition` (or your preferred name)
   - **Description:** "Face Recognition Add-on for Home Assistant"
   - **Visibility:** Choose **Public** (required for HA add-on store) or **Private**
   - **DO NOT** check "Initialize with README" (we already have files)
   - Click **Create repository**

3. **Copy Repository URL:**
   - Copy the HTTPS URL (e.g., `https://github.com/YOUR_USERNAME/haFacialRecognition.git`)
   - You'll need this in the next step

### Option B: Create Repository from GitHub Desktop

1. **Open GitHub Desktop**
2. **File → New Repository**
   - **Name:** `haFacialRecognition`
   - **Description:** "Face Recognition Add-on for Home Assistant"
   - **Local path:** Choose your project folder (should already be open)
   - **Git ignore:** None (we have our own `.gitignore`)
   - **License:** None (or add one if you want)
   - Click **Create Repository**

---

## Step 2: Initialize Repository in GitHub Desktop

### If You Created Repository on GitHub (Option A):

1. **Open GitHub Desktop**
2. **File → Clone Repository**
   - Go to **URL** tab
   - Paste your repository URL: `https://github.com/YOUR_USERNAME/haFacialRecognition.git`
   - Choose **Local path** (where to save it)
   - Click **Clone**

3. **Copy Your Files:**
   - Copy all files from your current project folder
   - Paste them into the cloned repository folder
   - Make sure `face_recognition/face_recognition/` structure is preserved

### If You Created Repository Locally (Option B):

1. **GitHub Desktop should already be open** with your repository
2. **Verify files are visible:**
   - You should see all your project files in the left panel
   - Check that `face_recognition/face_recognition/` directory exists

---

## Step 3: Commit and Push Files

### 3.1 Review Changes

1. **In GitHub Desktop**, you'll see:
   - **Left panel:** List of changed files
   - **Right panel:** File diff view

2. **Verify Important Files Are Included:**
   - ✅ `face_recognition/face_recognition/config.yaml`
   - ✅ `face_recognition/face_recognition/Dockerfile`
   - ✅ `face_recognition/face_recognition/run.sh`
   - ✅ `face_recognition/face_recognition/requirements.txt`
   - ✅ `face_recognition/face_recognition/face_recognition_addon/` (all Python files)
   - ✅ `integration/` directory
   - ✅ `README.md`

3. **Check for Unwanted Files:**
   - ❌ `__pycache__/` directories (should be ignored)
   - ❌ `*.pyc` files (should be ignored)
   - If you see these, they'll be ignored by `.gitignore`

### 3.2 Stage Files

1. **At the bottom left**, you'll see:
   - **Summary:** (empty text box)
   - **Description:** (optional text box)

2. **Stage All Files:**
   - Click the checkbox next to each file, OR
   - Click **"Select all"** checkbox at the top of the file list
   - All files should show a checkmark ✅

### 3.3 Write Commit Message

1. **In the Summary field**, type:
   ```
   Chunk 0: Configuration & Credentials - Ready for HA installation
   ```

2. **In the Description field** (optional), type:
   ```
   - Add-on configuration system
   - Secret handling via HA secrets.yaml
   - Configuration validation
   - Ready for Home Assistant installation
   ```

### 3.4 Commit

1. **Click "Commit to main"** button (bottom left)
   - Wait for commit to complete
   - You'll see "X files committed" message

### 3.5 Push to GitHub

1. **Click "Push origin"** button (top right, or in the toolbar)
   - If this is your first push, it might say **"Publish branch"**
   - Click **"Publish branch"** or **"Push origin"**

2. **Wait for Upload:**
   - Progress bar will show upload status
   - Wait until it says "Pushed to origin/main" or similar

3. **Verify on GitHub:**
   - Click **"View on GitHub"** button (or go to `https://github.com/YOUR_USERNAME/haFacialRecognition`)
   - You should see all your files on GitHub

---

## Step 4: Install in Home Assistant

### 4.1 Add Repository to HA

1. **Open Home Assistant**
2. **Go to:** Settings → Add-ons → Add-on Store
3. **Click:** ⋮ (three dots) in top right → **Repositories**
4. **Click:** **Add** button
5. **Enter Repository URL:**
   ```
   https://github.com/YOUR_USERNAME/haFacialRecognition
   ```
   - Replace `YOUR_USERNAME` with your actual GitHub username
   - **Important:** Use HTTPS URL, not SSH
6. **Click:** **Add**
7. **Wait:** A few seconds for repository to refresh

### 4.2 Install Add-on

1. **Scroll down** in Add-on Store
2. **Find:** "Face Recognition" add-on
   - Should appear under your repository name
   - Icon: May show default add-on icon
3. **Click:** On "Face Recognition" add-on
4. **Click:** **Install** button
5. **Wait:** For installation to complete (may take 1-2 minutes)

### 4.3 Configure Add-on

1. **Click:** **Configuration** tab
2. **Set Configuration Values:**
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
   - Adjust values as needed
   - **Important:** `review_threshold` must be less than `confidence_threshold`
3. **Click:** **Save**

### 4.4 Start Add-on

1. **Click:** **Start** button
2. **Click:** **Logs** tab to see output
3. **Verify:** You should see:
   ```
   Starting Face Recognition Add-on
   Configuration loaded successfully
   Add-on ready (Chunk 0 - Configuration only)
   Waiting for future functionality... (Chunk 2+)
   ```

---

## Step 5: Verify Installation

### ✅ Success Indicators:

- **Status:** Shows **"Running"** (green)
- **Logs:** Show configuration loaded successfully
- **No errors:** In logs or status

### ❌ If It Fails:

1. **Check Logs:**
   - Look for error messages
   - Common issues:
     - Configuration validation errors
     - Missing files
     - Syntax errors

2. **Check Configuration:**
   - Verify `review_threshold < confidence_threshold`
   - Verify time format is HH:MM (e.g., "02:00")

3. **Check GitHub:**
   - Verify files are on GitHub
   - Verify `face_recognition/face_recognition/` structure exists

---

## Updating the Add-on

When you make changes and want to update:

### In GitHub Desktop:

1. **Make your changes** to files
2. **GitHub Desktop** will show changed files
3. **Stage files** (checkboxes)
4. **Write commit message:**
   ```
   Update: Description of changes
   ```
5. **Click:** **Commit to main**
6. **Click:** **Push origin**

### In Home Assistant:

1. **Go to:** Settings → Add-ons → Face Recognition
2. **Click:** **Update** button (if available)
   - OR **Uninstall** then **Install** again
3. **Restart** add-on if needed

---

## Troubleshooting

### Repository Not Appearing in HA

1. **Check URL format:**
   - ✅ Correct: `https://github.com/USERNAME/REPO`
   - ❌ Wrong: `git@github.com:USERNAME/REPO.git` (SSH)

2. **Check repository visibility:**
   - Must be **Public** OR use GitHub token for private repos

3. **Refresh repository:**
   - Remove and re-add repository in HA
   - Wait a few minutes for GitHub to update

### Add-on Not Installing

1. **Check repository structure:**
   - Must have: `face_recognition/face_recognition/config.yaml`
   - Verify on GitHub website

2. **Check config.yaml:**
   - Must have valid YAML syntax
   - Must have `slug: face_recognition`

3. **Check GitHub Desktop:**
   - Verify all files are committed
   - Verify files are pushed to GitHub

### Add-on Crashes

1. **Check logs** for error messages
2. **Check configuration** values
3. **Verify** `review_threshold < confidence_threshold`

---

## Quick Reference

### GitHub Desktop Shortcuts:
- **Commit:** `Ctrl+Enter` (Windows) or `Cmd+Enter` (Mac)
- **Push:** `Ctrl+P` (Windows) or `Cmd+P` (Mac)
- **View on GitHub:** `Ctrl+Shift+G` (Windows) or `Cmd+Shift+G` (Mac)

### Important Files:
- `face_recognition/face_recognition/config.yaml` - Add-on configuration
- `face_recognition/face_recognition/Dockerfile` - Container definition
- `face_recognition/face_recognition/run.sh` - Entry script

---

## Next Steps

Once installed and running:

1. ✅ **Verify** add-on starts successfully
2. ✅ **Test** configuration changes
3. 🚀 **Proceed** to Chunk 2: IPC & Event Plumbing

---

**Need Help?** Check `GITHUB_SETUP.md` for more detailed troubleshooting.

