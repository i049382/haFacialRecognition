# GitHub Repository Setup for Home Assistant Add-on

## Repository Structure

Your repository is now set up with the correct structure for Home Assistant add-on installation:

```
haFacialRecognition/
├── face_recognition/              # Add-on directory (slug name)
│   └── face_recognition/          # Add-on directory (slug name again)
│       ├── config.yaml            # Add-on configuration schema
│       ├── Dockerfile             # Container definition
│       ├── run.sh                 # Entry point script
│       ├── requirements.txt      # Python dependencies
│       ├── .dockerignore          # Docker ignore file
│       └── face_recognition_addon/  # Python package
│           ├── __init__.py
│           ├── config.py
│           └── main.py
├── integration/                   # HA custom integration (separate)
└── README.md                      # Project documentation
```

## GitHub Setup Steps

### 1. Push to GitHub

If you haven't already, create a GitHub repository and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Chunk 0 - Configuration & Credentials"

# Add remote (replace with your GitHub username/repo)
git remote add origin https://github.com/YOUR_USERNAME/haFacialRecognition.git

# Push to GitHub
git push -u origin main
```

### 2. Install in Home Assistant

Once your code is on GitHub:

1. **Open Home Assistant**
   - Go to **Settings → Add-ons → Add-on Store**
   - Click the **⋮ (three dots)** in the top right
   - Select **Repositories**

2. **Add Repository**
   - Click **Add** button
   - Enter your GitHub repository URL:
     ```
     https://github.com/YOUR_USERNAME/haFacialRecognition
     ```
   - Click **Add**

3. **Refresh**
   - Click **Refresh** button (or wait a few seconds)
   - The repository should appear in the list

4. **Install Add-on**
   - Scroll down to find **"Face Recognition"** add-on
   - Click on it
   - Click **Install**
   - Wait for installation to complete

5. **Configure Add-on**
   - Click **Configuration** tab
   - Set your values:
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
   - Click **Save**

6. **Start Add-on**
   - Click **Start** button
   - Check **Logs** tab to verify it's running

### 3. Verify Installation

**✅ Success indicators:**
- Add-on status shows **"Running"**
- Logs show:
  ```
  Starting Face Recognition Add-on
  Configuration loaded successfully
  Add-on ready (Chunk 0 - Configuration only)
  Waiting for future functionality... (Chunk 2+)
  ```
- No error messages

**❌ If it fails:**
- Check logs for error messages
- Verify `config.yaml` syntax is correct
- Ensure all files are committed to GitHub
- Try refreshing the repository in HA

## Updating the Add-on

When you make changes and push to GitHub:

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Update: Description of changes"
   git push
   ```

2. **Update in Home Assistant:**
   - Go to **Settings → Add-ons → Face Recognition**
   - Click **Update** button (if available)
   - Or click **Uninstall** then **Install** again

## Repository URL Format

Home Assistant supports these GitHub URL formats:

- `https://github.com/USERNAME/REPO` ✅
- `https://github.com/USERNAME/REPO.git` ✅
- `git@github.com:USERNAME/REPO.git` ❌ (SSH not supported)

## Troubleshooting

### Add-on Not Appearing

1. **Check repository structure:**
   - Must have `face_recognition/face_recognition/` directory
   - Must have `config.yaml` in the inner directory

2. **Check GitHub URL:**
   - Must be public repository (or use GitHub token for private)
   - URL must be correct

3. **Refresh repository:**
   - Remove and re-add repository
   - Wait a few minutes for GitHub to update

### Add-on Fails to Start

1. **Check logs:**
   - Look for configuration errors
   - Verify JSON syntax in options

2. **Check configuration:**
   - Ensure `review_threshold < confidence_threshold`
   - Verify time format is HH:MM

### Configuration Not Loading

1. **Check secrets:**
   - Add `face_recognition_drive_credentials` to `/config/secrets.yaml`
   - Or leave empty (non-fatal)

2. **Check options.json:**
   - Should be auto-generated from config.yaml schema
   - Verify values are valid

## Next Steps

Once installed and running:

1. ✅ Verify add-on starts successfully
2. ✅ Check logs for configuration loading
3. ✅ Test configuration changes
4. 🚀 Proceed to **Chunk 2: IPC & Event Plumbing**

---

## Notes

- The add-on will run but do nothing until Chunk 2 (HTTP API)
- This is expected behavior for Chunk 0
- Configuration validation is working
- Ready for Chunk 2 implementation

