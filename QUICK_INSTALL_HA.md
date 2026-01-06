# Quick Install in Home Assistant 🚀

## 5 Steps to Install

### 1. Add Repository
- **HA → Settings → Add-ons → Add-on Store**
- **⋮ → Repositories → Add**
- **URL:** `https://github.com/YOUR_USERNAME/haFacialRecognition`
- **Add** → Wait for refresh

### 2. Install Add-on
- **Find:** "Face Recognition" in Add-on Store
- **Click:** Install
- **Wait:** 1-2 minutes

### 3. Configure
- **Click:** Configuration tab
- **Set:**
  ```yaml
  confidence_threshold: 0.80
  review_threshold: 0.65
  camera_paths: []
  enable_daily_poll: false
  daily_poll_time: "02:00"
  drive_folder_id: ""
  api_port: 8080
  api_token: "test_token_123"
  ```
- **Save**

### 4. Start
- **Click:** Start button
- **Status:** Should show "Running" ✅

### 5. Verify
- **Click:** Logs tab
- **Should see:**
  ```
  Configuration loaded successfully
  Add-on ready (Chunk 0)
  ```

---

## ✅ Success!

If you see "Running" and logs show success → **Chunk 0 is working!**

---

**For detailed instructions, see `INSTALL_IN_HA.md`**

