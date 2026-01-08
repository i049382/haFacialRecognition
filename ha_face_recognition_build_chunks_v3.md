# Home Assistant Face Recognition – Build Chunks & Testing Plan v3
## Simplified Service-Based Architecture

This document must be followed **in conjunction with the PRD v3**.

---

## Chunk 0 – Configuration & Credentials ✅ COMPLETE

### Scope
- Add-on configuration
- Secret handling

### Deliverables
- ✅ `config.yaml` schema
- ✅ Threshold config
- ✅ Drive auth via HA secrets

### Testing
- ✅ Add-on loads config
- ✅ Missing secrets fail gracefully

### Status
**COMPLETE** - Tested and working in Home Assistant (2026-01-06)

---

## Chunk 1 – Repository & Skeleton Setup ✅ COMPLETE

### Scope
- Repo structure
- Add-on skeleton
- Integration skeleton

### Testing
- ✅ Add-on installs
- ✅ Integration loads
- ✅ HA responsive

### Status
**COMPLETE** - Verified structure and imports

---

## Chunk 2 – IPC & Event Plumbing ✅ COMPLETE

### Scope
- Add-on exposes local HTTP API
- Integration provides `recognize_face` service
- Service calls add-on API and fires HA events

### Deliverables
- ✅ `POST /event` endpoint in add-on
- ✅ `GET /status` endpoint in add-on
- ✅ `face_recognition.recognize_face` service
- ✅ `face_recognition.detected` events

### Testing
- ✅ HTTP API accessible on port 8080
- ✅ Status endpoint returns correct JSON
- ✅ Service accepts image data and returns results
- ✅ Events fire from service responses

### Status
**COMPLETE** - Implemented and ready for testing

---

## Chunk 3 – Face Detection

### Scope
- Detect faces in images
- Crop faces
- Multi-face handling

### Deliverables
- Face detector wrapper
- Bounding box extraction
- Cropped face images

### Testing
- Images with no faces → 0 faces detected
- Images with one face → 1 face detected
- Images with multiple faces → N faces detected
- Reasonable crop regions

### Success Criteria
- Correct face counts
- Reasonable crops
- No crashes on malformed images

---

## Chunk 4 – Embeddings & Distance Metrics

### Scope
- Embedding generation from face crops
- Distance calculation between embeddings
- No recognition yet

### Deliverables
- Embedding generator
- Vector storage format
- Distance function

### Testing
- Same face twice → low distance (< 0.3)
- Different faces → higher distance (> 0.5)
- Stable, repeatable embeddings

### Success Criteria
- Stable, repeatable embeddings
- Distance metric behaves intuitively

---

## Chunk 5 – Recognition Logic & Thresholds

### Scope
- Recognition decisions based on embeddings
- Confidence thresholds
- Review flagging

### Deliverables
- Decision engine
- Threshold configuration
- Review markers

### Testing
- Known face (in training set) → recognised
- Borderline face → marked for review
- Unknown face → marked unknown
- Deterministic outcomes

### Success Criteria
- Deterministic outcomes
- No flapping results
- Thresholds configurable

---

## Chunk 6 – Identity Storage

### Scope
- SQLite identity database
- Person metadata storage
- Rename/update without retraining

### Deliverables
- SQLite schema
- Person CRUD operations
- Avatar management

### Testing
- Create person → stored in DB
- Rename person → history preserved
- Delete person → clean removal

### Success Criteria
- Persistent storage across restarts
- No data corruption
- Efficient queries

---

## Chunk 7 – Google Drive Upload (Review Only)

### Scope
- Upload unknown/review faces to Drive
- Correct Drive folder structure
- Sidecar JSON with metadata

### Deliverables
- Drive client
- Upload queue
- Retry-once logic

### Testing
- Unknown face → uploaded to `/review/`
- Known face → NOT uploaded
- Drive offline → graceful failure
- Drive remains clean

### Success Criteria
- Drive folder structure maintained
- Failures don't block pipeline
- No duplicate uploads

---

## Chunk 8 – Google Colab Notebook (Review + Train)

### Scope
- Single Colab notebook
- Review UI for unknown faces
- Training pipeline
- Model export

### Deliverables
- Review loop
- Label assignment
- Trained model
- `latest.txt` update

### Testing
- Load review faces from Drive
- Assign labels
- Train model
- Export model to Drive

### Success Criteria
- No data overwrite
- Deterministic model output
- Model compatible with add-on

---

## Chunk 9 – Model Sync & Hot Reload

### Scope
- Manual update check
- Optional daily poll
- Model hot reload

### Deliverables
- Version checker
- Safe reload logic
- Reprocess review faces only

### Testing
- Update model in Drive
- Trigger manual update
- Confirm reload without restart

### Success Criteria
- No HA restart required
- Old results preserved
- Smooth transition

---

## Chunk 10 – Timeline UI

### Scope
- Face-centric timeline
- Avatars
- Failure states

### Deliverables
- Lovelace card
- Filters
- Error indicators

### Testing
- Known face → avatar shown
- Unknown face → default avatar
- Failure → visible error state

### Success Criteria
- Clean, readable UI
- No clutter
- Responsive

---

## Chunk 11 – Correlation & Automations

### Scope
- Multi-camera correlation (if used)
- Example automations

### Deliverables
- Correlation logic (optional)
- Sample YAML automations

### Testing
- Multiple recognition events
- Correlation reduces noise
- Automation triggers correctly

### Success Criteria
- No alert spam
- Timeline retains full detail

---

## Build Rules

- Follow order strictly
- Do not skip chunks
- Respect PRD v3 constraints
- Test each chunk before proceeding