# Home Assistant Face Recognition System

A personal, event-driven face recognition system integrated with Home Assistant for home security awareness.

## Architecture

This project consists of two main components:

1. **Add-on** (`addon/`) - ML processing service running in isolated container
   - Face detection and recognition
   - Image ingestion from Nest and filesystem cameras
   - SQLite identity database
   - HTTP API for IPC

2. **Integration** (`integration/`) - Home Assistant custom integration
   - Consumes add-on HTTP API
   - Fires HA events (`face_recognition.detected`)
   - Exposes UI components

## Component Boundaries

- **ML processing**: Only in add-on
- **HA events**: Only in integration
- **Storage**: Add-on handles SQLite, integration handles HA state
- **IPC**: HTTP API between add-on and integration

## Development Status

Currently implementing **Chunk 0: Configuration & Credentials**

See `ha_face_recognition_build_chunks_v2.md` for build plan.

