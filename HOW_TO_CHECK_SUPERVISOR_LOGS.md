# How to Check Supervisor Logs (Not Core Logs)

## Problem
The log file you shared is from **Home Assistant Core**, not **Supervisor**. We need **Supervisor logs** to see add-on repository errors.

## How to Get Supervisor Logs

### Method 1: Via Home Assistant UI

1. **Go to:** Settings → System → Logs
2. **Top right corner:** There's a dropdown menu
3. **Click the dropdown** - it probably says "Core" or "Home Assistant"
4. **Select:** **"Supervisor"** from the dropdown
5. **Look for errors** about:
   - `repository`
   - `add-on`
   - `face_recognition`
   - `config.yaml`
   - `Failed to load`

### Method 2: Via Supervisor Panel (If Available)

1. **Go to:** Settings → Add-ons → Supervisor
2. **Click:** "Logs" tab
3. **Look for errors**

### Method 3: Via SSH/Terminal (Advanced)

If you have SSH access:
```bash
docker logs homeassistant | grep -i "repository\|add-on\|face"
```

Or:
```bash
ha supervisor logs
```

---

## What to Look For in Supervisor Logs

**Error messages might look like:**
- `Failed to load repository`
- `Invalid add-on structure`
- `Config validation failed`
- `File not found: config.yaml`
- `Unable to discover add-ons`
- `Repository refresh failed`

**Or success messages:**
- `Repository loaded successfully`
- `Found X add-ons`
- `Add-on discovered: face_recognition`

---

## Why Supervisor Logs Matter

**Supervisor logs** show:
- ✅ Repository refresh status
- ✅ Add-on discovery process
- ✅ Config.yaml validation errors
- ✅ File access errors

**Core logs** (what you shared) show:
- ❌ Home Assistant component errors
- ❌ Integration errors
- ❌ Not add-on repository errors

---

## Next Steps

1. **Go to:** Settings → System → Logs
2. **Select:** "Supervisor" from dropdown (top right)
3. **Look for:** Errors about repository or add-on
4. **Copy:** Any errors you find
5. **Share:** The Supervisor log errors

---

**The Supervisor logs will tell us exactly why the add-on isn't being discovered!**

