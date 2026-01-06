# Check: Config.yaml Requirements for Add-on Discovery

## Required Fields for Add-on Discovery

Home Assistant requires specific fields in `config.yaml` for add-on discovery. Let me verify ours has everything.

## Current Config.yaml Fields

✅ `name: Face Recognition`  
✅ `version: "0.0.1"`  
✅ `slug: face_recognition`  
✅ `description: Personal face recognition system for Home Assistant`  
✅ `arch: [aarch64, amd64, armhf, armv7, i386]`  
✅ `init: false`  
✅ `options:` (configuration schema)  
✅ `schema:` (validation schema)  
✅ `image:` (Docker image)

## Potential Issues

### Issue 1: Missing `homeassistant` Field

Some HA versions require:
```yaml
homeassistant: "2023.1.0"  # Minimum HA version
```

### Issue 2: Image Format

Current: `image: "ghcr.io/home-assistant/{arch}-base-python:latest"`

Should be: `image: ghcr.io/home-assistant/{arch}-base-python:latest` (no quotes)

### Issue 3: Slug Must Match Directory

Directory: `face_recognition/face_recognition/`  
Slug: `face_recognition` ✅ (matches)

### Issue 4: Version Format

Current: `version: "0.0.1"` ✅ (quoted, which is correct)

---

## Let's Try Adding Missing Fields

I'll update config.yaml to include potentially missing fields that might help with discovery.

