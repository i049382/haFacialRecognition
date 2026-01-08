# Home Assistant Face Recognition System PRD v3
## Simplified Service-Based Architecture

## 1. Purpose
Build a **personal, service-driven face recognition system** integrated with Home Assistant (HA), designed for home security awareness.
The system performs **local inference only**, uses **manual, human-in-the-loop training**, and integrates cleanly with HA automations via services.

This simplified version focuses on **service-based recognition** where automations call the recognition service, rather than automatic ingestion from cameras.

## 2. Goals
- Provide face recognition as a service callable from HA automations
- Surface recognition results as HA-native events
- Allow manual review and training via Google Colab
- Never impact HA core responsiveness

### Non-Goals
- Automatic camera event ingestion (Nest, filesystem)
- Real-time video analysis
- Continuous face tracking
- Automatic/self-learning training
- Identity verification or compliance guarantees
- Multi-user workflows

---

## 3. High-Level Architecture

```
Home Assistant Automation
        ↓ (calls service)
face_recognition.recognize_face service
        ↓
Home Assistant Integration
 - HTTP client to add-on
 - Event firing
        ↓
Home Assistant Add-on (ML)
 - Face detection
 - Embedding generation
 - Recognition
 - Identity DB (SQLite)
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

## 4. Service-Based Recognition Flow

### 4.1 Recognition Service
- Service name: `face_recognition.recognize_face`
- Called from HA automations with image data
- Supports multiple image sources:
  - Camera entity ID
  - Image URL (local or remote)
  - Base64 encoded image data

### 4.2 Service Response
- Returns recognition results immediately
- Includes person ID, confidence, review flag
- Fires HA event `face_recognition.detected` with results

### 4.3 Automation Integration Example
```yaml
automation:
  - alias: "Recognize face from camera snapshot"
    trigger:
      - platform: state
        entity_id: binary_sensor.motion_detected
        to: "on"
    action:
      - service: face_recognition.recognize_face
        data:
          entity_id: camera.front_door
          camera: "front_door"
```

---

## 5. Face Recognition Pipeline

For every image received via service:

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

## 7. Home Assistant Events

Event: `face_recognition.detected`

```json
{
  "person_id": "person_017",
  "display_name": "Alice (Neighbour)",
  "confidence": 0.94,
  "camera": "front_door",
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

## 8. Google Drive Contract

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
- No component overwrites another's output

---

## 9. Colab Training

- Single notebook
- Manual review & labelling
- Train classifier
- Export **TensorFlow SavedModel**
- Update `latest.txt`

---

## 10. Model Lifecycle

- Manual "Check for updates" button
- Optional daily poll
- Hot reload without HA restart
- Reprocess **review faces only**

---

## 11. Configuration & Credentials

- Add-on `config.yaml`:
  - Thresholds
  - Polling options
- Secrets via HA (Drive credentials, tokens)
- No hard-coded secrets

---

## 12. Non-Functional Requirements

- Target latency: ≤ 2–3s
- Hard limit: ≤ 5s
- ML isolated in add-on
- Max inference concurrency: 1
- Retry once on external failures
- Failures logged and shown in UI

---

## 13. Risks & Dependencies

- CPU contention → add-on isolation & limits
- Google Drive API limits → manual/daily checks only
- Colab availability → non-critical dependency

---

## 14. Assumptions

- Single home environment
- Reasonable time sync
- Personal/private use only

---

## 15. Out of Scope

- Automatic camera ingestion
- Real-time video processing
- Automatic learning
- Multi-user support
- Compliance guarantees

---

## 16. AI Implementation Rules

- Respect component boundaries
- No ML in HA core
- No automatic training
- Use events, not sensors

---

## 17. Success Criteria

- Recognition service works reliably from automations
- HA remains responsive
- Manual training loop works end-to-end
- No unintended data growth