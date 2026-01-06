# Debug: Repository Found But No Add-ons

## Current Situation
✅ Repository appears in list  
✅ Can click on it  
❌ Only shows "remove" option  
❌ No add-ons listed  

This means HA found the repository but can't discover add-ons in it.

## Critical Check: Supervisor Logs

**Please check Supervisor logs for specific errors:**

1. **HA → Settings → System → Logs**
2. **Top right:** Select **"Supervisor"** (not Core)
3. **Look for lines containing:**
   - `repository`
   - `add-on`
   - `face_recognition`
   - `config.yaml`
   - `Failed`
   - `Error`

4. **Copy any errors** you see - they'll tell us exactly what's wrong!

## Most Likely Issues

### Issue 1: Config.yaml Not Found

**HA might be looking for config.yaml in wrong location.**

**Check on GitHub:**
```
https://github.com/i049382/haFacialRecognition/tree/main/face_recognition
```

**Should see:**
- `face_recognition/` directory (nested)
- Inside that: `config.yaml`, `Dockerfile`, etc.

**If structure looks wrong:** That's the problem!

### Issue 2: Config.yaml Format Issue

**Even if found, config.yaml might have format issues.**

**Test the config.yaml:**
1. Go to: `https://raw.githubusercontent.com/i049382/haFacialRecognition/main/face_recognition/face_recognition/config.yaml`
2. Copy the contents
3. Paste into a YAML validator: https://www.yamllint.com/
4. Check for errors

### Issue 3: Image Field Still Has Quotes

**I removed quotes, but verify it's pushed:**

Check the raw URL above - does `image:` have quotes?
- ❌ `image: "ghcr.io/..."`
- ✅ `image: ghcr.io/...`

### Issue 4: Directory Structure

**HA might need exact structure. Let's verify:**

**Current:**
```
face_recognition/face_recognition/config.yaml
```

**Some HA versions need:**
```
face_recognition/config.yaml  (flat, not nested)
```

## Quick Test: Check Supervisor Logs First

**Before trying anything else, check Supervisor logs:**

1. Go to Supervisor logs
2. Look for errors about:
   - "Failed to load add-on"
   - "Config not found"
   - "Invalid structure"
   - "face_recognition"

**The logs will tell us exactly what's wrong!**

## Alternative: Try Flat Structure

If logs don't help, let's try moving config.yaml up one level:

**Test structure:**
```
face_recognition/config.yaml  (instead of nested)
```

But **check logs first** - they'll tell us if it's a structure issue or something else!

---

## What to Do Right Now

1. **Check Supervisor logs** - Look for errors
2. **Copy any errors** you see
3. **Verify config.yaml on GitHub** - Check raw URL
4. **Report back** what you find

**The logs are the key - they'll tell us exactly what HA is trying to do and why it's failing!**

