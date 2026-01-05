# Installation Guide

## Quick Start

### 1. Push to GitHub

```bash
git add .
git commit -m "Chunk 0: Configuration & Credentials"
git push origin main
```

### 2. Install in Home Assistant

1. **Settings → Add-ons → Add-on Store**
2. Click **⋮** → **Repositories**
3. Add: `https://github.com/YOUR_USERNAME/haFacialRecognition`
4. Refresh
5. Install **"Face Recognition"** add-on
6. Configure and start

### 3. Verify

Check logs - should see:
```
Starting Face Recognition Add-on
Configuration loaded successfully
Add-on ready (Chunk 0 - Configuration only)
```

## Detailed Instructions

See `GITHUB_SETUP.md` for complete setup guide.

## Current Status

✅ **Chunk 0 Complete** - Configuration & Credentials  
⏳ **Chunk 2 Next** - IPC & Event Plumbing

The add-on will run but do nothing until Chunk 2 is implemented. This is expected.

