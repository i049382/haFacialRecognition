# Home Assistant Face Recognition System PRD

## 1. Purpose
Build a **personal, event-driven face recognition system** integrated with Home Assistant (HA), designed for home security awareness.  
The system performs **local inference only**, uses **manual, human-in-the-loop training**, and integrates cleanly with HA automations.

This PRD is written to support **AI-assisted implementation** (Cursor, Copilot, ChatGPT, etc.) and is intentionally explicit and prescriptive.

---

## 2. Goals
- Recognise known individuals from camera images
- Surface recognition results as HA-native events
- Allow manual review and training via Google Colab
- Support multiple cameras observing the same area
- Avoid impacting HA core responsiveness

### Non-Goals
- No real-time video analysis
- No continuous face tracking
- No automatic or self-learning training
- No identity verification or compliance guarantees
- No multi-user workflows

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
 - Decision logic
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
- Relevant event types: `person`, optionally `motion`
- Media retrieved via:
  `/api/nest/event_media/<device_id>/<event_id>/thumbnail`
- Media URLs are **time-limited** and must be fetched immediately

### 4.2 Filesystem Cameras (e.g. Eufy)
- Trigger: new image file written to configured directory
- Detection via filesystem watch (e.g. inotify)
- File assumed complete on arrival

All images are normalised into a common internal format before inference.

---

## 5. Face Recognition Pipeline

For every image:

1. Face detection
2. Face crop
3. Embedding generation
4. Match against known identities
5. Confidence scoring
6. Decision routing

### Decision Rules
- Confidence ≥ threshold → recognised
- Confidence below threshold → review required
- No match → unknown

Only **unknown or low-confidence faces** are sent to Google Drive.

---

## 6. Identity Model

- Each person is identified by a **UID**
- Names are labels, not identifiers
- Multiple people may share the same name

```json
{
  "person_id": "person_017",
  "display_name": "Alice (Neighbour)",
  "avatar": "/local/faces/avatars/person_017.jpg",
  "avatar_locked": false
}
```

### Avatar Rules
- Default avatar generated from best face crop
- Manual override supported
- Locked avatars are never auto-updated

---

## 7. Multi-Face & Multi-Camera Handling

- Each detected face is processed independently
- One HA event is fired **per face**
- Multiple cameras may detect the same person
- Correlation is handled at automation level (not ML level)

Recommended correlation window: **10–30 seconds** per person_id.

---

## 8. Home Assistant Events

### Event Name
`face_recognition.detected`

### Example Payload
```json
{
  "person_id": "person_017",
  "display_name": "Alice (Neighbour)",
  "confidence": 0.94,
  "camera": "nest_doorbell",
  "image_id": "img_20260105_143211.jpg",
  "face_id": "img_..._face_0",
  "timestamp": "2026-01-05T14:32:11Z",
  "model_version": "v004",
  "avatar": "/local/faces/avatars/person_017.jpg"
}
```

Unknown or review-required faces include:
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
 ├── review/        # Unknown / low-confidence face crops
 ├── training/      # Curated labelled faces
 ├── models/
 │    ├── model_v001/
 │    └── latest.txt
```

Rules:
- HA writes only to `/review/`
- Colab writes to `/training/` and `/models/`
- No component overwrites another’s output

---

## 10. Google Colab Workflow (Single Notebook)

1. Load review faces from Drive
2. Display face crops
3. Assign identity (existing UID or new)
4. Promote selected faces to training
5. Train classifier
6. Save model to `/models/model_vXYZ/`
7. Update `latest.txt`

Training is **manual only**.

---

## 11. Model Lifecycle

- HA does not poll constantly
- Two update mechanisms:
  - Manual “Check for model updates” button
  - Optional daily poll
- Model hot-reloaded without HA restart
- Only faces marked `needs_review` are reprocessed

---

## 12. Storage Policy

- Recognised face metadata: **30 days minimum**, optional permanent
- Unknown/review faces: **30 days**, unless kept
- Full images: cache only, unless required for review

---

## 13. Non-Functional Requirements

### Performance
- Target latency: **≤ 2–3 seconds**
- Hard limit: **≤ 5 seconds**

### Resource Isolation
- ML runs only in HA add-on
- CPU and concurrency limits enforced
- Max inference concurrency: **1 (initially)**

### Failure Handling
- Failures logged
- Marked visibly in UI timeline
- No silent drops

---

## 14. Risks & Mitigations

| Risk | Mitigation |
|----|----|
| Nest media expiry | Immediate fetch, log failure |
| CPU contention | Add-on isolation + limits |
| Detection errors | Conservative thresholds |
| Dataset bias | Manual curation |
| Review backlog | Auto-expiry |

---

## 15. Dependencies

- Google Nest SDM API
- Google Drive API
- Google Colab availability
- TensorFlow runtime inside add-on

---

## 16. Assumptions

- Single home environment
- Reasonable time sync
- Personal/private use only

---

## 17. Out of Scope

- Real-time video processing
- Automatic learning
- Multi-user support
- Compliance guarantees

---

## 18. AI Implementation Notes

- Follow component boundaries strictly
- Do not introduce automatic training
- Do not move ML into HA core
- Use events, not sensors, for recognition

---

## 19. Success Criteria

- Recognition events fire reliably
- HA remains responsive
- Manual training loop works end-to-end
- No unintended data growth

---
