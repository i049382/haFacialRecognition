# Fix: Docker Image Install Error

## Error Found

```
Can't install ghcr.io/home-assistant/amd64-base-python:0.0.1: DockerError(404, 'manifest unknown')
```

## Problem

Home Assistant is trying to pull `ghcr.io/home-assistant/amd64-base-python:0.0.1` but:
1. The image doesn't exist with that tag (`:0.0.1` is the add-on version, not image tag)
2. We're using a Dockerfile with `BUILD_FROM`, so we don't need the `image` field

## Solution

**Removed the `image` field** from config.yaml because:
- We're using a Dockerfile that builds from `BUILD_FROM`
- HA will automatically use the correct base image for `BUILD_FROM`
- The `image` field was causing HA to try to pull a non-existent image

## What Changed

**Before:**
```yaml
image: ghcr.io/home-assistant/{arch}-base-python
```

**After:**
```yaml
# Image field removed - using Dockerfile with BUILD_FROM instead
```

## Next Steps

1. **Commit and push:**
   - Commit `face_recognition/face_recognition/config.yaml`
   - Push to GitHub

2. **In HA:**
   - Remove repository
   - Re-add repository
   - Wait 2 minutes
   - Try installing add-on again

3. **Expected:**
   - Add-on should install successfully
   - HA will build from Dockerfile using BUILD_FROM

---

**This should fix the installation error!**

