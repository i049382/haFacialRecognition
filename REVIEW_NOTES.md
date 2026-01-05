# Face Recognition Project - Review Notes

## Overall Assessment
✅ **Well-structured PRD and build plan** - Clear scope, good separation of concerns, incremental approach.

## Critical Clarifications Needed

### 1. IPC Mechanism (Chunk 2)
**Issue:** PRD doesn't specify how add-on communicates with HA integration.

**Options:**
- Supervisor API (recommended for add-ons)
- HTTP API endpoint
- MQTT
- Shared filesystem + file watching

**Recommendation:** Use Supervisor API for add-on → integration communication. Add explicit details to Chunk 2.

---

### 2. Identity Storage (Chunk 7)
**Issue:** Where are person_id, display_name, and embeddings stored?

**Options:**
- SQLite database in add-on
- JSON files in `/config/faces/`
- Embedded in model metadata
- Separate identity registry

**Recommendation:** Use SQLite database in add-on persistent storage. Add to Chunk 7 scope.

---

### 3. Bootstrap Problem (Chunk 7)
**Issue:** Chunk 7 assumes model exists, but training is Chunk 9.

**Solution Options:**
- Start with empty model → all faces are "unknown" until Chunk 9
- Include a minimal bootstrap model in Chunk 7
- Clarify that Chunk 7 only handles decision logic, not actual recognition until Chunk 9

**Recommendation:** Clarify in Chunk 7 that recognition will return "unknown" until model is trained in Chunk 9.

---

### 4. Face Upload Format (Chunk 8)
**Issue:** Format of uploaded face crops not specified.

**Needs:**
- File naming convention (e.g., `{timestamp}_{face_id}_{hash}.jpg`)
- Metadata format (JSON sidecar? embedded?)
- Directory structure within `/review/`

**Recommendation:** Add to Chunk 8:
```
/faces/review/
  ├── 20260105_143211_img_abc123_face_0.jpg
  ├── 20260105_143211_img_abc123_face_0.json  # metadata
  └── ...
```

---

### 5. Model Format (Chunk 9-10)
**Issue:** Model format not specified.

**Options:**
- TensorFlow SavedModel
- ONNX
- Pickle (Python)
- Custom format

**Recommendation:** Specify TensorFlow SavedModel format in Chunk 9, include versioning schema.

---

### 6. Configuration Management
**Issue:** Where are configs stored?

**Needs:**
- Confidence thresholds
- Google Drive credentials/paths
- Camera watch directories
- Model paths
- Storage retention policies

**Recommendation:** Add configuration schema to PRD Section 20, implement in Chunk 1.

---

### 7. Windows Compatibility (Chunk 4)
**Issue:** Build chunks mention `inotify` (Linux-specific).

**Solution:** Use cross-platform library:
- Python `watchdog` library
- Works on Windows, Linux, macOS

**Recommendation:** Update Chunk 4 to specify `watchdog` library.

---

### 8. Error Recovery & Retry Logic
**Issue:** PRD mentions failures but not retry strategies.

**Needs:**
- Nest API fetch retries
- Drive upload retries
- Model download retries
- Backoff strategies

**Recommendation:** Add retry policies to relevant chunks (3, 8, 10).

---

## Suggested Additions

### Chunk 0: Configuration & Credentials Setup
**Scope:**
- Configuration schema definition
- Google Drive API credentials setup
- Configuration validation
- Environment variable handling

**Deliverables:**
- `config.schema.json` for add-on
- Credential setup instructions
- Config validation logic

---

### Enhanced Chunk 2: IPC Specification
Add explicit details:
- Supervisor API usage
- Event payload format
- Error handling
- Connection retry logic

---

### Chunk 7.5: Identity Registry (Optional)
If identity storage is complex, consider separate chunk:
- Database schema
- CRUD operations
- Avatar management
- Migration logic

---

## Testing Considerations

### Missing Test Data
- Sample face images (known/unknown)
- Test Nest event payloads
- Mock Drive responses
- Edge cases (no faces, multiple faces, poor quality)

**Recommendation:** Create `tests/fixtures/` directory structure.

---

## Technical Recommendations

### 1. Face Detection Library
**Recommendation:** Use `face_recognition` library (dlib-based) or MediaPipe Face Detection.
- Well-tested
- Good performance
- Python-friendly

### 2. Embedding Model
**Recommendation:** Use pre-trained model:
- FaceNet (TensorFlow)
- ArcFace
- InsightFace

### 3. Distance Metric
**Recommendation:** Cosine similarity or Euclidean distance (L2 normalized).

### 4. Database Choice
**Recommendation:** SQLite for simplicity, PostgreSQL if scale needed later.

---

## Alignment Check

### PRD ↔ Build Chunks Alignment
✅ Chunks follow PRD architecture
✅ Event structure matches PRD Section 8
✅ Drive structure matches PRD Section 9
⚠️ Missing: Configuration details
⚠️ Missing: Initial model bootstrap

---

## Questions for User

1. **IPC Preference:** Supervisor API, HTTP, or MQTT?
2. **Storage Preference:** SQLite, JSON files, or other?
3. **Model Format:** TensorFlow SavedModel acceptable?
4. **Initial State:** Start with empty model (all unknown) or bootstrap model?
5. **Windows Development:** Will you test on Windows or deploy to Linux HA instance?

---

## Priority Actions Before Starting

1. ✅ Resolve IPC mechanism (Chunk 2)
2. ✅ Define identity storage approach (Chunk 7)
3. ✅ Specify model format (Chunk 9)
4. ✅ Add configuration schema (Chunk 1)
5. ✅ Update Chunk 4 for Windows compatibility

---

## Additional Notes

- Consider adding health check endpoint in add-on
- Add metrics/logging structure early (Chunk 1)
- Consider Docker volume mounts for persistent storage
- Add-on restart behavior should be graceful (preserve in-flight processing)

