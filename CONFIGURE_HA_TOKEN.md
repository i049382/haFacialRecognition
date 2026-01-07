# Configure Home Assistant API Token

## Add Token to configuration.yaml

Add this to your `/config/configuration.yaml`:

```yaml
face_recognition:
  api_host: localhost
  api_port: 8180
  ha_api_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjNTg3ZTVhYWQ1NTM0Y2U2YTAzZmUzNDk2NDQ5ZDczMiIsImlhdCI6MTc2Nzc4MjU5MSwiZXhwIjoyMDgzMTQyNTkxfQ.wd-28qDCW0cr-U7CGrM6cIIP-hB0C8eKfmGumybePlI"
```

## Steps

1. **Open File Editor** add-on in Home Assistant
2. **Open** `/config/configuration.yaml`
3. **Add** the `face_recognition:` section above (or update existing section)
4. **Save** the file
5. **Restart Home Assistant** (Settings → System → Restart)

## Verify It's Working

After restart, check logs for:
- `"HA API token configured for internal API calls"`
- When a Nest event fires, you should see: `"Using HA API token for authentication"`

## Security Note

⚠️ **Important:** This token gives full access to your Home Assistant instance. Keep it secure:
- Don't share it publicly
- Don't commit it to GitHub
- If compromised, revoke it immediately and create a new one

## Test the Token

You can test if the token works by:
1. Go to Developer Tools → Services
2. Call `face_recognition.fire_nest_event` service
3. Check logs - should see "Using HA API token for authentication"
4. Should successfully fetch image via Nest API

