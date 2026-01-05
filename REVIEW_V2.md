# Face Recognition Project - V2 Review

## ✅ Excellent Improvements

### PRD v2 - Addressed Issues

1. **✅ IPC Mechanism** (Section 3)
   - Now explicitly shows "Local HTTP API (IPC)" in architecture
   - Clear separation between add-on and integration

2. **✅ Identity Storage** (Section 6)
   - Explicitly states "SQLite inside the add-on"
   - Clear separation: identities in DB, embeddings in model

3. **✅ Bootstrap Behavior** (Section 5)
   - Clear statement: "all faces are treated as Unknown" until model exists
   - Removes ambiguity about initial state

4. **✅ Model Format** (Section 10)
   - Specified "TensorFlow SavedModel"
   - Clear export format

5. **✅ Windows Compatibility** (Section 4.2)
   - Explicitly mentions "watchdog (cross-platform safe)"
   - Addresses inotify concern

6. **✅ Configuration** (Section 12)
   - New section for configuration & credentials
   - Mentions HA secrets for sensitive data

7. **✅ Retry Logic** (Section 13)
   - Added "Retry once on external failures"
   - Clear failure handling approach

### Build Chunks v2 - Addressed Issues

1. **✅ Chunk 0 Added**
   - Configuration & credentials setup first
   - Good foundation

2. **✅ Chunk 2 Clarified**
   - Specifies HTTP API endpoints (`POST /event`, `GET /status`)
   - Clear IPC mechanism

3. **✅ Chunk 4 Updated**
   - Explicitly mentions watchdog
   - Cross-platform safe

4. **✅ Chunk 7.5 Added**
   - Identity storage separated out
   - Good for testing independently

5. **✅ Chunk 7 Bootstrap**
   - Testing criteria includes "No model → all Unknown"
   - Validates bootstrap behavior

---

## 🔍 Minor Clarifications Needed

### 1. HTTP API Contract (Chunk 2)
**Current:** Endpoints specified (`POST /event`, `GET /status`)  
**Missing:** Request/response formats, error codes

**Suggestion:** Add to Chunk 2:
```yaml
POST /event
  Request: JSON payload matching HA event structure
  Response: 200 OK or error details
  
GET /status
  Response: { "status": "ready", "model_version": "v001" }
```

### 2. Drive Upload Format (Chunk 8)
**Current:** Mentions "sidecar JSON"  
**Missing:** Exact JSON schema

**Suggestion:** Add to Chunk 8:
```json
{
  "face_id": "img_20260105_143211_face_0",
  "timestamp": "2026-01-05T14:32:11Z",
  "camera": "nest_doorbell",
  "confidence": 0.45,
  "image_id": "img_20260105_143211.jpg"
}
```

### 3. Model Storage Location (Chunk 9-10)
**Current:** Model downloaded from Drive  
**Missing:** Where stored locally in add-on?

**Suggestion:** Add to PRD Section 11 or Chunk 10:
- Models stored in `/data/models/` (add-on persistent storage)
- `latest.txt` contains version string (e.g., "v004")

### 4. Chunk 7.5 Timing
**Current:** Comes after Chunk 7  
**Question:** Does Chunk 7 need identity DB, or just decision logic?

**Assessment:** ✅ Current order is fine if Chunk 7 only handles threshold decisions, and Chunk 7.5 adds identity management. But consider:
- Chunk 7 might need to query identities for display_name
- If so, Chunk 7.5 should come before Chunk 7, OR
- Chunk 7 uses mock/empty identity DB until 7.5

**Recommendation:** Clarify in Chunk 7 that it uses a minimal identity store (can be in-memory dict initially).

### 5. Chunk 10 Testing
**Current:** Missing testing criteria  
**Suggestion:** Add:
```yaml
Testing:
- Update model in Drive
- Trigger manual check → model downloads
- Confirm hot reload without restart
- Old events preserve old model_version
```

### 6. Image Deduplication (Chunk 4)
**Current:** Mentions "processed once"  
**Missing:** How deduplication works

**Suggestion:** Add to Chunk 4:
- Hash-based deduplication (MD5/SHA256 of image content)
- Dedupe window: 5 minutes (same image from same camera)

---

## 📋 Optional Enhancements

### 1. API Authentication
**Consideration:** Should HTTP API require authentication?
- Add-on runs locally, but security best practice
- Could use simple token or rely on network isolation

**Recommendation:** Add token-based auth in Chunk 2 (can be simple initially).

### 2. Health Check Endpoint
**Current:** `GET /status` mentioned  
**Enhancement:** Could include:
- Model loaded status
- Processing queue length
- Last processed timestamp
- Error counts

### 3. Chunk Dependencies Graph
**Visual aid:** Could add a simple dependency diagram:
```
Chunk 0 → Chunk 1 → Chunk 2 → Chunk 3,4 → Chunk 5 → Chunk 6 → Chunk 7 → Chunk 7.5 → Chunk 8 → Chunk 9 → Chunk 10 → Chunk 11 → Chunk 12
```

---

## ✅ Overall Assessment

**Status:** **READY TO BUILD** 🚀

The v2 documents have addressed all critical concerns from the initial review. The remaining items are minor clarifications that can be resolved during implementation or added as implementation details.

### Strengths:
- ✅ Clear architecture
- ✅ Explicit technical choices
- ✅ Good separation of concerns
- ✅ Incremental, testable chunks
- ✅ Bootstrap behavior clarified

### Recommendation:
**Proceed with Chunk 0** - The documents are solid enough to start implementation. Minor clarifications can be handled during development.

---

## 🎯 Pre-Build Checklist

Before starting Chunk 0, consider:
- [ ] Decide on HTTP API authentication approach (simple token vs. network isolation)
- [ ] Confirm Chunk 7 can work with minimal identity store before Chunk 7.5
- [ ] Prepare test images (known faces, unknown faces, no faces)
- [ ] Set up Google Drive folder structure manually
- [ ] Have HA development environment ready

---

## Questions for User

1. **API Auth:** Should the HTTP API require authentication, or rely on local network isolation?
2. **Chunk 7.5 Timing:** Is it okay if Chunk 7 uses a simple in-memory identity store initially?
3. **Model Storage:** Confirm `/data/models/` is acceptable for local model storage?
4. **Deduplication Window:** Is 5 minutes reasonable for same-image deduplication?

