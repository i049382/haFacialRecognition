# Why Nest Doesn't Deliver Thumbnails Automatically

## Current Situation

Looking at your logs, Nest events **DO** include thumbnail URLs:
```python
'attachment': {
    'image': '/api/nest/event_media/.../thumbnail',
    'video': '/api/nest/event_media/...'
}
```

But these URLs expire quickly (404 errors).

## Why Thumbnails Aren't "Delivered Automatically"

### 1. **Nest API Design**
- Nest provides **temporary URLs** that expire quickly
- Thumbnails are generated on-demand from videos
- No persistent thumbnail storage by default

### 2. **Home Assistant Nest Integration Behavior**
- Stores **MP4 videos** to filesystem: `/config/nest/event_media/<device_id>/<timestamp>-camera_person.mp4`
- Does **NOT** store separate thumbnail files
- Thumbnails must be generated from videos or fetched from API

### 3. **Our Current Approach**
- ✅ Try API first (fast, but expires)
- ✅ Fallback to filesystem (extract frame from MP4)
- ✅ Works reliably with fallback

## What We Can Check

### Option 1: Check if Nest Stores Thumbnails
Let's verify what files Nest actually stores:

```bash
# Check Nest media directory
ls -la /config/nest/event_media/<device_id>/

# Look for:
# - *.mp4 files (videos) ✅ These exist
# - *.jpg, *.jpeg, *.png files (thumbnails) ❓ Do these exist?
```

### Option 2: Generate Thumbnails on Event
We could generate and cache thumbnails when events fire:
- Extract frame immediately
- Save as thumbnail file
- Use cached thumbnail instead of API

### Option 3: Faster API Fetch
Try to fetch from API **immediately** when event fires:
- Reduce processing delay
- Fetch thumbnail before it expires

## Investigation Steps

1. **Check filesystem structure:**
   - What files does Nest actually store?
   - Are there any thumbnail files?

2. **Check event timing:**
   - How quickly do we process events?
   - Is there delay causing expiration?

3. **Check Nest integration settings:**
   - Are there settings to enable thumbnail storage?
   - Can we configure thumbnail generation?

## Next Steps

Let's add logging to check:
1. What files Nest stores
2. How quickly we process events
3. If thumbnails exist in filesystem

