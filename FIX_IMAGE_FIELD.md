# Fix: Image Field Regex Error

## Error Found!

Supervisor logs show:
```
does not match regular expression ... for dictionary value @ data['image']. 
Got 'ghcr.io/home-assistant/{arch}-base-python:latest'
```

## Problem

The `image` field format is invalid. The regex doesn't accept `:latest` tag with `{arch}` placeholder.

## Solution

**Option 1: Remove `:latest` tag (Recommended)**

Changed from:
```yaml
image: ghcr.io/home-assistant/{arch}-base-python:latest
```

To:
```yaml
image: ghcr.io/home-assistant/{arch}-base-python
```

**Option 2: Remove `image` field entirely**

If using Dockerfile, you might not need the `image` field at all. But keeping it is fine for now.

## Next Steps

1. **Commit the fix:**
   - In GitHub Desktop, commit `face_recognition/face_recognition/config.yaml`
   - Push to GitHub

2. **In HA:**
   - Remove repository
   - Re-add repository
   - Wait 2 minutes
   - Check for add-on

3. **Verify:**
   - Check Supervisor logs again
   - Should see add-on discovered!

---

**This should fix it!** The image field format was preventing add-on discovery.

