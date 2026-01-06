# Home Assistant Face Recognition – Build Chunks & Testing Plan

This document must be followed **in conjunction with the PRD**.

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

## Chunk 1 – Repository & Skeleton Setup

### Scope
- Repo structure
- Add-on skeleton
- Integration skeleton

### Testing
- Add-on installs
- Integration loads
- HA responsive

---

## Chunk 2 – IPC & Event Plumbing

### Scope
- Add-on exposes local HTTP API
- Integration consumes API and fires HA events

### Deliverables
- `POST /event`
- `GET /status`

### Testing
- Mock event → HA event visible

---

## Chunk 3 – Nest Event Ingestion

### Scope
- Listen to `nest_event`
- Fetch snapshot immediately

### Testing
- Event → image saved
- Expired media → failure shown

---

## Chunk 4 – Filesystem Camera Ingestion

### Scope
- Watch directories using **watchdog**

### Testing
- New file → processed once

---

## Chunk 5 – Face Detection

### Scope
- Detect & crop faces
- Multi-face handling

### Testing
- 0 / 1 / many faces

---

## Chunk 6 – Embeddings

### Scope
- Generate embeddings
- Distance metrics

### Testing
- Same face similarity

---

## Chunk 7 – Recognition Logic

### Scope
- Threshold decisions
- Bootstrap behaviour

### Testing
- No model → all Unknown

---

## Chunk 7.5 – Identity Storage

### Scope
- SQLite identity DB
- Rename/update without retraining

### Testing
- Rename person → history preserved

---

## Chunk 8 – Drive Upload (Review Only)

### Scope
- Upload cropped faces + sidecar JSON

### Testing
- Unknown → uploaded
- Known → skipped

---

## Chunk 9 – Colab Training

### Scope
- Review
- Label
- Train
- Export SavedModel

---

## Chunk 10 – Model Sync

### Scope
- Manual update check
- Optional daily poll

---

## Chunk 11 – Timeline UI

### Scope
- Face-centric timeline
- Failure states

---

## Chunk 12 – Correlation & Automations

### Scope
- Multi-camera correlation
- Example automations

---

## Build Rules

- Follow order strictly
- Do not skip chunks
- Respect PRD constraints
