# Fix: Module Execution Error

## Error Found

```
No module named face_recognition_addon.__main__; 'face_recognition_addon' is a package and cannot be directly executed
```

## Problem

When using `python3 -m face_recognition_addon`, Python looks for `__main__.py` file in the package, but we had `main.py` instead.

## Solution

**Renamed `main.py` to `__main__.py`** so that `python3 -m face_recognition_addon` works correctly.

**Why:**
- `python3 -m package_name` requires `package_name/__main__.py`
- This is the standard Python way to make a package executable as a module

## What Changed

**Before:**
```
face_recognition_addon/
├── __init__.py
├── config.py
└── main.py  ❌ Wrong name
```

**After:**
```
face_recognition_addon/
├── __init__.py
├── config.py
└── __main__.py  ✅ Correct name
```

## Next Steps

1. **Commit and push:**
   - Commit the change (renamed main.py to __main__.py)
   - Push to GitHub

2. **In HA:**
   - The add-on should rebuild automatically, OR
   - Uninstall and reinstall the add-on

3. **Start add-on:**
   - Click Start
   - Check logs - should see success messages!

---

**This should fix the module execution error!**

