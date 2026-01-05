# Quick Start: GitHub Desktop 🚀

## 5-Minute Setup

### 1. Create Repository (2 min)

**Option A: On GitHub.com**
1. Go to github.com → Click **+** → **New repository**
2. Name: `haFacialRecognition`
3. **Public** (required for HA)
4. **Don't** initialize with README
5. Click **Create**

**Option B: In GitHub Desktop**
1. File → New Repository
2. Name: `haFacialRecognition`
3. Local path: Your project folder
4. Click **Create Repository**

### 2. Clone/Open Repository (1 min)

**If created on GitHub:**
1. GitHub Desktop → File → Clone Repository
2. URL tab → Paste: `https://github.com/YOUR_USERNAME/haFacialRecognition.git`
3. Click **Clone**
4. Copy your project files into cloned folder

**If created locally:**
- GitHub Desktop should already have it open ✅

### 3. Commit & Push (1 min)

1. **Select all files** (checkboxes)
2. **Summary:** `Chunk 0: Configuration & Credentials`
3. **Click:** "Commit to main"
4. **Click:** "Push origin" (or "Publish branch")

### 4. Install in HA (1 min)

1. HA → Settings → Add-ons → Add-on Store
2. ⋮ → Repositories → Add
3. URL: `https://github.com/YOUR_USERNAME/haFacialRecognition`
4. Refresh → Install "Face Recognition"
5. Configure → Start

### 5. Verify ✅

Check logs - should see:
```
Configuration loaded successfully
Add-on ready (Chunk 0)
```

---

**Done!** 🎉

For detailed instructions, see `GITHUB_DESKTOP_GUIDE.md`

