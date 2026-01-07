# Test Nest Event Payload

Based on your last logs, here's a payload that matches the real Nest event structure.

## For Developer Tools → Events

**Event type:** `nest_event`

**Event data (YAML):**
```yaml
device_id: "65563380bfcf5478f63ff88485eca57e"
type: "camera_person"
timestamp: "2026-01-07T11:14:09.646000+00:00"
nest_event_id: "WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd"
attachment:
  image: "/api/nest/event_media/65563380bfcf5478f63ff88485eca57e/WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd/thumbnail"
  video: "/api/nest/event_media/65563380bfcf5478f63ff88485eca57e/WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd"
zones:
  - ""
```

## For Service Call (face_recognition.fire_nest_event)

If you want to use the service instead:

**Service:** `face_recognition.fire_nest_event`

**Service data (YAML):**
```yaml
device_id: "65563380bfcf5478f63ff88485eca57e"
nest_event_id: "WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd"
event_type: "camera_person"
```

## Updated Payload with Current Timestamp

To test with a fresh event (use current timestamp):

**Event type:** `nest_event`

**Event data (YAML):**
```yaml
device_id: "65563380bfcf5478f63ff88485eca57e"
type: "camera_person"
timestamp: "2026-01-07T11:30:00+00:00"
nest_event_id: "WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd"
attachment:
  image: "/api/nest/event_media/65563380bfcf5478f63ff88485eca57e/WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd/thumbnail"
  video: "/api/nest/event_media/65563380bfcf5478f63ff88485eca57e/WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd"
zones:
  - ""
```

## What Happens

When you fire this event:
1. Your `NestEventListener` will receive it
2. It will extract `attachment.image` URL
3. It will try to fetch via Nest API using your HA token
4. If API fails, it will fallback to filesystem matching by timestamp
5. It will extract a frame from the video
6. It will send the event and image data to your add-on at `http://localhost:8180/event`

## Notes

- The `nest_event_id` (`WyIxNzM3MDU5MDUwIiwgIjU4NzIwNjkxNSJd`) is base64-encoded - this is normal for Nest events
- The `attachment.image` URL will only work if the media hasn't expired (usually expires in minutes)
- If you want to test with a real video file, use a `nest_event_id` that matches an existing video in your filesystem

