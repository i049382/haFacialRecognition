# Face Recognition Integration

Home Assistant custom integration for face recognition system.

## Installation

1. Copy the `integration/` folder to `/config/custom_components/face_recognition/` in your Home Assistant installation

2. Add configuration to `/config/configuration.yaml`:
   ```yaml
   face_recognition:
     api_host: localhost
     api_port: 8080
     ha_api_token: "your_long_lived_access_token"
   ```

3. Restart Home Assistant

## Configuration

See `configuration.yaml.example` for configuration options.

### Required Configuration

- `ha_api_token`: Long-lived access token for Home Assistant API calls

### Optional Configuration

- `api_host`: Add-on API hostname (default: `localhost`)
- `api_port`: Add-on API port (default: `8080`)
- `api_token`: Add-on API authentication token (if configured)

## Getting Your HA API Token

1. Open Home Assistant
2. Go to: Your Profile (bottom left) → **Long-Lived Access Tokens**
3. Click: **Create Token**
4. Name it: "Face Recognition Integration"
5. Copy the token and paste it in `configuration.yaml`

## Services

### `face_recognition.fire_event`
Manually fire a recognition event (for testing).


## Events

### `face_recognition.detected`
Fired when a face is detected and recognized.

## Requirements

- Home Assistant 2024.1 or later
- Face Recognition Add-on running

