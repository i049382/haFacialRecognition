# Endpoint Diagnostic Guide

## Current Problem
`ServerDisconnectedError: Server disconnected` - Flask server crashes on POST request.

## Step 1: Update Add-on Files

### A. Update `api.py` with better error handling:
1. Copy the updated `api.py` to your add-on
2. It now has:
   - Outer try-except to catch ANY crash
   - Better logging (`=== POST /event ENDPOINT CALLED ===`)
   - Config object safety checks
   - JSON parsing with error handling

### B. Make sure `__main__.py` has Gunicorn disabled:
```python
# TEMPORARILY DISABLED GUNICORN FOR TESTING
use_gunicorn = False  # Force Flask dev server for now
```

## Step 2: Restart Add-on & Check Logs

### Restart add-on, then check logs for:
```
=== POST /event ENDPOINT CALLED ===
```

### If you see this:
✅ Endpoint is being called (good!)

### Then look for:
1. **Error messages** after that line
2. **Python tracebacks**
3. **"CONFIG IS NONE"** warning
4. **JSON parsing errors**

## Step 3: Run Diagnostic Tests

### Test 1: Basic connectivity
```bash
# From HA container/terminal
curl http://localhost:8080/status
```
Expected: `{"status": "ready", "version": "0.0.1", "chunk": "3"}`

### Test 2: Simple POST
```bash
curl -X POST http://localhost:8080/event \
  -H "Content-Type: application/json" \
  -d '{"test":true}'
```

### Test 3: Your actual payload
```bash
curl -X POST http://localhost:8080/event \
  -H "Content-Type: application/json" \
  -d '{"event_type":"nest_event","device_id":"test","event_id":"test","event_type_nest":"camera_person","camera":"test","image_size":12345,"timestamp":"2026-01-07T21:15:24.491000+00:00"}'
```

## Step 4: Common Crash Causes & Fixes

### Cause 1: `self.config` is `None`
**Fix**: Check `api.py` line 85-89 - we added a check for this.

### Cause 2: JSON parsing fails
**Fix**: We added better JSON error handling (lines 81-93).

### Cause 3: Missing imports in endpoint
**Fix**: The endpoint might try to import something that fails.

### Cause 4: Flask server itself crashes
**Fix**: Use the minimal test endpoint temporarily.

## Step 5: Minimal Endpoint Test

If still crashing, replace the entire `post_event` function with:

```python
@app.route('/event', methods=['POST'])
def post_event():
    """MINIMAL working endpoint."""
    logger.error("=== MINIMAL ENDPOINT CALLED ===")
    return jsonify({"status": "received", "minimal": True}), 200
```

## Step 6: Check Integration is Sending Correctly

From your logs, the integration sends:
```python
# Uses data=json.dumps(payload) not json=payload
json_data = json.dumps(payload)
response = await self._session.post(
    f"{self.api_url}/event",
    data=json_data,  # This is correct
    headers=headers,
    timeout=timeout,
)
```

## Expected Success Flow

1. Integration sends POST request
2. Add-on logs: `=== POST /event ENDPOINT CALLED ===`
3. Add-on logs request details
4. Add-on returns: `{"status": "received", "type": "nest_ingestion"}`
5. Integration logs: `Successfully sent Nest event to add-on`

## If Still Failing

### Option A: Enable Debug Mode
In `__main__.py`, change:
```python
api.run(host='0.0.0.0', port=config.api_port, debug=False, threaded=True, use_reloader=False)
```
To:
```python
api.run(host='0.0.0.0', port=config.api_port, debug=True, threaded=True, use_reloader=False)
```

### Option B: Check Port Conflict
Test if port 8080 is already used:
```bash
netstat -tulpn | grep :8080
```

### Option C: Change Port
In add-on config, change `api_port` to 8081, update integration config to match.

## Quick Checklist

- [ ] Updated `api.py` with better error handling
- [ ] Gunicorn disabled in `__main__.py`
- [ ] Add-on restarted
- [ ] Check logs for endpoint call
- [ ] Test with `curl` commands
- [ ] Check for Python exceptions in logs

## Success Indicators

You'll know it's working when you see in **add-on logs**:
```
=== POST /event ENDPOINT CALLED ===
[INFO] Received event data: ['event_type', 'device_id', ...]
[INFO] Sending response for Nest event
```

And in **integration logs**:
```
Successfully sent Nest event to add-on: {'status': 'received', 'type': 'nest_ingestion'}
```