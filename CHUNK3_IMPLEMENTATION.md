# Chunk 3: Nest Event Ingestion - Implementation

## Scope
- Listen to `nest_event` events from Home Assistant
- Fetch snapshot immediately (Nest URLs expire quickly)
- Forward events to add-on for processing

## Deliverables

### 1. Nest Event Listener (Integration) ✅
- Listens to `nest_event` events from HA event bus
- Fetches images immediately from Nest API
- Sends events to add-on via HTTP API

### 2. API Updates (Add-on) ✅
- Updated `/event` endpoint to handle Nest ingestion events
- Logs Nest events for processing

### 3. Image Fetching ✅
- Fetches images from `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
- Handles expired URLs gracefully
- Timeout handling for quick expiration

## Files Created/Modified

**Integration:**
- `integration/nest_listener.py` - Nest event listener
- `integration/__init__.py` - Updated to start Nest listener

**Add-on:**
- `face_recognition/face_recognition/face_recognition_addon/api.py` - Updated to handle Nest events
- `face_recognition/face_recognition/face_recognition_addon/__main__.py` - Updated chunk version
- `face_recognition/face_recognition/requirements.txt` - Added `requests` library

## How It Works

1. **Integration Setup:**
   - When integration loads, checks if Nest integration is available
   - If available, starts Nest event listener
   - Listener subscribes to `nest_event` events

2. **Event Handling:**
   - When `nest_event` fires:
     - Extracts `device_id`, `event_id`, `type`
     - Only processes `motion` and `person` events
     - Immediately fetches image from Nest API
     - Sends event + image info to add-on

3. **Image Fetching:**
   - Uses HA's internal API: `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
   - Fetches with 10-second timeout (URLs expire quickly)
   - Handles 404 (expired) gracefully
   - Logs image size for verification

4. **Add-on Processing:**
   - Receives Nest event via `/event` endpoint
   - Logs event information
   - In future chunks, will process image for face recognition

## Testing

### Test 1: Verify Nest Listener Starts
1. Install integration in `custom_components/`
2. Restart HA
3. Check logs for: "Nest integration detected, starting Nest event listener"
4. Check logs for: "Nest event listener started"

### Test 2: Trigger Nest Event
1. Ensure Nest camera is configured in HA
2. Trigger motion/person event on Nest camera
3. Check integration logs for: "Processing Nest event: motion on device <device_id>"
4. Check add-on logs for: "Nest event received: motion on device <device_id>"

### Test 3: Image Fetching
1. Trigger Nest event
2. Check logs for: "Successfully fetched Nest image (<size> bytes)"
3. If expired, should see: "Nest media expired or not found"

### Test 4: Expired Media Handling
1. Wait for Nest event to expire (usually ~30 seconds)
2. Manually trigger event processing
3. Should see graceful error handling, not crash

## Configuration

The integration automatically detects Nest integration. No configuration needed for Chunk 3.

In future chunks, we may add:
- Enable/disable Nest ingestion
- Filter by event types
- Filter by device IDs

## Next Steps

🚀 **Chunk 4: Filesystem Camera Ingestion** or **Chunk 5: Face Detection**

---

**Chunk 3 Implementation Complete!** Ready for testing.

