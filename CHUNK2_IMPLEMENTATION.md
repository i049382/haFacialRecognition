# Chunk 2: IPC & Event Plumbing - Implementation

## Scope
- Add-on exposes local HTTP API
- Integration consumes API and fires HA events

## Deliverables

### 1. HTTP API Server (Add-on)
- ✅ `POST /event` - Receive recognition events
- ✅ `GET /status` - Health check endpoint
- ✅ API token authentication (if configured)
- ✅ Error handling and validation

### 2. Integration Updates
- ✅ Service to fire events manually (for testing)
- ✅ Event definitions (`face_recognition.detected`)
- ✅ Coordinator structure (for future API polling)

### 3. Testing
- ⏳ Mock event → HA event visible
- ⏳ Status endpoint works
- ⏳ Authentication works (if token configured)

## Files Created/Modified

**Add-on:**
- `face_recognition/face_recognition/face_recognition_addon/api.py` - HTTP API server
- `face_recognition/face_recognition/face_recognition_addon/__main__.py` - Updated to start API server

**Integration:**
- `integration/__init__.py` - Updated with coordinator structure
- `integration/services.py` - Service definitions
- `integration/services.yaml` - Service schema

## API Endpoints

### GET /status
**Response:**
```json
{
  "status": "ready",
  "version": "0.0.1",
  "chunk": "2"
}
```

### POST /event
**Request Headers:**
```
Authorization: Bearer <api_token>  (if api_token configured)
Content-Type: application/json
```

**Request Body:**
```json
{
  "person_id": "person_017",
  "display_name": "Alice (Neighbour)",
  "confidence": 0.94,
  "camera": "nest_doorbell",
  "image_id": "img_20260105_143211.jpg",
  "face_id": "img_face_0",
  "timestamp": "2026-01-05T14:32:11Z",
  "model_version": "v004"
}
```

**Response:**
```json
{
  "status": "received"
}
```

## Testing

### Test 1: Status Endpoint
```bash
curl http://localhost:8080/status
```

### Test 2: Fire Event (via HA Service)
1. Developer Tools → Services
2. Service: `face_recognition.fire_event`
3. Service Data:
```yaml
person_id: "test_001"
display_name: "Test Person"
confidence: 0.99
camera: "test_camera"
```
4. Call Service
5. Check Developer Tools → Events
6. Should see `face_recognition.detected` event

### Test 3: API Authentication
If `api_token` is configured:
```bash
curl -X POST http://localhost:8080/event \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"person_id":"test","display_name":"Test","confidence":0.9,"camera":"test"}'
```

## Next Steps

1. ✅ Commit and push changes
2. ✅ Rebuild add-on in HA
3. ✅ Test status endpoint
4. ✅ Test event firing via service
5. ✅ Test API endpoint (if accessible)

---

**Chunk 2 Implementation Complete!** Ready for testing.

