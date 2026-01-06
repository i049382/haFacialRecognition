# Fix: Repository Found But No Add-ons Discovered

## Problem Identified
✅ Repository is recognized (shows in list)  
❌ No add-ons discovered (only "remove" option when clicked)  

This means the repository structure or config.yaml format is preventing add-on discovery.

## Most Likely Issues

### Issue 1: Directory Structure

HA expects add-ons to be discoverable. Let's verify the exact structure:

**Current structure:**
```
haFacialRecognition/
├── repository.yaml
└── face_recognition/
    └── face_recognition/
        └── config.yaml
```

**HA might need:**
```
haFacialRecognition/
├── repository.yaml
└── face_recognition/
    └── config.yaml  ← Directly here, not nested twice?
```

**OR:**
```
haFacialRecognition/
├── repository.yaml
└── face_recognition/
    └── face_recognition/
        └── config.yaml  ← Current structure
```

### Issue 2: Config.yaml Location

HA scans for `config.yaml` files. It might be looking in the wrong place.

### Issue 3: Config.yaml Format Issue

Even if found, config.yaml might have a format issue preventing discovery.

---

## Solution: Try Both Structures

Let's test if HA needs the config.yaml directly under `face_recognition/` instead of nested.

### Option A: Current Structure (Nested)
```
face_recognition/face_recognition/config.yaml
```

### Option B: Flat Structure (Test)
```
face_recognition/config.yaml
```

---

## Quick Test

Let's create a test version with config.yaml directly under `face_recognition/` to see if that works.

