# Home Assistant Face Recognition – Build Chunks & Testing Plan

This document is designed to be used **in conjunction with the PRD** as a strict, ordered build guide for AI-assisted development.

Each chunk is:
- Independently buildable
- Independently testable
- Safe to stop after
- Explicit about scope and success criteria

**Rule:** Do not start a new chunk until the previous chunk’s success criteria are met.

---

## Chunk 1 – Repository & Skeleton Setup

### Scope
- Project repository structure
- Home Assistant add-on skeleton
- Home Assistant custom integration skeleton

### Deliverables
- `addon/`
  - `Dockerfile`
  - `config.yaml`
  - `run.sh`
- `integration/`
  - `manifest.json`
  - `__init__.py`
  - `events.py`
- README describing boundaries

### Testing
- Install add-on → starts without crashing
- Install integration → HA boots cleanly
- No ML logic present

### Success Criteria
- Home Assistant fully responsive
- No errors in logs

---

## Chunk 2 – Event Plumbing (Add-on → HA)

### Scope
- IPC between add-on and HA integration
- Custom HA event emission

### Deliverables
- Mock recognition event sent from add-on
- HA event `face_recognition.detected`

### Test Payload
```json
{
  "person_id": "test_001",
  "display_name": "Test Person",
  "confidence": 0.99,
  "camera": "test_camera"
}
```

### Testing
- Listen in HA Developer Tools → Events
- Trigger automation from event

### Success Criteria
- Events fire reliably
- Automations trigger instantly

---

## Chunk 3 – Nest Event Ingestion (No ML)

### Scope
- Listen to `nest_event`
- Fetch snapshot image
- Persist locally with metadata

### Deliverables
- Nest event listener
- Snapshot fetch via HA API
- Metadata JSON stored alongside image

### Testing
- Trigger Nest event → image saved
- Restart HA during event → failure logged

### Success Criteria
- Images saved reliably
- Failures visible in logs/UI

---

## Chunk 4 – Filesystem Camera Ingestion

### Scope
- Watch directory for new images
- Deduplicate images
- Normalise metadata

### Deliverables
- File watcher
- Hash-based deduplication
- Unified image object

### Testing
- Drop image → detected
- Duplicate image → processed once

### Success Criteria
- No duplicate processing
- No missed files

---

## Chunk 5 – Face Detection Only

### Scope
- Face detection
- Face cropping
- Multi-face handling

### Deliverables
- Face detector wrapper
- Bounding boxes
- Cropped face images

### Testing
- Images with:
  - No faces
  - One face
  - Multiple faces

### Success Criteria
- Correct face counts
- Reasonable crops

---

## Chunk 6 – Embeddings & Distance Metrics

### Scope
- Embedding generation
- Distance calculation
- No recognition yet

### Deliverables
- Embedding generator
- Vector storage format
- Distance function

### Testing
- Same face twice → low distance
- Different faces → higher distance

### Success Criteria
- Stable, repeatable embeddings

---

## Chunk 7 – Recognition Logic & Thresholds

### Scope
- Recognition decisions
- Confidence thresholds
- Review flagging

### Deliverables
- Decision engine
- Threshold configuration
- Review markers

### Testing
- Known face → recognised
- Borderline face → review
- Unknown face → unknown

### Success Criteria
- Deterministic outcomes
- No flapping results

---

## Chunk 8 – Google Drive Upload (Review Only)

### Scope
- Upload unknown/review faces
- Correct Drive structure

### Deliverables
- Drive client
- Upload queue
- Retry-once logic

### Testing
- Unknown face → uploaded
- Known face → NOT uploaded
- Drive offline → graceful failure

### Success Criteria
- Drive remains clean
- Failures do not block pipeline

---

## Chunk 9 – Google Colab Notebook (Review + Train)

### Scope
- Single Colab notebook
- Review UI
- Training pipeline
- Model export

### Deliverables
- Review loop
- Label assignment
- Trained model
- `latest.txt`

### Testing
- Review faces
- Train model
- Verify model folder created

### Success Criteria
- No data overwrite
- Deterministic model output

---

## Chunk 10 – Model Sync & Hot Reload

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
- Trigger update
- Confirm reload without restart

### Success Criteria
- No HA restart required
- Old results preserved

---

## Chunk 11 – Timeline UI

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

---

## Chunk 12 – Correlation & Automations

### Scope
- Multi-camera correlation
- Example automations

### Deliverables
- Correlation logic
- Sample YAML automations

### Testing
- Two cameras detect same person
- Only one notification sent

### Success Criteria
- No alert spam
- Timeline retains full detail

---

## Build Rules for AI Coders

- Follow chunk order strictly
- Do not introduce features early
- Do not refactor across chunks
- Obey PRD constraints at all times
- Ask before deviating

---

## End of Document
