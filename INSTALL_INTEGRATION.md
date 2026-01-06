# Installing the Face Recognition Integration

## Steps to Install

### 1. Copy Integration to Home Assistant

The integration needs to be copied to your Home Assistant `custom_components` directory.

**On Home Assistant OS/Supervised:**
- Use the File Editor add-on or SSH add-on
- Navigate to `/config/custom_components/`
- Create folder: `face_recognition/`
- Copy all files from `integration/` folder to `/config/custom_components/face_recognition/`

**On Home Assistant Core (manual install):**
- Copy `integration/` folder to your HA config directory as `custom_components/face_recognition/`

### 2. Required Files

Make sure these files are copied:
```
custom_components/face_recognition/
├── __init__.py
├── manifest.json
├── events.py
├── services.py
└── services.yaml
```

### 3. Restart Home Assistant

After copying the files:
1. Go to Developer Tools → YAML
2. Click "Restart" (or restart HA via Settings → System → Restart)

### 4. Verify Installation

After restart:
1. Go to Developer Tools → Services
2. You should see `face_recognition.fire_event` in the service dropdown
3. If you see it, the integration is installed correctly!

## Alternative: Test Event Directly (No Integration Needed)

If you just want to test that events work, you can fire the event directly:

1. Go to Developer Tools → Events
2. Event type: `face_recognition.detected`
3. Event data:
   ```yaml
   person_id: "test_001"
   display_name: "Test Person"
   confidence: 0.99
   camera: "test_camera"
   ```
4. Click "Fire event"
5. If listening to `face_recognition.detected`, you should see it appear

This tests the event system without needing the integration installed.

