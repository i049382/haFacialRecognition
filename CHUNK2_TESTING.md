# Chunk 2 Testing Guide

## Testing Steps

### 1. Rebuild Add-on with Chunk 2 Code

**Important:** The add-on needs to be rebuilt with the new Chunk 2 code that includes the HTTP API server.

1. **Commit and push Chunk 2 changes to GitHub:**
   ```bash
   git add .
   git commit -m "Chunk 2: IPC & Event Plumbing - HTTP API server"
   git push
   ```

2. **In Home Assistant:**
   - Go to **Settings → Add-ons → Face Recognition**
   - Click **Uninstall** (to remove old container)
   - Click **Install** (rebuilds with new code)
   - Wait for installation to complete
   - Click **Start**

### 2. Check Add-on Logs

After starting, check the **Logs** tab. You should see:
```
Starting Face Recognition Add-on
Configuration loaded successfully
Add-on ready (Chunk 2 - IPC & Event Plumbing)
HTTP API server starting on port 8080
```

If you see errors, check:
- Is Flask installed? (should be in requirements.txt)
- Are there any import errors?

### 3. Test HTTP API Endpoints

#### Option A: From Browser (if port is exposed)

1. **Check if port is exposed:**
   - The `config.yaml` now includes `ports: 8080/tcp: 8080`
   - This should expose port 8080 to the host

2. **Test Status Endpoint:**
   ```
   http://homeassistant.local:8080/status
   ```
   Or try:
   ```
   http://YOUR_HA_IP:8080/status
   ```

3. **Expected Response:**
   ```json
   {
     "status": "ready",
     "version": "0.0.1",
     "chunk": "2"
   }
   ```

#### Option B: From Inside HA (SSH/Terminal)

If you have SSH access:
```bash
# From inside HA container/host
curl http://localhost:8080/status
```

Or from Supervisor:
```bash
ha addons exec face_recognition curl http://localhost:8080/status
```

### 4. Test Event Endpoint (POST /event)

**Note:** This requires authentication if `api_token` is configured.

#### Without Token (if api_token is empty):
```bash
curl -X POST http://localhost:8080/event \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": "test_001",
    "display_name": "Test Person",
    "confidence": 0.99,
    "camera": "test_camera"
  }'
```

#### With Token (if api_token is set):
```bash
curl -X POST http://localhost:8080/event \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": "test_001",
    "display_name": "Test Person",
    "confidence": 0.99,
    "camera": "test_camera"
  }'
```

**Expected Response:**
```json
{
  "status": "received"
}
```

### 5. Test Event Firing (Integration Service)

Once the integration is installed:
1. Go to **Developer Tools → Services**
2. Service: `face_recognition.fire_event`
3. Service Data:
   ```yaml
   person_id: "test_001"
   display_name: "Test Person"
   confidence: 0.99
   camera: "test_camera"
   ```
4. Click **Call Service**
5. Check **Developer Tools → Events** → Listen to `face_recognition.detected`
6. Should see the event appear

## Troubleshooting

### Port Not Accessible

**Issue:** `http://homeassistant.local:8080/status` returns "site can not be reached"

**Solutions:**
1. **Check if port is exposed:**
   - Verify `config.yaml` has `ports: 8080/tcp: 8080`
   - Rebuild add-on after adding ports

2. **Check add-on logs:**
   - Should see "HTTP API server starting on port 8080"
   - If not, API server didn't start

3. **Check if add-on is running:**
   - Status should show "Running"
   - If not, check logs for errors

4. **Try different URL:**
   - `http://YOUR_HA_IP:8080/status` (replace with actual IP)
   - `http://localhost:8080/status` (from HA host)

5. **Check firewall:**
   - Port 8080 might be blocked
   - Try from inside HA network

### API Server Not Starting

**Check logs for:**
- Import errors (Flask not installed?)
- Port already in use?
- Configuration errors?

**Fix:**
- Verify `requirements.txt` includes `flask==3.0.0`
- Rebuild add-on
- Check logs for specific errors

### Integration Service Not Available

**Issue:** `face_recognition.fire_event` service doesn't appear

**Solution:**
- Integration needs to be installed in `custom_components/`
- Restart HA after installing integration
- See `INSTALL_INTEGRATION.md` for details

## Success Criteria

✅ **Chunk 2 Complete When:**
- [ ] Add-on starts without errors
- [ ] Logs show "HTTP API server starting on port 8080"
- [ ] `GET /status` returns correct JSON
- [ ] `POST /event` accepts events (with/without auth)
- [ ] Events can be fired via integration service (if installed)
- [ ] Events appear in HA event bus

---

**Next:** Once Chunk 2 is tested and working, proceed to Chunk 3 or 4!

