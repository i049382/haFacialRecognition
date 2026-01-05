# Face Recognition Add-on

Home Assistant add-on for face recognition processing.

## Installation

### As Local Add-on

1. Copy this directory to your HA add-ons folder:
   ```bash
   cp -r . /config/addons/face_recognition
   ```

2. In Home Assistant:
   - Go to **Settings → Add-ons → Add-on Store**
   - Click **⋮** → **Repositories**
   - Add local path: `/config/addons`
   - Refresh
   - Find "Face Recognition" and install

### As GitHub Repository

1. Fork this repository
2. In Home Assistant:
   - Go to **Settings → Add-ons → Add-on Store**
   - Click **⋮** → **Repositories**
   - Add: `https://github.com/yourusername/haFacialRecognition`
   - Refresh
   - Find "Face Recognition" and install

## Configuration

Configure via Home Assistant UI:

- `confidence_threshold`: Recognition threshold (0.0-1.0)
- `review_threshold`: Review threshold (must be < confidence_threshold)
- `camera_paths`: List of camera watch directories
- `enable_daily_poll`: Enable daily model update check
- `daily_poll_time`: Time for daily poll (HH:MM format)
- `drive_folder_id`: Google Drive folder ID
- `api_port`: HTTP API port (default: 8080)
- `api_token`: API authentication token

## Secrets

Add to `/config/secrets.yaml`:

```yaml
face_recognition_drive_credentials: |
  {
    "type": "service_account",
    ...
  }
```

## Status

- **Chunk 0:** ✅ Configuration & Credentials (Complete)
- **Chunk 2:** ⏳ IPC & Event Plumbing (Next)

## Development

See `ha_face_recognition_build_chunks_v2.md` for build plan.

