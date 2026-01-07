# Configure HA API Token

## Location

The `ha_api_token` should be configured in **Home Assistant's `configuration.yaml`** file.

**Path:** `/config/configuration.yaml` (in your HA installation)

## Configuration Format

Add this to your `configuration.yaml`:

```yaml
face_recognition:
  api_host: localhost
  api_port: 8080
  ha_api_token: "your_long_lived_access_token_here"
```

## Full Example

```yaml
# Other HA configurations...
# ...

face_recognition:
  api_host: localhost          # Add-on API host
  api_port: 8080               # Add-on API port
  ha_api_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Long-lived access token
```

## How to Get the Token

1. **Open Home Assistant**
2. **Go to:** Your Profile (bottom left) → **Long-Lived Access Tokens**
3. **Click:** **Create Token**
4. **Name it:** "Face Recognition Integration"
5. **Copy the token** (starts with `eyJ...`)
6. **Paste it** in `configuration.yaml` (with quotes)

## Where This File Is Located

### If using File Editor add-on:
- Open **File Editor** add-on
- Navigate to `/config/configuration.yaml`
- Edit the file

### If using SSH:
- File is at: `/config/configuration.yaml`
- Edit with: `nano /config/configuration.yaml` or `vi /config/configuration.yaml`

## After Adding Configuration

1. **Save** `configuration.yaml`
2. **Restart Home Assistant:**
   - Settings → System → Restart
   - Or Developer Tools → YAML → Restart

3. **Verify it loaded:**
   - Check HA logs for: "HA API token configured for internal API calls"
   - If you see: "No HA API token configured" → token not found

## Important Notes

- **Use quotes** around the token: `"eyJ..."`
- **No spaces** before/after the colon
- **Indentation matters** - use 2 spaces (not tabs)
- **Restart required** after changing `configuration.yaml`

## Optional: Use Secrets

For better security, you can use HA secrets:

### In `configuration.yaml`:
```yaml
face_recognition:
  api_host: localhost
  api_port: 8080
  ha_api_token: !secret face_recognition_ha_token
```

### In `secrets.yaml`:
```yaml
face_recognition_ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

This keeps the token out of the main config file.

## Current Status Check

After restarting, check HA logs for:
- ✅ "HA API token configured for internal API calls" → Working
- ⚠️ "No HA API token configured" → Not configured or not found

