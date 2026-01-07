# How to Create a Long-Lived Access Token for Home Assistant

## Option 1: Using Home Assistant CLI (Recommended)

If you have SSH or terminal access to your Home Assistant host:

1. **SSH into your Home Assistant host** (or use the Terminal add-on)

2. **Run this command:**
   ```bash
   ha auth create-token --name "Face Recognition Integration" --lifespan 365
   ```

3. **Copy the token** that's displayed (it will look like a long string)

4. **Add it to your `configuration.yaml`:**
   ```yaml
   face_recognition:
     api_host: localhost
     api_port: 8180
     ha_api_token: "PASTE_YOUR_TOKEN_HERE"
   ```

## Option 2: Using REST API (if you have a temporary token)

If you have a temporary access token (from logging in):

1. **Make a POST request:**
   ```bash
   curl -X POST \
     -H "Authorization: Bearer YOUR_TEMPORARY_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"client_name": "Face Recognition Integration", "lifespan": 365}' \
     http://homeassistant.local:8123/api/auth/long_lived_access_token
   ```

2. **Copy the token** from the response

3. **Add it to `configuration.yaml`** as shown above

## Option 3: Check if token section exists

Sometimes the UI section is hidden. Try:
- Scroll all the way down on your profile page
- Check if there's a "Tokens" or "Access Tokens" section
- Look in Developer Tools → Long-Lived Access Tokens

## After Adding Token

1. **Save `configuration.yaml`**
2. **Restart Home Assistant**
3. **Check logs** - should see "HA API token configured for internal API calls"
4. **Trigger a Nest event** - should now successfully fetch images!

