# Home Assistant Face Recognition System PRD

## 1. Purpose
Build a **personal, event-driven face recognition system** integrated with Home Assistant (HA), designed for home security awareness.  
The system performs **local inference only**, uses **manual, human-in-the-loop training**, and integrates cleanly with HA automations.

This PRD is written to support **AI-assisted implementation** and is intentionally explicit.

---

## 2. Goals
- Recognise known individuals from camera images
- Surface recognition results as HA-native events
- Allow manual review and training via Google Colab
- Support multiple cameras observing the same area
- Never impact HA core responsiveness

### Non-Goals
- Real-time video analysis
- Continuous face tracking
- Automatic/self-learning training
- Identity verification or compliance guarantees
- Multi-user workflows

---

## 3. High-Level Architecture

```
Cameras
 ├─ Google Nest (event-driven)
 └─ Local cameras (filesystem-driven)
        ↓
Home Assistant Add-on (ML)
 - Image ingestion
 - Face detection
 - Embedding generation
 - Recognition
 - Identity DB (SQLite)
        ↓
Local HTTP API (IPC)
        ↓
Home Assistant Integration
 - Fires HA events
 - Exposes UI data
        ↓
Google Drive
 - Review faces
 - Training data
 - Models
        ↓
Google Colab
 - Review & label
 - Train model
 - Promote model
```

---

## 4. Ingestion Sources

### 4.1 Google Nest Cameras
- Trigger: `nest_event`
- Media fetched immediately via:
  `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
- Media URLs are **time-limited**

### 4.2 Filesystem Cameras
- Trigger: new image file
- Detection via **watchdog** (cross-platform safe)
- Files assumed complete on arrival

---

## 5. Face Recognition Pipeline

1. Face detection
2. Face crop
3. Embedding generation
4. Identity matching (if model exists)
5. Confidence scoring
6. Decision routing

### Bootstrap Behaviour
- Until a trained model exists, **all faces are treated as Unknown**
- Recognition activates only after a model is loaded successfully

---

## 6. Identity Model & Storage

- Each person has a stable **UID**
- Names are labels only
- Identities stored in **SQLite inside the add-on**
- Model stores embeddings/classifier only

```json
{
  "person_id": "person_017",
  "display_name": "Alice (Neighbour)",
  "avatar": "/local/faces/avatars/person_017.jpg",
  "avatar_locked": false
}
```

---

## 7. Multi-Face & Multi-Camera Handling

- Each face processed independently
- One HA event fired per face
- Multiple cameras may detect same person
- Correlation handled in automations (10–30s window)

---

## 8. Home Assistant Events

Event: `face_recognition.detected`

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

Unknown/review faces include:
```json
{
  "person_id": null,
  "display_name": "Unknown",
  "needs_review": true
}
```

---

## 9. Google Drive Contract

```
/faces/
 ├── review/
 │    ├── face_xxx.jpg
 │    └── face_xxx.json
 ├── training/
 └── models/
      ├── model_v001/
      └── latest.txt
```

- HA writes only to `/review`
- Colab writes to `/training` and `/models`
- No component overwrites another’s output

---

## 10. Colab Training

- Single notebook
- Manual review & labelling
- Train classifier
- Export **TensorFlow SavedModel**
- Update `latest.txt`

---

## 11. Model Lifecycle

- Manual “Check for updates” button
- Optional daily poll
- Hot reload without HA restart
- Reprocess **review faces only**

---

## 12. Configuration & Credentials

- Add-on `config.yaml`:
  - Camera paths
  - Thresholds
  - Polling options
- Secrets via HA (Drive credentials, tokens)
- No hard-coded secrets

---

## 13. Non-Functional Requirements

- Target latency: ≤ 2–3s
- Hard limit: ≤ 5s
- ML isolated in add-on
- Max inference concurrency: 1
- Retry once on external failures
- Failures logged and shown in UI

---

## 14. Risks & Dependencies

- Nest media expiry → immediate fetch + failure surfacing
- CPU contention → add-on isolation & limits
- Google Drive API limits → manual/daily checks only
- Colab availability → non-critical dependency

---

## 15. Assumptions

- Single home environment
- Reasonable time sync
- Personal/private use only

---

## 16. Out of Scope

- Real-time video processing
- Automatic learning
- Multi-user support
- Compliance guarantees

---

## 17. AI Implementation Rules

- Respect component boundaries
- No ML in HA core
- No automatic training
- Use events, not sensors
