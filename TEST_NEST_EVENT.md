# Testing Nest Event Ingestion

## Option 1: Using Services (Recommended)

**Services** appear in a **different tab** than Events:

1. Go to **Developer Tools** (wrench icon in sidebar)
2. Click the **Services** tab (NOT the Events tab)
3. In the "Service" dropdown, look for:
   - `face_recognition.fire_nest_event` (new service for testing)
   - `face_recognition.fire_event` (existing service)

4. Select `face_recognition.fire_nest_event`
5. Fill in the fields:
   - **device_id**: `65563380bfcf5478f63ff88485eca57` (or your device ID)
   - **nest_event_id**: Use an existing event ID from your `nest/event_media` folder (e.g., `1767637263`)
   - **event_type**: `camera_person` or `camera_motion`
6. Click **Call Service**

## Option 2: Fire Event Directly (If Services Don't Appear)

If services aren't showing up, you can fire the `nest_event` directly:

1. Go to **Developer Tools → Events** tab
2. **Event type**: `nest_event`
3. **Event data** (YAML):
   ```yaml
   type: camera_person
   device_id: "65563380bfcf5478f63ff88485eca57"
   nest_event_id: "1767637263"
   timestamp: "2026-01-07T09:29:32"
   ```
4. Click **Fire Event**

This will trigger your `NestEventListener` just like a real Nest event!

## Troubleshooting: Services Not Appearing

If services don't appear in Developer Tools → Services:

1. **Check if integration loaded:**
   - Go to **Settings → Devices & Services**
   - Look for "Face Recognition" integration
   - Check logs for "Face Recognition services registered"

2. **Check logs:**
   - Look for: `"=== FACE RECOGNITION INTEGRATION LOADING (CHUNK 3) ==="`
   - Look for: `"Services set up successfully"`
   - Look for: `"Face Recognition services registered"`

3. **Verify files are copied:**
   - Make sure `services.py` and `services.yaml` are in `/config/custom_components/face_recognition/`
   - Restart Home Assistant after copying files

4. **Use Option 2** (fire event directly) if services still don't work

## What Happens When You Fire the Event

1. The `nest_event` is fired on the Home Assistant event bus
2. Your `NestEventListener` picks it up
3. It looks for MP4 video at: `/config/nest/event_media/<device_id>/<nest_event_id>/`
4. Extracts a frame from the video using `ffmpeg` or Python libraries
5. Sends event and image data to the add-on at `http://localhost:8180/event`

Check logs to see each step!

