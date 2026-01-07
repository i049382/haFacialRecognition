# Nest Event to Filesystem Mapping - Options

## Problem
- Nest events provide: `nest_event_id` and preview URL `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
- Filesystem stores: `/config/nest/event_media/<device_id>/<folder>/<timestamp>-camera_person.mp4`
- The `nest_event_id` from the event may not match the folder name
- The MP4 filename prefix (e.g., `1767607742`) appears to be a timestamp, not the event ID

## Option 1: Use Nest API (Original Plan) ✅ Recommended
**Fetch the thumbnail immediately via the API endpoint**

### Pros:
- Works immediately when event fires
- No filesystem path matching needed
- Uses the official Nest API endpoint

### Cons:
- Requires HA API authentication token
- Media URLs expire quickly (must fetch immediately)

### Implementation:
- Use `attachment.image` URL from the event
- Fetch via `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
- Requires `ha_api_token` in configuration

## Option 2: Filesystem Watcher (Alternative)
**Watch the nest/event_media directory for new files**

### Pros:
- No authentication needed
- No event ID matching issues
- Can process files even if event was missed

### Cons:
- Files may appear slightly after event fires
- Need to correlate files with events (by timestamp)
- More complex logic

### Implementation:
- Use `watchdog` to watch `/config/nest/event_media/<device_id>/*/`
- When new MP4 file appears, extract timestamp from filename
- Match to recent `nest_event` by timestamp (within 5-10 seconds)

## Option 3: Automation Bridge (Hybrid)
**Use HA automation to bridge nest_event → our service**

### Pros:
- Automation has access to full event data
- Can extract correct paths/IDs
- Flexible - can add custom logic

### Cons:
- Requires user to create automation
- More moving parts

### Implementation:
```yaml
automation:
  - alias: "Nest Event to Face Recognition"
    trigger:
      - platform: event
        event_type: nest_event
        event_data:
          type: camera_person
    action:
      - service: face_recognition.process_nest_event
        data:
          device_id: "{{ trigger.event.data.device_id }}"
          nest_event_id: "{{ trigger.event.data.nest_event_id }}"
          # Automation can access filesystem or call API
```

## Recommendation: **Option 1 (Nest API)**

Since we already have the code structure for API fetching, let's:
1. **Fix the authentication** - use HA API token properly
2. **Fetch immediately** when event fires
3. **Fallback to filesystem** if API fails

This gives us the best of both worlds:
- Immediate processing (API)
- Reliability fallback (filesystem)

## Next Steps

1. **Test if HA API token works** - try fetching a thumbnail URL
2. **If API works**: Use it as primary method
3. **If API fails**: Add filesystem watcher as fallback
4. **Add correlation logic** - match events to files by timestamp if needed

