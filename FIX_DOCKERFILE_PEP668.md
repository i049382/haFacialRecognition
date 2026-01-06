# Fix: Dockerfile PEP 668 Error

## Error Found

```
error: externally-managed-environment
× This environment is externally managed
```

## Problem

Python 3.12 in Alpine Linux has PEP 668 protection which prevents installing packages directly with pip. The error occurs when trying to:
1. Upgrade pip: `pip3 install --upgrade pip`
2. Install packages: `pip3 install -r requirements.txt`

## Solution

**Removed pip upgrade step** and **added `--break-system-packages` flag** to pip install:

**Before:**
```dockerfile
RUN apk add --no-cache \
    python3 \
    py3-pip \
    sqlite \
    && pip3 install --no-cache-dir --upgrade pip

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
```

**After:**
```dockerfile
RUN apk add --no-cache \
    python3 \
    py3-pip \
    sqlite

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt
```

## Changes Made

1. **Removed pip upgrade:** `py3-pip` already installs pip, no need to upgrade
2. **Added `--break-system-packages`:** Required for Python 3.12+ PEP 668 protection
   - This is safe in a Docker container (isolated environment)
   - Allows installing packages via pip

## Next Steps

1. **Commit and push:**
   - Commit `face_recognition/face_recognition/Dockerfile`
   - Push to GitHub

2. **In HA:**
   - Remove repository
   - Re-add repository
   - Wait 2 minutes
   - Try installing add-on again

3. **Expected:**
   - Docker build should succeed
   - Add-on should install successfully

---

**This should fix the Docker build error!**

